#!/usr/bin/env python3
"""Verify 16 real Full HD frames from a ManimCE Week02–04 class.

PNG parse, 1920x1080, non-empty screen sample, dimensions and contact sheet.
The manifest is auditable; no OCR or unsupported zero-overlap guarantee.
"""
from __future__ import annotations
import argparse, csv
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageStat, ImageFont


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("frames",type=Path)
    ap.add_argument("out",type=Path)
    ap.add_argument("--slug",required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    files=sorted(args.frames.glob(f"{args.slug}-*.png"))
    if len(files)!=16:
        raise ValueError(f"{args.slug}: expected 16 frames, received {len(files)}")
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",19)
    except OSError: font=ImageFont.load_default()
    sheet=Image.new("RGB",(2200,1600),"#F7F9FB")
    draw=ImageDraw.Draw(sheet)
    rows=[];ink=[]
    for n,file in enumerate(files):
        with Image.open(file) as obj: obj.verify()
        with Image.open(file) as obj:
            im=obj.convert("RGB")
            if im.size!=(1920,1080):
                raise ValueError(f"{file.name} has incorrect size {im.size}")
            sample=im.resize((192,108),Image.Resampling.LANCZOS)
            pixels=list(sample.getdata())
            nonwhite=sum(1 for p in pixels if min(p)<231)
            mean=sum(ImageStat.Stat(sample).mean)/3
            rows.append(dict(frame=file.name,full_width=1920,
                full_height=1080,ink_pixels=nonwhite,mean_rgb=round(mean,2)))
            ink.append(nonwhite)
            x=(n%4)*550+12;y=(n//4)*398+39
            thumb=ImageOps.contain(im,(527,297),Image.Resampling.LANCZOS)
            sheet.paste(thumb,(x,y))
            draw.text((x+2,y-28),file.name,fill="#2B4252",font=font)
            draw.rectangle((x-4,y-4,x+534,y+301),
                           outline="#C7CFD9",width=2)
    if sum(i>130 for i in ink)<8:
        raise ValueError(f"{args.slug}: too many blank chapter samples")
    cover=next((r for r in rows if r["frame"]==f"{args.slug}-03s.png"),None)
    if cover is None or cover["ink_pixels"]<100:
        raise ValueError(f"{args.slug}: cover PNG unexpectedly blank")
    path=args.out/f"{args.slug}_contact.jpg"
    sheet.save(path,quality=89,optimize=True,subsampling=0)
    with (args.out/f"{args.slug}_FRAME_METRICS.csv").open("w",newline="") as stream:
        w=csv.DictWriter(stream,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    print("PASS",args.slug,"16 actual Full HD PNGs and",path)


if __name__=="__main__": main()
