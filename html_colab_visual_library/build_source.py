from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "parts"
TARGET = ROOT / "html_colab_visual_library.py"

chunks = []
for path in sorted(PARTS.glob("html_colab_visual_library.part_*")):
    chunks.append(path.read_text(encoding="utf-8"))

if not chunks:
    raise SystemExit("No source parts were found.")

TARGET.write_text("".join(chunks), encoding="utf-8")
print(f"Built {TARGET} from {len(chunks)} parts.")
