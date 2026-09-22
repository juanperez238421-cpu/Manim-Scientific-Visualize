#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, sys
job=Path(sys.argv[1])
parts=[]
for p in sorted((job/'bootstrap').glob('chunk_*.txt')):
    parts.append(p.read_text(encoding='ascii').strip())
if not parts:
    raise SystemExit('no source chunks found')
encoded=''.join(parts)
raw=base64.b64decode(encoded, validate=True)
out=job/'stat10_normal_distribution_class1_detailed_v2.py'
out.write_bytes(gzip.decompress(raw))
print(out, out.stat().st_size, 'bytes from', len(parts), 'chunks')
