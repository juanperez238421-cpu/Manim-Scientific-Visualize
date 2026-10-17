"""Train the learned in-betweener (numpy only, deterministic seed).

Task: given two frames before a gap and two frames after it (a window of N frames, 6..40 at 60 fps),
predict every frame in between. The network predicts a correction to the cubic Hermite in-between,
multiplied by 4u(1-u) so the two keys are always kept exactly.

Mirrors src/neural/features.js (window-relative transform) and src/neural/inbetween.js (inputs,
baseline, window). Outputs:
  src/neural/weights/inbetween_v1.json   weights + normalisation + metrics (loaded by the JS runtime)
  qa/neural_report.json                  evaluation on held-out sequences (val + test)

usage: .venv/bin/python packages/bonemotion/train/train_inbetween.py [--epochs 40]
"""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
DIM = 46
POS_BLOCKS = [0, 19, 26, 33, 39]
ANG_IDX = [3, 22, 29]
NMIN, NMAX = 6, 40

ap = argparse.ArgumentParser()
ap.add_argument('--data', default=str(ROOT / 'build' / 'bonemotion' / 'dataset'))
ap.add_argument('--epochs', type=int, default=40)
ap.add_argument('--per-epoch', type=int, default=260_000)
ap.add_argument('--hidden', type=int, default=256)
ap.add_argument('--batch', type=int, default=1024)
ap.add_argument('--lr', type=float, default=1.5e-3)
args = ap.parse_args()

meta = json.loads((Path(args.data) / 'meta.json').read_text())
assert meta['layout'] == 'bm-feat-v1' and meta['dim'] == DIM, 'feature layout mismatch with features.js'
F = np.fromfile(Path(args.data) / 'frames.f32', dtype=np.float32).reshape(-1, DIM).astype(np.float64)
seqs = []
off = 0
for s in meta['sequences']:
    seqs.append({'fam': s['fam'], 'split': s['split'], 'start': off, 'n': s['frames']})
    off += s['frames']
rng = np.random.default_rng(1016)


def windows(split, count, gen, Ns=None):
    """random (window, in-between) samples from one split -> dict of arrays"""
    S = [s for s in seqs if s['split'] == split and s['n'] > NMAX + 4]
    lens = np.array([s['n'] for s in S], dtype=np.float64)
    which = gen.choice(len(S), size=count, p=lens / lens.sum())
    N = gen.integers(NMIN, NMAX + 1, size=count) if Ns is None else np.asarray(Ns)
    st = np.array([S[w]['start'] for w in which]); n = np.array([S[w]['n'] for w in which])
    s0 = st + 1 + (gen.random(count) * (n - N - 3)).astype(int)
    j = 1 + (gen.random(count) * (N - 1)).astype(int)
    fam = np.array([S[w]['fam'] for w in which])
    return dict(Am1=F[s0 - 1], A0=F[s0], A1=F[s0 + N], A2=F[s0 + N + 1], Aj=F[s0 + j], N=N.astype(np.float64), u=j / N, fam=fam,
                Aj_prev=F[s0 + j - 1], s0=s0, j=j)


def to_rel(A, p0, y0):
    c, s = np.cos(y0)[:, None], np.sin(y0)[:, None]
    R = A.copy()
    for o in POS_BLOCKS:
        x, y, z = A[:, o] - p0[:, 0], A[:, o + 1] - p0[:, 1], A[:, o + 2] - p0[:, 2]
        R[:, o] = c[:, 0] * x - s[:, 0] * z; R[:, o + 1] = y; R[:, o + 2] = s[:, 0] * x + c[:, 0] * z
    for k in ANG_IDX:
        R[:, k] = A[:, k] - y0
    return R


def prepare(W):
    p0, y0 = W['A0'][:, 0:3], W['A0'][:, 3]
    Rm1, R0, R1, R2, Rj = (to_rel(W[k], p0, y0) for k in ('Am1', 'A0', 'A1', 'A2', 'Aj'))
    N, u = W['N'][:, None], W['u'][:, None]
    h00, h10, h01, h11 = 2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2, u**3 - u**2
    base = h00 * R0 + h10 * (R0 - Rm1) * N + h01 * R1 + h11 * (R2 - R1) * N
    lin = R0 + (R1 - R0) * u
    extra = np.concatenate([N / 40, u, np.sin(np.pi * u), np.cos(np.pi * u), np.sin(2 * np.pi * u)], axis=1)
    X = np.concatenate([Rm1, R0, R1, R2, extra], axis=1)
    return X, base, lin, Rj, (4 * u * (1 - u))


# ---------------------------------------------------------------- normalisation (from training data)
Xs, Bs, _, Ys, Ws = prepare(windows('train', 200_000, rng))
in_mean, in_std = Xs.mean(0), np.maximum(Xs.std(0), 1e-3)
res = (Ys - Bs) / np.maximum(Ws, 0.05)
res_std = np.maximum(res.std(0), 1e-3)
del Xs, Bs, Ys, Ws, res

# ---------------------------------------------------------------- the network
H = args.hidden
nin = 4 * DIM + 5
def init(nout, ninp):
    return rng.normal(0, math.sqrt(2.0 / ninp), size=(nout, ninp)), np.zeros(nout)
params = [init(H, nin), init(H, H), init(DIM, H)]
params[-1] = (params[-1][0] * 0.1, params[-1][1])
m = [(np.zeros_like(W), np.zeros_like(b)) for W, b in params]
v = [(np.zeros_like(W), np.zeros_like(b)) for W, b in params]


def elu(x):
    return np.where(x > 0, x, np.expm1(np.minimum(x, 0)))


def forward(Xn):
    acts = [Xn]
    zs = []
    h = Xn
    for li, (W, b) in enumerate(params):
        z = h @ W.T + b
        zs.append(z)
        h = elu(z) if li < len(params) - 1 else z
        acts.append(h)
    return h, acts, zs


def loss_and_grad(X, base, Y, w):
    Xn = (X - in_mean) / in_std
    o, acts, zs = forward(Xn)
    target = (Y - base) / res_std  # normalised residual
    err = w * o - target
    L = np.mean(err ** 2)
    g = 2 * err * w / err.size
    grads = []
    for li in range(len(params) - 1, -1, -1):
        W, b = params[li]
        gW = g.T @ acts[li]
        gb = g.sum(0)
        grads.append((gW, gb))
        if li > 0:
            g = g @ W
            z = zs[li - 1]
            g = g * np.where(z > 0, 1.0, np.exp(np.minimum(z, 0)))
    return L, grads[::-1]


def predict(X, base, w):
    o, _, _ = forward((X - in_mean) / in_std)
    return base + w * o * res_std


steps_per_epoch = args.per_epoch // args.batch
total = steps_per_epoch * args.epochs
b1, b2, eps = 0.9, 0.999, 1e-8
step = 0
val = windows('val', 30_000, np.random.default_rng(7))
Xv, Bv, Lv, Yv, Wv = prepare(val)
hist = []
t0 = time.time()
for ep in range(args.epochs):
    W_ = windows('train', args.per_epoch, rng)
    X, B, _, Y, Wt = prepare(W_)
    perm = rng.permutation(len(X))
    tl = 0.0
    for k in range(steps_per_epoch):
        idx = perm[k * args.batch:(k + 1) * args.batch]
        L, grads = loss_and_grad(X[idx], B[idx], Y[idx], Wt[idx])
        tl += L
        step += 1
        lr = args.lr * 0.5 * (1 + math.cos(math.pi * step / total)) + 2e-5
        for i, ((W, b), (gW, gb)) in enumerate(zip(params, grads)):
            mW, mb = m[i]; vW, vb = v[i]
            mW = b1 * mW + (1 - b1) * gW; mb = b1 * mb + (1 - b1) * gb
            vW = b2 * vW + (1 - b2) * gW * gW; vb = b2 * vb + (1 - b2) * gb * gb
            m[i] = (mW, mb); v[i] = (vW, vb)
            c1, c2 = 1 - b1 ** step, 1 - b2 ** step
            params[i] = (W - lr * (mW / c1) / (np.sqrt(vW / c2) + eps), b - lr * (mb / c1) / (np.sqrt(vb / c2) + eps))
    Pv = predict(Xv, Bv, Wv)
    vl = float(np.mean(((Pv - Yv) / res_std) ** 2))
    vh = float(np.mean(((Bv - Yv) / res_std) ** 2))
    hist.append({'epoch': ep + 1, 'train_loss': tl / steps_per_epoch, 'val_loss': vl, 'val_loss_hermite': vh, 'seconds': round(time.time() - t0, 1)})
    print(f"epoch {ep + 1:2d}  train {tl / steps_per_epoch:.4f}  val {vl:.4f}  (hermite {vh:.4f})  {time.time() - t0:.0f} s", flush=True)


# ---------------------------------------------------------------- evaluation on held-out sequences
def pos_err(P, Y):
    """mean Euclidean error over the 5 tracked points (root, ankles, wrists), in cm"""
    e = [np.linalg.norm(P[:, o:o + 3] - Y[:, o:o + 3], axis=1) for o in POS_BLOCKS]
    return np.mean(e, axis=0) / 2.0  # u -> cm (200 u = 1 m)


def evaluate(split):
    out = {}
    g = np.random.default_rng(99)
    for Nfix in (10, 20, 30, 40):
        W_ = windows(split, 20_000, g, Ns=np.full(20_000, Nfix))
        X, B, Lin, Y, Wt = prepare(W_)
        P = predict(X, B, Wt)
        r = {}
        for name, Q in (('linear', Lin), ('hermite', B), ('neural', P)):
            pe = pos_err(Q, Y)
            ang = np.mean(np.abs(Q[:, 4:19] - Y[:, 4:19]))
            r[name] = {'pos_cm': float(pe.mean()), 'pos_cm_p90': float(np.percentile(pe, 90)), 'angle_mae_rad': float(ang)}
        # per family (neural vs hermite)
        fams = {}
        for f in np.unique(W_['fam']):
            sel = W_['fam'] == f
            fams[str(f)] = {'hermite_cm': float(pos_err(B[sel], Y[sel]).mean()), 'neural_cm': float(pos_err(P[sel], Y[sel]).mean()), 'n': int(sel.sum())}
        r['families'] = fams
        out[f'N{Nfix}'] = r
    return out


report = {'data': {'sequences': len(seqs), 'frames': int(F.shape[0]),
                   'train_seqs': sum(s['split'] == 'train' for s in seqs), 'val_seqs': sum(s['split'] == 'val' for s in seqs), 'test_seqs': sum(s['split'] == 'test' for s in seqs)},
          'model': {'inputs': nin, 'hidden': [H, H], 'outputs': DIM, 'params': int(sum(W.size + b.size for W, b in params)), 'activation': 'ELU', 'epochs': args.epochs, 'optimizer': 'Adam + cosine'},
          'history': hist, 'val': evaluate('val'), 'test': evaluate('test')}
for split in ('val', 'test'):
    for k, r in report[split].items():
        print(split, k, {m_: round(r[m_]['pos_cm'], 2) for m_ in ('linear', 'hermite', 'neural')})

wout = HERE / 'src' / 'neural' / 'weights' / 'inbetween_v1.json'
r6 = lambda a: [float(f'{x:.6g}') for x in np.asarray(a).ravel()]
wout.write_text(json.dumps({
    'meta': {'layout': 'bm-feat-v1', 'dim': DIM, 'nmin': NMIN, 'nmax': NMAX, 'fps': 60, 'test': {k: {m_: round(v_[m_]['pos_cm'], 3) for m_ in ('linear', 'hermite', 'neural')} for k, v_ in report['test'].items()}},
    'in_mean': r6(in_mean), 'in_std': r6(in_std), 'res_std': r6(res_std),
    'layers': [{'nin': W.shape[1], 'nout': W.shape[0], 'W': r6(W), 'b': r6(b)} for W, b in params],
}))
qa = HERE / 'qa'
qa.mkdir(exist_ok=True)
(qa / 'neural_report.json').write_text(json.dumps(report, indent=1))
print('weights ->', wout.relative_to(ROOT), f'({wout.stat().st_size / 1e6:.2f} MB)')
