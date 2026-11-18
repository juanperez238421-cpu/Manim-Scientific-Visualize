#!/usr/bin/env python3
"""Validate sampled PNG frames and build a 3x3 inspection contact sheet per class."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageStat, ImageFont
import csv,sys

def main():
    source,target=Path(sys.argv[1]),Path(sys.argv[2])
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
    except OSError: font=ImageFont.load_default()
    metrics=[]
    for klass in ("Class01",):
        files=sorted(source.glob(klass+"-*.png"))
        if len(files)!=9: raise RuntimeError(f"{klass}: expected 9 frames, got {len(files)}")
        sheet=Image.new("RGB",(1620,1050),"#F7F9FA"); draw=ImageDraw.Draw(sheet)
        for i,filename in enumerate(files):
            with Image.open(filename) as raw: raw.verify()
            with Image.open(filename) as raw:
                im=raw.convert("RGB")
                assert im.size==(1920,1080),(filename,im.size)
                sample=im.resize((160,90))
                ink=sum(1 for r,g,b in sample.getdata() if min(r,g,b)<225)
                mean=ImageStat.Stat(sample).mean
                metrics.append({"class":klass,"frame":filename.name,
                                "ink_pixels":ink,"mean_luma":round(sum(mean)/3,2)})
                if filename.name.endswith("-03s.png") and ink<55:
                    raise RuntimeError("Blank institutional cover: "+filename.name)
                x=(i%3)*540+7; y=(i//3)*350+30
                sheet.paste(ImageOps.contain(im,(526,296)),(x,y))
                draw.text((x+8,y-22),filename.name,fill="#263746",font=font)
                draw.rectangle((x-2,y-2,x+527,y+299),outline="#CBD4D8",width=2)
        output=target/f"Physics9_2027_Week01_V5_{klass}_contact.jpg"
        sheet.save(output,quality=88,optimize=True)
        print("Contact sheet",output)
    with (target/"FRAME_METRICS.csv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=["class","frame","ink_pixels","mean_luma"])
        writer.writeheader();writer.writerows(metrics)

if __name__=="__main__": main()
