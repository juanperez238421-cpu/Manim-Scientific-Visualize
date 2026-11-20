#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys

path = sys.argv[1]
w, h = 320, 180
frame_bytes = w * h
proc = subprocess.Popen(
    [
        "ffmpeg", "-nostdin", "-loglevel", "error", "-i", path,
        "-vf", f"scale={w}:{h},format=gray",
        "-f", "rawvideo", "-pix_fmt", "gray", "-"
    ],
    stdout=subprocess.PIPE,
)

count = 0
violations = []
dark_ratios = []
blank_run = 0
max_blank_run = 0

while True:
    raw = proc.stdout.read(frame_bytes)
    if not raw:
        break
    if len(raw) != frame_bytes:
        raise SystemExit(f"partial frame {count}: {len(raw)} bytes")

    border = 0
    border_total = 0
    for y in (0, h - 1):
        row = raw[y*w:(y+1)*w]
        border += sum(px < 140 for px in row)
        border_total += len(row)
    for y in range(1, h - 1):
        for x in (0, w - 1):
            border += raw[y*w+x] < 140
            border_total += 1

    border_ratio = border / border_total
    if border_ratio > 0.004:
        violations.append({"frame": count, "border_dark_ratio": border_ratio})

    dark = sum(px < 170 for px in raw) / frame_bytes
    dark_ratios.append(dark)
    if dark < 0.0009:
        blank_run += 1
        max_blank_run = max(max_blank_run, blank_run)
    else:
        blank_run = 0
    count += 1

rc = proc.wait()
if rc != 0:
    raise SystemExit(f"ffmpeg scan failed: {rc}")
if count == 0:
    raise SystemExit("no frames decoded")

dark_sorted = sorted(dark_ratios)
report = {
    "frames_scanned": count,
    "border_violation_count": len(violations),
    "max_blank_run_frames": max_blank_run,
    "max_blank_run_seconds_at_30fps": max_blank_run / 30.0,
    "foreground_dark_ratio_median": dark_sorted[len(dark_sorted)//2],
    "foreground_dark_ratio_p95": dark_sorted[int(0.95 * (len(dark_sorted)-1))],
    "first_border_violations": violations[:20],
}
print(json.dumps(report, indent=2))

if violations:
    raise SystemExit(f"outer-border contact in {len(violations)} frames")
if max_blank_run > 60:
    raise SystemExit(f"blank transition longer than 2 s: {max_blank_run} frames")
