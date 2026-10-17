"""Soundtrack for the bonemotion demo reel, synthesised on the final timeline from build/bonemotion-demo/cues.json.

A soft vaudeville bed (tuba on 1 and 3, banjo on 2 and 4, a muted-trumpet theme now and then) under
foley that is placed on the exact frames the library reports: every bone of the assembly clacks
(pitch rising as the skeleton builds from the feet to the skull), footsteps and cane taps, pops,
whooshes on releases and take-offs, catches, bounces, the sling's swish per turn. Mixed to -16 LUFS.

usage: .venv/bin/python productions/bonemotion-demo/tools/soundtrack.py
"""
import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("hh", ROOT / "productions" / "halloween-hop" / "audio" / "score.py")
hh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hh)
SR = hh.SR
CUES = json.loads((ROOT / "build" / "bonemotion-demo" / "cues.json").read_text())
TOTAL = CUES["total"]
N = int(np.ceil(TOTAL * SR)) + SR
x = np.zeros(N)
cue_list, stems = [], {}
m, hz = hh.m, hh.hz
rng = np.random.default_rng(2611)


def add(t, sig, gain=1.0, cue=None):
    i = int(round(t * SR))
    if i < 0 or i >= N:
        return
    seg = sig[: N - i]
    x[i:i + len(seg)] += gain * seg
    if cue:
        cue_list.append({"id": cue, "t": round(t, 6), "frame": round(t * 60, 3)})
        stems[cue] = gain * sig[: int(0.25 * SR)]


# ---------------------------------------------------------------- the bed (quiet, it sits under the foley)
BPM = 120
spb = 60 / BPM
bars = [("D", [m("D2"), m("A1")], [m("D4"), m("F#4"), m("A4")]), ("G", [m("G2"), m("D2")], [m("D4"), m("G4"), m("B4")]),
        ("A", [m("A1"), m("E2")], [m("C#4"), m("E4"), m("A4")]), ("D", [m("D2"), m("A1")], [m("D4"), m("F#4"), m("A4")])]
for s in CUES["segments"]:
    t0, dur = s["t0"], s["dur"]
    nb = int((dur - 0.9) / (4 * spb))
    for b in range(nb):
        _, roots, chord = bars[b % 4]
        tb = t0 + 0.45 + b * 4 * spb
        add(tb, hh.tuba(hz(roots[0]), 0.9 * spb, 0.55), 0.55)
        add(tb + 2 * spb, hh.tuba(hz(roots[1]), 0.9 * spb, 0.5), 0.5)
        add(tb + spb, hh.banjo_strum(chord, 0.7 * spb, 0.5), 0.35)
        add(tb + 3 * spb, hh.banjo_strum(chord, 0.7 * spb, 0.5), 0.35)
    # a phrase of the theme on muted trumpet at the start of every other segment
    if int(s["num"]) % 2 == 1 and dur > 5:
        for b, d, nt in hh.THEME[:8]:
            tt = t0 + 0.6 + b * spb * 0.75
            if tt < t0 + dur - 1.2:
                add(tt, hh.trumpet(hz(m(nt) + 0), d * spb * 0.7, 0.6), 0.32)

# ---------------------------------------------------------------- foley on the reported frames
asm = [e for e in CUES["events"] if e["kind"] == "clack" and e["seg"] == "assemble"]
for k, e in enumerate(asm):
    # the build plays an ascending run: low (feet) to high (skull), small bones lighter
    f = 500 * 2 ** (2.2 * k / max(1, len(asm) - 1))
    add(e["t"], hh.woodblock(float(f * (1 + 0.04 * rng.uniform(-1, 1))), 0.55 if e.get("small") else 0.9), 0.32 if e.get("small") else 0.55,
        cue="asm-first" if k == 0 else ("asm-last" if k == len(asm) - 1 else None))
for e in CUES["events"]:
    t, k, sg = e["t"], e["kind"], e["seg"]
    if k == "clack" and sg == "assemble":
        continue
    if k == "step":
        add(t, hh.woodblock(float(rng.uniform(380, 460)), 0.6), 0.35)
    elif k == "cane":
        add(t, hh.woodblock(2100, 0.8), 0.45)
    elif k == "pop":
        add(t, hh.boing(220, 0.45), 0.9, cue=f"pop@{sg}")
        add(t, hh.woodblock(1500, 1.0), 0.6)
    elif k in ("release", "flick"):
        add(t - 0.08, hh.whoosh(0.22, up=True, vel=0.7), 0.7)
        add(t, hh.woodblock(1800, 0.7), 0.5, cue=f"release@{sg}")
    elif k == "whoosh":
        add(t - 0.05, hh.whoosh(0.3, up=True, vel=0.7), 0.7, cue=f"takeoff@{sg}")
    elif k in ("catch", "hatland", "land"):
        add(t, hh.thud(0.8), 0.7, cue=f"{k}@{sg}")
        add(t, hh.woodblock(900, 0.8), 0.45)
    elif k == "bounce":
        add(t, hh.thud(1.1), 0.9, cue=f"bounce@{sg}")
        add(t, hh.woodblock(700, 1.0), 0.6)
    elif k in ("click", "clack"):
        add(t, hh.woodblock(2300, 1.0), 0.7, cue=f"{k}@{sg}")
    elif k == "tug":
        add(t, hh.woodblock(800, 0.6), 0.45)
    elif k == "stomp":
        add(t, hh.thud(0.7), 0.6)
        add(t + 0.02, hh.slide_whistle(500, 1500, 0.5), 0.45, cue="stomp")
    elif k == "eyes":
        add(t, hh.triangle(0.8), 0.6, cue="eyes")
    elif k == "hop":
        add(t, hh.woodblock(520, 0.7), 0.5)
    elif k == "swish":
        add(t, hh.whoosh(0.16, up=False, vel=0.5), 0.45)
    elif k == "spinwhoosh":
        add(t, hh.whoosh(0.2, up=True, vel=min(1.0, 0.25 + e["w"] / 18)), 0.35)
    elif k == "sting":
        add(t, hh.celesta(hz(m("A5"))), 0.4)
        add(t + 0.15, hh.celesta(hz(m("D6"))), 0.4)

y = hh.period_chain(x[: int(TOTAL * SR)], crackle=False)
y = y / max(1e-9, np.abs(y).max()) * 0.5
out = ROOT / "build" / "bonemotion-demo" / "audio"
out.mkdir(parents=True, exist_ok=True)
g, hist = 1.0, []
for it in range(6):
    z, gr = hh.limiter(np.stack([y * g, y * g], axis=1), -2.0)
    hh.write_wav(out / "mix.wav", z)
    mm = hh.measure(out / "mix.wav")
    hist.append({"gain": g, **mm})
    err = -16.0 - mm["integrated_lufs"]
    if abs(err) <= 0.2:
        break
    g *= 10 ** (err / 20)
(out / "stems").mkdir(exist_ok=True)
for cid, sig in stems.items():
    s = np.zeros(int(0.25 * SR)); s[: len(sig)] = sig
    np.save(out / "stems" / f"{cid.replace('@', '_')}.npy", hh.period_chain(s, crackle=False))
(out / "cue_sheet.json").write_text(json.dumps({"cues": cue_list, "loudness": hist[-1]}, indent=1))
print(f"mix.wav: {TOTAL:.2f} s, {len(cue_list)} sync cues, loudness {hist[-1]}")
