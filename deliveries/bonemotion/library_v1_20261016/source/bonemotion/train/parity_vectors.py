"""Fixed inputs -> network outputs computed in numpy from the exported weights (the JS QA must match them)."""
import json
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parents[1]
W = json.loads((HERE / 'src/neural/weights/inbetween_v1.json').read_text())
rng = np.random.default_rng(5)
xm, xs, rs = (np.array(W[k]) for k in ('in_mean', 'in_std', 'res_std'))
out = []
for k in range(8):
    x = xm + xs * rng.normal(0, 0.7, size=xm.shape)
    h = (x - xm) / xs
    for i, L in enumerate(W['layers']):
        Wm = np.array(L['W']).reshape(L['nout'], L['nin']); b = np.array(L['b'])
        z = Wm @ h + b
        h = np.where(z > 0, z, np.expm1(np.minimum(z, 0))) if i < len(W['layers']) - 1 else z
    out.append({'x': x.tolist(), 'y': (h * rs).tolist()})
(HERE / 'qa/parity_vectors.json').write_text(json.dumps(out))
print('8 parity vectors written')
