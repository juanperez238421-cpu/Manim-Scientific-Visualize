#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, sys
job=Path(sys.argv[1])
parts=[p.read_text(encoding='ascii').strip() for p in sorted((job/'bootstrap').glob('v3_chunk_*.txt'))]
if not parts:
    raise SystemExit('No V3 chunks found')
encoded=''.join(parts)
raw=base64.b64decode(encoded, validate=True)
out=job/'stat10_normal_distribution_reviewed_v3.py'
out.write_bytes(gzip.decompress(raw))
print(f'decoded {out} ({out.stat().st_size} bytes) from {len(parts)} chunks')
