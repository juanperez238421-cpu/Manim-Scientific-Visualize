from pathlib import Path
import base64
import zlib

ROOT = Path(__file__).resolve().parent
payload = "".join(
    (ROOT / "compact_parts" / f"part_{index:02d}.txt").read_text(encoding="utf-8")
    for index in range(2)
)
source = zlib.decompress(base64.b64decode(payload)).decode("utf-8")
exec(compile(source, str(ROOT / "visual_html_v6_compact_source.py"), "exec"), globals())
