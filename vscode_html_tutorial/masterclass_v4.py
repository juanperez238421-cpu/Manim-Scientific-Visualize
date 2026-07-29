"""Loader for the senior-reviewed VS Code and GitHub masterclass scenes."""
from pathlib import Path
import base64
import zlib

ROOT = Path(__file__).resolve().parent
payload = "".join(
    (ROOT / "masterclass_v4_parts" / f"part_{index:02d}.txt").read_text(encoding="utf-8")
    for index in range(7)
)
source = zlib.decompress(base64.b64decode(payload)).decode("utf-8")
exec(compile(source, str(ROOT / "masterclass_v4_source.py"), "exec"), globals())
