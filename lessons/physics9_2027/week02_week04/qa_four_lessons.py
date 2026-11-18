#!/usr/bin/env python3
"""Visual QA for four real, final 1080p teaching videos (9 frames per video)."""
import csv,sys
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageStat,ImageFont

CLASS_MAP={
    "W02C01":"Week02_V1_Class01",
    "W02C02":"Week02_V1_Class02",
    "W04C01":"Week04_V1_Class01",
    "W04C02":"Week04_V1_Class02",
}
def main():
    source,target=Path(sys.argv[1]),Path(sys.argv[2])
    try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
    except OSError:font=ImageFont.load_default()
    metrics=[]
    for code,stem in CLASS_MAP.items():
        files=sorted(source.glob(code+"-*.png"))
        if len(files)!=9:raise RuntimeError(f"{code}: expected exactly nine PNG frames; got {len(files)}")
        sheet=Image.new("RGB",(1620,1050),"#F7F9FA")
        draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(files):
            with Image.open(p) as image:image.verify()
            with Image.open(p) as image:
                im=image.convert("RGB")
                if im.size!=(1920,1080):raise ValueError(f"Wrong frame size: {p} {im.size}")
                sample=im.resize((160,90))
                ink=sum(1 for r,g,b in sample.getdata() if min(r,g,b)<225)
                means=ImageStat.Stat(sample).mean
                if p.name.endswith("-03s.png") and ink<55:
                    raise RuntimeError("Missing original institutional cover: "+p.name)
                x=(i%3)*540+7;y=(i//3)*350+30
                sheet.paste(ImageOps.contain(im,(526,296)),(x,y))
                draw.rectangle((x-2,y-2,x+527,y+299),outline="#CBD4D8",width=2)
                draw.text((x+8,y-22),p.name,fill="#263746",font=font)
                metrics.append({"class":code,"frame":p.name,
                                "ink_pixels":ink,"mean_luma":round(sum(means)/3,2)})
        out=target/f"Physics9_2027_{stem}_contact.jpg"
        sheet.save(out,quality=89,optimize=True)
        print("PASS",code,len(files),"frames",str(out))
    with (target/"FRAME_METRICS.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["class","frame","ink_pixels","mean_luma"])
        writer.writeheader();writer.writerows(metrics)
if __name__=="__main__":main()
