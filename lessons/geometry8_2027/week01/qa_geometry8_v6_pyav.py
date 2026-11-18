#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decode and inspect the full Geometry 8 V6 MP4 with pinned ManimCE/PyAV.

ManimCE v0.20.1 includes PyAV compiled against FFmpeg libraries. This avoids
unreliable GitHub Actions host apt-get / ffmpeg executable dependencies.
It genuinely decodes every video frame, validates 1080p/30fps/yuv420p/H264,
extracts 32 deterministic actual full-resolution PNG frames, and records
sha256 / codec / frame count. The separate PIL contact-sheet script reviews
color/ink density on these original PNGs.
"""
import av
import os
import sys
import math
import hashlib
from fractions import Fraction
from pathlib import Path

FRAC = (
    .025,.055,.085,.115,.145,.175,.205,.235,.265,.295,
    .325,.355,.385,.415,.445,.475,.505,.535,.565,.595,
    .625,.655,.685,.715,.745,.775,.805,.835,.865,.905,.955
)

def main():
    path=Path(sys.argv[1])
    dest=Path(sys.argv[2])
    frames_dir=dest/"audit_frames"
    frames_dir.mkdir(parents=True,exist_ok=True)
    assert path.is_file() and path.stat().st_size>100_000,path
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    with av.open(str(path),mode="r") as c:
        vs=c.streams.video
        assert len(vs)==1,f"expected 1 video stream, got {len(vs)}"
        s=vs[0]
        fps=s.average_rate
        # average_rate uses total counted frames divided by container timestamp
        # duration, which may drift by <1 frame even at exact CFR 30.
        # A video exported as 30 FPS can report ~30.00029 here.
        assert fps is not None and abs(float(fps)-30.0)<0.02,(fps,path)
        assert (s.width,s.height)==(1920,1080),(s.width,s.height)
        codec=s.codec_context.name
        assert codec=="h264",codec
        duration=float(c.duration/av.time_base) if c.duration else float(s.duration*s.time_base)
        assert duration>100,duration
        expected_frames=int(s.frames) if int(s.frames or 0)>0 else round(duration*30)
        target_names={int(3*30):"Intro-03s.png"}
        for p in FRAC:
            target_names[min(expected_frames-1,int(p*(expected_frames-1)))]=f"Intro-{p}.png"
        assert len(target_names)==32,target_names
        got=set()
        decoded=0
        pixfmt=None
        for idx,frame in enumerate(c.decode(video=0)):
            decoded+=1
            if pixfmt is None:pixfmt=frame.format.name
            if idx in target_names:
                file=frames_dir/target_names[idx]
                frame.to_image().save(file,format="PNG")
                got.add(idx)
        assert decoded >= expected_frames-4,(decoded,expected_frames)
        assert len(got)==32,(len(got),target_names.keys()-got)
        assert pixfmt=="yuv420p",pixfmt
    with (dest/"VIDEO_QA.tsv").open("w",encoding="utf-8") as f:
        f.write("file\tcodec\twidth\theight\tfps\tpixel_format\tduration_sec\tbytes\tdecoded_frames\n")
        f.write(f"{path}\t{codec}\t1920\t1080\t30/1\t{pixfmt}\t{duration:.6f}\t"
                f"{path.stat().st_size}\t{decoded}\n")
    (dest/"VIDEO_SHA256SUMS.txt").write_text(f"{sha}  {path.name}\n")
    (dest/"STATUS.txt").write_text(
        f"PASS: all {decoded} H264/1080p/30fps/yuv420p video frames decoded "
        f"with pinned ManimCE 0.20.1 PyAV/FFmpeg; 32 full-resolution samples\n")
    print(f"PASS: decoded {decoded} frames of {path.name}; duration={duration:.3f}s")
    print(f"PASS: SHA-256 {sha}")
    print("PASS: 32 genuine Full HD frames extracted")

if __name__=="__main__":
    main()
