"""contact sheet: python tools/sheet.py video.mp4 out.png t1,t2,... [cols] [tile_w]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pdf2video.tools_sheet import sheet  # noqa: E402

if __name__ == "__main__":
    sheet(sys.argv[1], [float(x) for x in sys.argv[3].split(",")], sys.argv[2], int(sys.argv[4]) if len(sys.argv) > 4 else 4, int(sys.argv[5]) if len(sys.argv) > 5 else 480)
