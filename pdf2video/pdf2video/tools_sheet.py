"""contact sheet: python tools/sheet.py video.mp4 out.png t1,t2,... [cols] [tile_w]"""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

def sheet(video, times, out, cols=4, tile_w=480):
    tiles = []
    with tempfile.TemporaryDirectory() as d:
        for i, t in enumerate(times):
            p = Path(d) / f"{i}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={tile_w}:-1", str(p)], check=True)
            im = Image.open(p).convert("RGB"); ImageDraw.Draw(im).text((6, 4), f"{t:.1f}s", fill=(200, 0, 0)); tiles.append(im)
    w, h = tiles[0].size; rows = (len(tiles) + cols - 1) // cols
    S = Image.new("RGB", (cols * w + (cols + 1) * 4, rows * h + (rows + 1) * 4), (90, 90, 90))
    for i, im in enumerate(tiles):
        S.paste(im, (4 + (i % cols) * (w + 4), 4 + (i // cols) * (h + 4)))
    S.save(out)

if __name__ == "__main__":
    sheet(sys.argv[1], [float(x) for x in sys.argv[3].split(",")], sys.argv[2], int(sys.argv[4]) if len(sys.argv) > 4 else 4, int(sys.argv[5]) if len(sys.argv) > 5 else 480)
