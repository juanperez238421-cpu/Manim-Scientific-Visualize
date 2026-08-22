#!/usr/bin/env python3
"""Verify a Manim MP4 and create an auditable delivery package."""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path

def call_json(cmd):
    proc=subprocess.run(cmd,check=True,text=True,stdout=subprocess.PIPE); return json.loads(proc.stdout)

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def fps(rate):
    if "/" in rate:
        a,b=rate.split("/",1); return float(a)/float(b)
    return float(rate)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("video"); parser.add_argument("--scene",required=True)
    parser.add_argument("--mode",choices=("preview","final"),required=True); parser.add_argument("--source")
    parser.add_argument("--output-dir",required=True); parser.add_argument("--git-sha"); args=parser.parse_args()
    video=Path(args.video)
    if not video.is_file() or video.stat().st_size<=0: raise FileNotFoundError(f"Invalid MP4: {video}")
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"): raise RuntimeError("ffprobe and ffmpeg are required")
    meta=call_json(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(video)])
    stream=next((s for s in meta.get("streams",[]) if s.get("codec_type")=="video"),None)
    if not stream: raise RuntimeError("No video stream found")
    duration=float(meta.get("format",{}).get("duration") or 0)
    if duration<=0: raise RuntimeError(f"Invalid duration: {duration}")
    if args.mode=="final":
        dims=(int(stream.get("width",0)),int(stream.get("height",0)))
        rate=stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1"
        if dims!=(1920,1080): raise RuntimeError(f"Expected 1920x1080, got {dims[0]}x{dims[1]}")
        if abs(fps(rate)-30.0)>0.05: raise RuntimeError(f"Expected 30 fps, got {fps(rate)}")
        if stream.get("codec_name")!="h264": raise RuntimeError(f"Expected H.264, got {stream.get('codec_name')}")
        if stream.get("pix_fmt")!="yuv420p": raise RuntimeError(f"Expected yuv420p, got {stream.get('pix_fmt')}")
    subprocess.run(["ffmpeg","-v","error","-i",str(video),"-f","null","-"],check=True)
    out=Path(args.output_dir); frames=out/"qa_frames"; frames.mkdir(parents=True,exist_ok=True)
    staged=out/f"{args.scene}_{args.mode}.mp4"; shutil.copy2(video,staged)
    if args.source and Path(args.source).is_file(): shutil.copy2(args.source,out/Path(args.source).name)
    digest=sha256(staged)
    (out/"ffprobe.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    (out/"SHA256SUMS.txt").write_text(f"{digest}  {staged.name}\n",encoding="utf-8")
    (out/"render_metadata.json").write_text(json.dumps({"standard_version":"1.0.0","manim_target":"0.20.1","scene":args.scene,"mode":args.mode,"source":args.source,"git_sha":args.git_sha,"created_utc":datetime.now(timezone.utc).isoformat(),"sha256":digest,"duration_seconds":duration},indent=2),encoding="utf-8")
    for index,pct in enumerate((0.05,0.25,0.50,0.75,0.95),start=1):
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{duration*pct:.6f}","-i",str(video),"-frames:v","1",str(frames/f"qa_{index:02d}.png")],check=True)
    print(json.dumps({"video":str(staged),"sha256":digest,"duration":duration},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
