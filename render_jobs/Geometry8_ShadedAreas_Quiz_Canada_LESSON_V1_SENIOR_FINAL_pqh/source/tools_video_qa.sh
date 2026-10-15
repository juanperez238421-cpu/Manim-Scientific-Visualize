#!/bin/bash
# Gates D + E: technical QA, SHA-256, share copy, contact sheet, event stills.
# usage: tools_video_qa.sh <rendered.mp4> <FINAL_NAME> <events.txt> <outdir>
set -euo pipefail
SRC=$1; NAME=$2; EVENTS=$3; OUT=$4
PY=/tmp/claude-0/-home-claude/4fb7dad8-3eac-55ff-8674-75a699e3adfa/scratchpad/venv/bin/python
mkdir -p "$OUT/stills" "$OUT/sheet_frames"
FINAL="$OUT/$NAME.mp4"; SHARE="$OUT/${NAME}_share.mp4"
cp "$SRC" "$FINAL"

QA="$OUT/${NAME}_VIDEO_QA.txt"
{
  echo "VIDEO QA — $NAME.mp4"
  echo "protocols: HYBRID-SCIANIM-v1 (LESSON style) + MANIMCE-PQH-DIRECT-GITHUB-v1 gates D/E"
  echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "== ffprobe =="
  ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames \
          -show_entries format=duration,size -of default=nw=1 "$FINAL"
} > "$QA"

DEC=$(ffmpeg -v error -i "$FINAL" -f null - 2>&1 | grep -v -i "timestamp" | wc -l || true)
echo "full decode errors: $DEC" >> "$QA"

# share copy < 30 MB (CRF ladder)
for crf in 23 25 27 29; do
  ffmpeg -nostdin -v error -y -i "$FINAL" -c:v libx264 -preset slow -crf $crf -pix_fmt yuv420p \
         -r 30 -movflags +faststart -an "$SHARE"
  sz=$(stat -c %s "$SHARE")
  if [ "$sz" -lt 30000000 ]; then echo "share copy: crf $crf, $sz bytes" >> "$QA"; break; fi
done

# contact sheet: one frame every 5 s
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL")
rm -f "$OUT"/sheet_frames/*.jpg
ffmpeg -nostdin -v error -i "$FINAL" -vf "fps=1/5,scale=384:-1" "$OUT/sheet_frames/s_%04d.jpg"
$PY - "$OUT/sheet_frames" "$OUT/${NAME}_contact_sheet.jpg" <<'EOF'
import sys, glob
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + "/*.jpg"))
ims = [Image.open(f) for f in fs]
W, H = ims[0].size
cols = 10
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, (H + 18) * rows), "white")
d = ImageDraw.Draw(sheet)
for i, im in enumerate(ims):
    x, y = (i % cols) * W, (i // cols) * (H + 18)
    sheet.paste(im, (x, y + 18))
    d.text((x + 4, y + 2), f"t={i * 5}s", fill=(0, 0, 0))
    d.rectangle([x, y + 18, x + W - 1, y + 18 + H - 1], outline=(200, 200, 200))
sheet.save(sys.argv[2], quality=88)
print(len(ims), "frames")
EOF
echo "contact sheet: one frame / 5 s" >> "$QA"

# event stills (frame-exact teaching states)
rm -f "$OUT"/stills/*.jpg
while IFS='|' read -r p s t; do
  ffmpeg -nostdin -v error -y -ss "$t" -i "$FINAL" -frames:v 1 -vf scale=960:-1 \
         "$OUT/stills/$(printf "%07.2f" "$t")_${p}_${s}.jpg"
done < "$EVENTS"
echo "event stills: $(ls "$OUT"/stills | wc -l)" >> "$QA"

( cd "$OUT" && sha256sum "$NAME.mp4" "${NAME}_share.mp4" > "${NAME}_SHA256SUMS.txt" )
echo >> "$QA"; echo "== SHA-256 ==" >> "$QA"; cat "$OUT/${NAME}_SHA256SUMS.txt" >> "$QA"
cat "$QA"
