#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, sys
job = Path(sys.argv[1])
b64 = job / "bootstrap" / "v3_append.pyfrag.gz.b64"
frag = gzip.decompress(base64.b64decode(b64.read_text(encoding="ascii"), validate=True)).decode("utf-8")
base = job / "stat10_normal_distribution_class1_detailed_v2.py"
out = job / "stat10_normal_distribution_class1_detailed_v3.py"
out.write_text(base.read_text(encoding="utf-8") + frag, encoding="utf-8")
print(out, out.stat().st_size)
