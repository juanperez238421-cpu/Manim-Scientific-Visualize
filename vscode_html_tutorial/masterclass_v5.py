"""Loader for V5 HTML, GitHub, and CSS masterclasses."""
from pathlib import Path
import base64
import zlib
ROOT = Path(__file__).resolve().parent
payload = "".join((ROOT / "masterclass_v5_parts" / f"part_{index:02d}.txt").read_text(encoding="utf-8") for index in range(2))
source = zlib.decompress(base64.b64decode(payload)).decode("utf-8")
exec(compile(source, str(ROOT / "masterclass_v5_source.py"), "exec"), globals())
# Compatibility alias used by the CSS triptych animation.
CENTER = ORIGIN
