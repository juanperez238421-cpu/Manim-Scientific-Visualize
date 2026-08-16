#!/usr/bin/env python3
"""Canonical local render entrypoint for JP Manim Classroom Standard."""
from __future__ import annotations
import argparse, os, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(cmd,check=True):
    print("+"," ".join(map(str,cmd))); return subprocess.run(cmd,check=check)

def latest_video(scene):
    candidates=[p for p in (ROOT/"media").rglob(f"{scene}.mp4") if "partial_movie_files" not in p.parts]
    if not candidates: raise FileNotFoundError(f"No final MP4 found for {scene}")
    return max(candidates,key=lambda p:p.stat().st_mtime)

def main():
    p=argparse.ArgumentParser(); p.add_argument("source"); p.add_argument("scene")
    p.add_argument("--mode",choices=("preview","medium","final"),default="preview")
    p.add_argument("--headless",action="store_true",default=bool(os.getenv("CI")))
    p.add_argument("--no-cache",action="store_true"); p.add_argument("--flush-cache",action="store_true")
    p.add_argument("--seed",type=int,default=42); args=p.parse_args()
    source=Path(args.source).resolve()
    run([sys.executable,"-m","py_compile",str(source)])
    run([sys.executable,str(ROOT/"tools/check_style.py"),str(source)])
    if args.mode=="preview": quality="-ql" if args.headless else "-pql"; extra=[]
    elif args.mode=="medium": quality="-qm" if args.headless else "-pqm"; extra=[]
    else: quality="-qh" if args.headless else "-pqh"; extra=["--fps","30","-r","1920,1080","--format=mp4"]
    cmd=["manim",quality,str(source),args.scene,"--seed",str(args.seed),*extra]
    if args.no_cache: cmd.append("--disable_caching")
    if args.flush_cache: cmd.append("--flush_cache")
    run(cmd)
    video=latest_video(args.scene)
    mode="final" if args.mode=="final" else "preview"
    verify=[sys.executable,str(ROOT/"tools/verify_video.py"),str(video),"--scene",args.scene,"--mode",mode,"--source",str(source),"--output-dir",str(ROOT/"delivery"/args.scene)]
    run(verify); return 0

if __name__=="__main__": raise SystemExit(main())
