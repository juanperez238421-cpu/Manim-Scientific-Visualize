#!/usr/bin/env python3
from __future__ import annotations
import base64
import io
from pathlib import Path
import sys
import tarfile
import zlib

job = Path(sys.argv[1]).resolve()
bootstrap = job / "bootstrap"

def decode_zlib(name: str, output: str) -> None:
    payload = (bootstrap / name).read_text(encoding="ascii").strip()
    (job / output).write_bytes(zlib.decompress(base64.b64decode(payload)))

decode_zlib("source.zlib.b64", "Statistics10_IQR_Class02_Compare_Boxplots_FINAL.py")
decode_zlib("style.zlib.b64", "jp_classroom_style.py")
archive = base64.b64decode((bootstrap / "misc.tgz.b64").read_text(encoding="ascii").strip())
with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tf:
    tf.extractall(job)
print("BOOTSTRAP_OK")
