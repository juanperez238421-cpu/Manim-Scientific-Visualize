#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, sys
job=Path(sys.argv[1])
payload=job/'bootstrap'/'source.py.gz.b64'
out=job/'stat10_normal_distribution_class1_detailed_v2.py'
out.write_bytes(gzip.decompress(base64.b64decode(payload.read_text(encoding='ascii'))))
print(out, out.stat().st_size)
