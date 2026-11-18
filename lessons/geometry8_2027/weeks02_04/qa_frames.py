#!/usr/bin/env python3
"""Visual QA for each 2027 Grade 8 CAD MP4: nine original 1080p frames.

Produces a real frame contact sheet + numeric frame information.
Visual inspection is sampled, not universal proof of zero overlap.
"""
import sys,csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat, ImageOps, ImageFont

def main():
    folder=Path(sys.argv[1]);target=Path(sys.argv[2]);scene=sys.argv[3]
    frames=sorted(folder.glob("frame*.png"))
    if len(frames)!=9: raise ValueError(f"Expected 9 original frames, got {len(frames)}")
    sheet=Image.new("RGB",(1780,1040),"#F7F9FB")
    draw=ImageDraw.Draw(sheet)
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",17)
    except OSError:font=ImageFont.load_default()
    metrics=[]
    for i,f in enumerate(frames):
        with Image.open(f) as raw:raw.verify()
        with Image.open(f) as raw:
            im=raw.convert("RGB")
            if im.size!=(1920,1080):raise ValueError((str(f),im.size))
            thumb=ImageOps.contain(im,(564,318),Image.Resampling.LANCZOS)
            x=(i%3)*593+14;y=(i//3)*345+25
            sheet.paste(thumb,(x,y))
            draw.text((x,y-20),f.name,fill="#1B2533",font=font)
            low=im.resize((192,108),Image.Resampling.LANCZOS)
            nonwhite=sum(1 for rgb in low.getdata() if min(rgb)<230)
            metrics.append([f.name,im.width,im.height,nonwhite])
    if sum(row[3]>100 for row in metrics)<4:
        raise ValueError("Too many near-white frames; video may be blank")
    sheet.save(target/"contact.jpg",quality=91,subsampling=0,optimize=True)
    with (target/"frame_metrics.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["frame","width","height","dark_pixels_192x108"])
        w.writerows(metrics)
    print("PASS:",scene,"9 real Full HD frames and nonempty contact sheet")

if __name__=="__main__":main()
