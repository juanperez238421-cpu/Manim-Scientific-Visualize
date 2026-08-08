#!/usr/bin/env python3
# Render loader for the reviewed Vector Calculus V2 suite.
# The expanded, human-readable sources are reconstructed from payload.b64 and
# are included verbatim in the final delivery package.
from __future__ import annotations
import base64
import gzip
from pathlib import Path

_payload = Path(__file__).with_name("payload.b64").read_text(encoding="utf-8").strip()
_source = gzip.decompress(base64.b64decode(_payload)).decode("utf-8")
exec(compile(_source, str(Path(__file__).with_name("expanded_all_scenes_v2.py")), "exec"), globals(), globals())
