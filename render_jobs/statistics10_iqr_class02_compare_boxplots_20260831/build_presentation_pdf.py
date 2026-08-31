#!/usr/bin/env python3
"""Build a slide-like PDF from audited full-resolution video frames.

The workflow extracts 96 uniformly distributed frames from the final PQH MP4.
This script divides them into 16 timeline bins and selects the densest readable
frame from each bin (ink-density heuristic), avoiding blank transition frames.
The chosen frames are then placed one-per-page in a 16:9 PDF.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

PAGE_W = 13.333333 * 72
PAGE_H = 7.5 * 72


def ink_score(path: Path) -> float:
    img = Image.open(path).convert("L")
    img.thumbnail((480, 270))
    px = list(img.getdata())
    if not px:
        return 0.0
    dark = sum(v < 244 for v in px)
    very_dark = sum(v < 220 for v in px)
    return dark + 0.35 * very_dark


def choose_frames(paths: list[Path], count: int) -> list[Path]:
    if len(paths) < count:
        raise ValueError(f"Need at least {count} audit frames, got {len(paths)}")
    selected: list[Path] = []
    for i in range(count):
        start = round(i * len(paths) / count)
        end = round((i + 1) * len(paths) / count)
        chunk = paths[start:end]
        if not chunk:
            continue
        # Ignore the earliest candidate when possible; complete states usually
        # occur in the middle/later part of a scene segment.
        candidates = chunk[1:] if len(chunk) > 2 else chunk
        selected.append(max(candidates, key=ink_score))
    return selected


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audit_dir", type=Path)
    ap.add_argument("output_pdf", type=Path)
    ap.add_argument("cover_png", type=Path)
    ap.add_argument("selected_dir", type=Path)
    ap.add_argument("--pages", type=int, default=16)
    args = ap.parse_args()

    frames = sorted(args.audit_dir.glob("frame_*.png"))
    chosen = choose_frames(frames, args.pages)
    args.selected_dir.mkdir(parents=True, exist_ok=True)
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    args.cover_png.parent.mkdir(parents=True, exist_ok=True)

    selected_paths: list[Path] = []
    for idx, src in enumerate(chosen, start=1):
        dst = args.selected_dir / f"slide_{idx:02d}.png"
        shutil.copy2(src, dst)
        selected_paths.append(dst)

    shutil.copy2(selected_paths[0], args.cover_png)

    c = canvas.Canvas(str(args.output_pdf), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Statistics 10 - IQR & Box Plots - Class 2")
    c.setAuthor("Instituto Jorge Robledo")
    for path in selected_paths:
        c.drawImage(ImageReader(str(path)), 0, 0, width=PAGE_W, height=PAGE_H, preserveAspectRatio=True, anchor="c")
        c.showPage()
    c.save()


if __name__ == "__main__":
    main()
