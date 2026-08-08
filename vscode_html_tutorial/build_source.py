from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "parts"
TARGET = ROOT / "vscode_html_tutorial.py"

chunks = []
for path in sorted(PARTS.glob("vscode_html_tutorial.part_*")):
    chunks.append(path.read_text(encoding="utf-8"))

if not chunks:
    raise SystemExit("No source parts found.")

source = "".join(chunks)
duplicate = (
    "            stroke_color=LINE,\n"
    "            stroke_width=1,\n"
    "        ).next_to(activity, RIGHT, buff=0).align_to(activity, UP)\n"
    "            stroke_color=LINE,\n"
    "            stroke_width=1,\n"
    "        ).next_to(activity, RIGHT, buff=0).align_to(activity, UP)\n"
)
source = source.replace(
    duplicate,
    "            stroke_color=LINE,\n"
    "            stroke_width=1,\n"
    "        ).next_to(activity, RIGHT, buff=0).align_to(activity, UP)\n",
)
TARGET.write_text(source, encoding="utf-8")
print(f"Built {TARGET} from {len(chunks)} parts.")
