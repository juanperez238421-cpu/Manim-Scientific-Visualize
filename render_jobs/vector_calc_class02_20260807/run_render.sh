#!/usr/bin/env bash
set -euo pipefail

JOB_DIR="render_jobs/vector_calc_class02_20260807"
SOURCE="$JOB_DIR/main.py"
SCENE="VectorCalculusSurfacesClass02Detailed"
PHASE="$(tr -d '[:space:]' < "$JOB_DIR/phase.txt")"
IMAGE="manimcommunity/manim:v0.20.1"

mkdir -p media delivery qa_frames
rm -f ffprobe.txt full_decode.log qa_contact_sheet.jpg manim_version.txt

if [ "$PHASE" = "pql" ]; then
  QUALITY="-pql"
  SCALE="0.08"
  LOG="pql_render.log"
  OUT_NAME="VectorCalc_Class02_Detailed_pql.mp4"
elif [ "$PHASE" = "pqh" ]; then
  QUALITY="-pqh"
  SCALE="1.00"
  LOG="pqh_render.log"
  OUT_NAME="VectorCalc_Class02_Detailed_pqh.mp4"
else
  echo "Unsupported phase: $PHASE" >&2
  exit 2
fi

echo "PHASE=$PHASE"
echo "QUALITY=$QUALITY"
echo "LESSON_TIME_SCALE=$SCALE"

docker pull "$IMAGE"

docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -e LESSON_TIME_SCALE="$SCALE" \
  -v "$PWD:/manim" \
  -w /manim \
  --entrypoint bash \
  "$IMAGE" \
  -c '
    set -euo pipefail
    mkdir -p /tmp/manim-bin
    printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/manim-bin/xdg-open
    chmod +x /tmp/manim-bin/xdg-open
    export PATH="/tmp/manim-bin:$PATH"
    manim --version
    manim '"$QUALITY"' '"$SOURCE"' '"$SCENE"' --format=mp4 --disable_caching
  ' 2>&1 | tee "$LOG"

docker run --rm --entrypoint manim "$IMAGE" --version > manim_version.txt 2>&1 || true

VIDEO="$(find media -type f -name "${SCENE}.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
if [ -z "$VIDEO" ]; then
  echo "Rendered MP4 not found" >&2
  find media -maxdepth 5 -type f -print || true
  exit 3
fi

test -s "$VIDEO"
echo "Native video: $VIDEO"
cp "$VIDEO" "delivery/$OUT_NAME"
cp "$SOURCE" delivery/main.py
cp "$JOB_DIR/run_render.sh" delivery/run_render.sh

ffprobe -v error \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration,size \
  -of default=noprint_wrappers=1 \
  "delivery/$OUT_NAME" | tee ffprobe.txt

ffmpeg -v error -i "delivery/$OUT_NAME" -f null - 2> full_decode.log

DURATION="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "delivery/$OUT_NAME")"
FPS_SAMPLE="$(python - <<PY
D=float("$DURATION")
print(max(0.001, 12.0/max(D,0.001)))
PY
)"
ffmpeg -y -v error -i "delivery/$OUT_NAME" \
  -vf "fps=$FPS_SAMPLE,scale=480:-1,tile=4x3:padding=8:margin=8" \
  -frames:v 1 qa_contact_sheet.jpg || true

sha256sum delivery/* > delivery/SHA256SUMS.txt
cat > delivery/RENDER_INFO.txt <<EOF
Scene: $SCENE
Source: $SOURCE
ManimCE image: $IMAGE
Phase: $PHASE
Command: manim $QUALITY $SOURCE $SCENE --format=mp4 --disable_caching
LESSON_TIME_SCALE: $SCALE
Native output: $VIDEO
EOF

ls -lh "delivery/$OUT_NAME"
cat ffprobe.txt
