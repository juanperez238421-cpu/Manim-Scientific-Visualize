"""Loader for the senior-revised CSS + HTML V6 Manim scene."""
from pathlib import Path
import base64
import zlib

ROOT = Path(__file__).resolve().parent
payload = (ROOT / "parts" / "source.part_00").read_text(encoding="utf-8")
source = zlib.decompress(base64.b64decode(payload)).decode("utf-8")
exec(compile(source, str(ROOT / "css_html_masterclass_v6_source.py"), "exec"), globals())
