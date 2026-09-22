#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, sys
job=Path(sys.argv[1])
files=sorted((job/'bootstrap').glob('v3s_*.txt'))
if not files:
    raise SystemExit('No safe V3 chunks found')
parts=[p.read_text(encoding='ascii').strip() for p in files]
encoded=''.join(parts)
print('payload chars:', len(encoded), 'files:', len(files))
raw=base64.b64decode(encoded, validate=True)
out=job/'stat10_normal_distribution_reviewed_v3.py'
out.write_bytes(gzip.decompress(raw))
print(f'decoded {out} ({out.stat().st_size} bytes)')
