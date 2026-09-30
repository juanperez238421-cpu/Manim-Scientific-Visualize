#!/usr/bin/env bash
set -euo pipefail
JOB=render_jobs/openai_asset_demo_20260815
STYLEJOB=render_jobs/valentina_workshop_20260813
SCENE=OpenAIAssetDemo
mkdir -p assets/images delivery qa
cp "$JOB/demo_short.py" main.py
cat "$STYLEJOB"/s_*.b64 | base64 -d | gzip -dc > jp_classroom_style.py
cat "$JOB"/ap_0[0-8] | base64 -d > assets/images/openai_inclined_plane.webp
echo '3f3f06e94d5cad870ad335502cc1a93e56ce675abb1231ded5f9c71fd3e60e3d  jp_classroom_style.py' | sha256sum -c -
echo 'ee660f75cc495e6c11d8e426c6d971aedfab774a258ca99901f13333f676f43d  assets/images/openai_inclined_plane.webp' | sha256sum -c -
python -m py_compile main.py jp_classroom_style.py
sha256sum main.py jp_classroom_style.py assets/images/openai_inclined_plane.webp > SOURCE_SHA256.txt
command -v ffprobe >/dev/null || { sudo apt-get update -qq; sudo apt-get install -y -qq ffmpeg; }
docker pull manimcommunity/manim:v0.20.1 >/dev/null
render(){
 q="$1"; scale="$2"; log="$3"; rm -rf media
 docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home -e LESSON_TIME_SCALE="$scale" \
  -v "$PWD:/manim" -w /manim --entrypoint bash manimcommunity/manim:v0.20.1 -c "
   set -euo pipefail; mkdir -p /tmp/bin
   printf '#!/usr/bin/env bash\nexit 0\n' >/tmp/bin/xdg-open; chmod +x /tmp/bin/xdg-open
   export PATH=/tmp/bin:\$PATH
   manim $q main.py $SCENE --format=mp4 --disable_caching
  " 2>&1 | tee "$log"
}
render -pql .12 preview.log
P="$(find media -type f -name "$SCENE.mp4" -print -quit)"; test -s "$P"
ffmpeg -nostdin -v error -i "$P" -f null -
render -pqh 1.0 final.log
V="$(find media -type f -name "$SCENE.mp4" -print -quit)"; test -s "$V"
W="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$V")"
H="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$V")"
FPS="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$V")"
CODEC="$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$V")"
PIX="$(ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of csv=p=0 "$V")"
DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")"
test "$W" = 1920; test "$H" = 1080; test "$FPS" = 30/1; test "$CODEC" = h264; test "$PIX" = yuv420p
ffmpeg -nostdin -v error -i "$V" -f null - 2>decode.log
cp "$V" delivery/OpenAIAssetDemo_pqh.mp4
cp main.py jp_classroom_style.py assets/images/openai_inclined_plane.webp SOURCE_SHA256.txt preview.log final.log decode.log delivery/
printf 'width\theight\tfps\tcodec\tpix_fmt\tduration\n%s\t%s\t%s\t%s\t%s\t%s\n' "$W" "$H" "$FPS" "$CODEC" "$PIX" "$DUR" > delivery/VIDEO_TECHNICAL.tsv
python - <<'PY'
import subprocess
from pathlib import Path
f=Path('delivery/OpenAIAssetDemo_pqh.mp4')
d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)],text=True))
for i,x in enumerate((.05,.25,.5,.75,.95),1):
 subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{d*x:.3f}','-i',str(f),'-frames:v','1',f'qa/qa_{i:02d}.png'],check=True)
PY
cp qa/*.png delivery/
sha256sum delivery/OpenAIAssetDemo_pqh.mp4 > delivery/VIDEO_SHA256.txt
sha256sum delivery/* > delivery/SHA256SUMS.txt
printf 'Scene: %s\nManimCE: 0.20.1\nFinal: manim -pqh main.py %s --format=mp4 --disable_caching\n' "$SCENE" "$SCENE" > delivery/RENDER_INFO.txt
