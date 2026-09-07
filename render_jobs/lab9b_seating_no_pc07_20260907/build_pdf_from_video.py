#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas

def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True).stdout.strip()

def duration(video):
    return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(video)]))

def frame(video, t, out):
    subprocess.run(['ffmpeg','-y','-ss',f'{t:.3f}','-i',str(video),'-frames:v','1','-vf','scale=1920:1080',str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('video', type=Path)
    p.add_argument('output_pdf', type=Path)
    p.add_argument('--frames-dir', type=Path, default=None)
    a=p.parse_args()
    video=a.video.resolve(); out=a.output_pdf.resolve(); d=duration(video)

    # Stable classroom moments only: cover, rules, room orientation, PC01-PC06,
    # assignment complete, final map, and final no-PC07 reminder.
    fractions=[0.040,0.150,0.290,0.380,0.450,0.520,0.590,0.660,0.735,0.850,0.930,0.985]
    times=[min(max(0.5,d*f),max(0.5,d-0.35)) for f in fractions]

    if a.frames_dir:
        fd=a.frames_dir.resolve(); fd.mkdir(parents=True,exist_ok=True); cleanup=False
    else:
        fd=Path(tempfile.mkdtemp(prefix='pdf_frames_')); cleanup=True

    files=[]
    for i,t in enumerate(times,1):
        f=fd/f'page_{i:02d}_{t:06.2f}s.png'
        frame(video,t,f)
        files.append(f)

    out.parent.mkdir(parents=True,exist_ok=True)
    pdf=canvas.Canvas(str(out),pagesize=(960,540))
    for f in files:
        with Image.open(f) as im:
            if im.width < 1280 or im.height < 720:
                raise RuntimeError(f'Unexpected frame size {im.size}')
        pdf.drawImage(str(f),0,0,width=960,height=540,preserveAspectRatio=True,anchor='c',mask='auto')
        pdf.showPage()
    pdf.save()

    if cleanup:
        shutil.rmtree(fd,ignore_errors=True)
    print(f'PDF={out}')
    print(f'PAGES={len(files)}')
    print(f'VIDEO_DURATION={d:.6f}')

if __name__=='__main__':
    main()
