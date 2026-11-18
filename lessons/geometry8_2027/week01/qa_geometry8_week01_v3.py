#!/usr/bin/env python3
"""Geometry8 2027 W01 V2: 16 real final-PQH image samples + metrics.

Checks: exists, complete PNG parse, exact 1920x1080, non-empty cover,
no overall blank chapter distribution, inspectable 4x4 contact sheets.
No OCR and no unsupported universal overlap-free claim.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageStat, ImageFont
import csv,sys

def main():
    src,dst=Path(sys.argv[1]),Path(sys.argv[2])
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",19)
    except OSError: font=ImageFont.load_default()
    metrics=[]
    for cls in ("Class01",):
        images=sorted(src.glob(cls+"-*.png"))
        if len(images)!=16:
            raise RuntimeError(f"{cls}: 16 sampled video frames required, got {len(images)}")
        sheet=Image.new("RGB",(2200,1600),"#F7F9FB")
        draw=ImageDraw.Draw(sheet)
        ink_list=[]
        for idx,file in enumerate(images):
            with Image.open(file) as x: x.verify()
            with Image.open(file) as x:
                im=x.convert("RGB")
                if im.size!=(1920,1080):
                    raise ValueError((file.name,im.size))
                sm=im.resize((192,108),Image.Resampling.LANCZOS)
                ink=sum(1 for pix in sm.getdata() if min(pix)<232)
                mean=ImageStat.Stat(sm).mean
                ink_list.append(ink)
                metrics.append({
                    "class":cls,
                    "frame":file.name,
                    "sample_ink_pixels":ink,
                    "mean_rgb":round(sum(mean)/3,2)
                })
                x=(idx%4)*550+11; y=(idx//4)*398+36
                thumb=ImageOps.contain(im,(527,297),Image.Resampling.LANCZOS)
                sheet.paste(thumb,(x,y))
                draw.text((x+3,y-27),file.name,fill="#273B48",font=font)
                draw.rectangle((x-4,y-4,x+533,y+301),
                               outline="#C7D1D7",width=2)
        opening=next((row for row in metrics if row["frame"]==cls+"-03s.png"),None)
        if opening is None or opening["sample_ink_pixels"]<90:
            raise ValueError(f"{cls}: real PNG school crest opening was empty")
        if sum(i>140 for i in ink_list)<8:
            raise ValueError(f"{cls}: too many nearly blank chapter samples")
        dest=dst/f"Geometry8_2027_Week01_V3_{cls}_contact.jpg"
        sheet.save(dest,quality=90,optimize=True,subsampling=0)
        print("PASS:",cls,"16 full-HD frames, contact sheet",dest)
    with (dst/"FRAME_METRICS.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=metrics[0].keys())
        writer.writeheader()
        writer.writerows(metrics)

if __name__=="__main__":
    main()
