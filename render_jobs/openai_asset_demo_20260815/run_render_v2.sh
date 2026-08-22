#!/usr/bin/env bash
set -euo pipefail
JOB=render_jobs/openai_asset_demo_20260815
SCENE=OpenAIAssetInclinedPlaneLesson
mkdir -p assets/images delivery qa_frames
cat "$JOB"/main_pt_0[0-4] > main.py
cat "$JOB"/style_pt_0[0-8] > jp_classroom_style.py
cat "$JOB"/ap_0[0-8] | base64 -d > assets/images/openai_inclined_plane_block_760_q55.webp
echo '0575594653365878ad454e471752691589960a4a5d7e30e27393994b19c6c032  main.py' | sha256sum -c -
echo '3f3f06e94d5cad870ad335502cc1a93e56ce675abb1231ded5f9c71fd3e60e3d  jp_classroom_style.py' | sha256sum -c -
echo 'ee660f75cc495e6c11d8e426c6d971aedfab774a258ca99901f13333f676f43d  assets/images/openai_inclined_plane_block_760_q55.webp' | sha256sum -c -
python -m py_compile main.py jp_classroom_style.py
sha256sum main.py jp_classroom_style.py assets/images/openai_inclined_plane_block_760_q55.webp > SOURCE_SHA256.txt
command -v ffprobe >/dev/null || { sudo apt-get update -qq; sudo apt-get install -y -qq ffmpeg; }
docker pull manimcommunity/manim:v0.20.1 >/dev/null
render(){
  local quality="$1" scale="$2" log="$3"
  rm -rf media
  docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home -e LESSON_TIME_SCALE="$scale" \
    -v "$PWD:/manim" -w /manim --entrypoint bash manimcommunity/manim:v0.20.1 -c "
      set -euo pipefail
      mkdir -p /tmp/manim-bin
      printf '#!/usr/bin/env bash\nexit 0\n' > /tmp/manim-bin/xdg-open
      chmod +x /tmp/manim-bin/xdg-open
      export PATH=/tmp/manim-bin:\$PATH
      manim $quality main.py $SCENE --format=mp4 --disable_caching
    " 2>&1 | tee "$log"
}
render -pql 0.12 preview_pql.log
PREVIEW="$(find media -type f -name "$SCENE.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
test -n "$PREVIEW" && test -s "$PREVIEW"
ffmpeg -nostdin -v error -i "$PREVIEW" -f null -
render -pqh 1.0 render_pqh.log
VIDEO="$(find media -type f -name "$SCENE.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
test -n "$VIDEO" && test -s "$VIDEO"
W="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$VIDEO")"
H="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$VIDEO")"
FPS="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$VIDEO")"
CODEC="$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$VIDEO")"
PIX="$(ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of csv=p=0 "$VIDEO")"
DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")"
SIZE="$(stat -c '%s' "$VIDEO")"
printf 'width\theight\tfps\tcodec\tpix_fmt\tduration\tsize_bytes\n%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$W" "$H" "$FPS" "$CODEC" "$PIX" "$DUR" "$SIZE" > VIDEO_TECHNICAL.tsv
test "$W" = 1920; test "$H" = 1080; test "$FPS" = 30/1; test "$CODEC" = h264; test "$PIX" = yuv420p
ffmpeg -nostdin -v error -i "$VIDEO" -f null - 2> decode.log
cp "$VIDEO" delivery/${SCENE}_pqh.mp4
cp main.py jp_classroom_style.py SOURCE_SHA256.txt VIDEO_TECHNICAL.tsv preview_pql.log render_pqh.log decode.log delivery/
cp assets/images/openai_inclined_plane_block_760_q55.webp delivery/
python - <<'PY'
import subprocess
from pathlib import Path
f=Path('delivery/OpenAIAssetInclinedPlaneLesson_pqh.mp4')
d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)],text=True).strip())
for i,x in enumerate((.05,.25,.5,.75,.95),1):
 subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{d*x:.3f}','-i',str(f),'-frames:v','1',f'qa_frames/qa_{i:02d}.png'],check=True)
PY
cp qa_frames/*.png delivery/
sha256sum delivery/${SCENE}_pqh.mp4 > delivery/VIDEO_SHA256.txt
sha256sum delivery/* > delivery/SHA256SUMS.txt
printf 'Scene: %s\nManimCE: 0.20.1\nFinal: manim -pqh main.py %s --format=mp4 --disable_caching\nResolution: %sx%s\nFPS: %s\nCodec: %s\nPixel format: %s\nDuration: %s\n' "$SCENE" "$SCENE" "$W" "$H" "$FPS" "$CODEC" "$PIX" "$DUR" > delivery/RENDER_INFO.txt
