#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageStat
from reportlab.pdfgen import canvas


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True).stdout.strip()


def duration(video: Path) -> float:
    return float(run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video)
    ]))


def extract(video: Path, t: float, out: Path) -> None:
    subprocess.run([
        "ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(video),
        "-frames:v", "1", "-vf", "scale=1920:1080", str(out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def motion_score(a: Path, b: Path) -> float:
    with Image.open(a).convert("L") as ia, Image.open(b).convert("L") as ib:
        diff = ImageChops.difference(ia, ib)
        return float(ImageStat.Stat(diff).mean[0])


def choose_stable_time(video: Path, center: float, d: float, work: Path, idx: int) -> float:
    offsets = (-1.50, -1.00, -0.55, -0.20, 0.15, 0.55, 1.00, 1.50)
    best = None
    for j, off in enumerate(offsets):
        t = min(max(0.60, center + off), max(0.60, d - 0.70))
        a = work / f"probe_{idx:02d}_{j:02d}_a.png"
        b = work / f"probe_{idx:02d}_{j:02d}_b.png"
        extract(video, t, a)
        extract(video, min(t + 0.28, d - 0.20), b)
        score = motion_score(a, b)
        candidate = (score, abs(off), t)
        if best is None or candidate < best:
            best = candidate
    assert best is not None
    return best[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument("--frames-dir", type=Path, default=None)
    args = parser.parse_args()

    video = args.video.resolve()
    output = args.output_pdf.resolve()
    d = duration(video)
    targets = [0.035, 0.105, 0.175, 0.250, 0.325, 0.405, 0.485,
               0.565, 0.645, 0.720, 0.790, 0.855, 0.920, 0.975]

    if args.frames_dir:
        frames_dir = args.frames_dir.resolve()
        frames_dir.mkdir(parents=True, exist_ok=True)
        cleanup_frames = False
    else:
        frames_dir = Path(tempfile.mkdtemp(prefix="lab9c_pdf_frames_"))
        cleanup_frames = True

    work = Path(tempfile.mkdtemp(prefix="lab9c_pdf_probe_"))
    chosen = []
    files = []
    try:
        for i, frac in enumerate(targets, 1):
            center = d * frac
            t = choose_stable_time(video, center, d, work, i)
            chosen.append(t)
            frame = frames_dir / f"page_{i:02d}_{t:06.2f}s.png"
            extract(video, t, frame)
            with Image.open(frame) as im:
                if im.width < 1280 or im.height < 720:
                    raise RuntimeError(f"Unexpected frame size {im.size}")
            files.append(frame)

        output.parent.mkdir(parents=True, exist_ok=True)
        pdf = canvas.Canvas(str(output), pagesize=(960, 540))
        for frame in files:
            pdf.drawImage(str(frame), 0, 0, width=960, height=540,
                          preserveAspectRatio=True, anchor="c", mask="auto")
            pdf.showPage()
        pdf.save()

        print(f"PDF={output}")
        print(f"PAGES={len(files)}")
        print(f"VIDEO_DURATION={d:.6f}")
        print("CHOSEN_TIMES=" + ",".join(f"{t:.3f}" for t in chosen))
    finally:
        shutil.rmtree(work, ignore_errors=True)
        if cleanup_frames:
            shutil.rmtree(frames_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
