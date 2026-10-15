import sys, glob
from PIL import Image
src, prefix = sys.argv[1], sys.argv[2]
fs = sorted(glob.glob(f"{src}/*.jpg"))
for k in range(0, len(fs), 6):
    ims = [Image.open(f) for f in fs[k:k + 6]]
    W, H = ims[0].size
    sheet = Image.new("RGB", (W * 2, H * 3), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * W, (i // 2) * H))
    sheet.save(f"{prefix}_{k // 6:02d}.jpg", quality=85)
print(len(fs))
