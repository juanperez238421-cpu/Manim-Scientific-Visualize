#!/usr/bin/env bash
set -euo pipefail

JOB_DIR="render_jobs/variance_workshop_20260726"
SCENE="VarianceComprehensiveWorkshop"
IMAGE="manimcommunity/manim:v0.20.1"

mkdir -p "$JOB_DIR" media_pql media_pqh delivery control_frames
cat "$JOB_DIR"/source_parts/part_*.b64 | base64 --decode > "$JOB_DIR/main.py"
test -s "$JOB_DIR/main.py"
python -m py_compile "$JOB_DIR/main.py"
printf '%s  %s\n' \
  'b4688502081292dc552a941b217d46acc8023b2045d5208ff0f79ac8df77d041' \
  "$JOB_DIR/main.py" | sha256sum --check --strict
grep -nE '^class VarianceComprehensiveWorkshop\(MovingCameraScene\)' "$JOB_DIR/main.py"

docker pull "$IMAGE"

run_manim() {
  local quality_flag="$1"
  local media_dir="$2"
  local log_file="$3"

  set +e
  docker run --rm \
    --user "$(id -u):$(id -g)" \
    -e HOME=/tmp/manim-home \
    -v "$PWD:/manim" \
    -w /manim \
    --entrypoint bash \
    "$IMAGE" \
    -c "
      set -euo pipefail
      mkdir -p /tmp/manim-bin
      printf '#!/usr/bin/env bash\\nexit 0\\n' > /tmp/manim-bin/xdg-open
      chmod +x /tmp/manim-bin/xdg-open
      export PATH=\"/tmp/manim-bin:\$PATH\"
      manim ${quality_flag} \\
        ${JOB_DIR}/main.py \\
        ${SCENE} \\
        --format=mp4 \\
        --disable_caching \\
        --media_dir ${media_dir}
    " 2>&1 | tee "$log_file"
  local status=${PIPESTATUS[0]}
  set -e
  test "$status" -eq 0
}

run_manim -pql media_pql pql_render.log
PQL_VIDEO="$(find media_pql -type f -name "${SCENE}.mp4" -print -quit)"
test -n "$PQL_VIDEO"
test -s "$PQL_VIDEO"

run_manim -pqh media_pqh pqh_render.log
PQH_VIDEO="$(find media_pqh -type f -name "${SCENE}.mp4" -print -quit)"
test -n "$PQH_VIDEO"
test -s "$PQH_VIDEO"

ffprobe -v error \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration,size \
  -of default=noprint_wrappers=1 \
  "$PQH_VIDEO" | tee ffprobe.txt

grep -q '^codec_name=h264$' ffprobe.txt
grep -q '^width=1920$' ffprobe.txt
grep -q '^height=1080$' ffprobe.txt
grep -q '^r_frame_rate=30/1$' ffprobe.txt
grep -q '^pix_fmt=yuv420p$' ffprobe.txt

ffmpeg -v error -i "$PQH_VIDEO" -f null - 2>&1 | tee full_decode.log

DURATION="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$PQH_VIDEO")"
MIDPOINT="$(python - "$DURATION" <<'PY'
import sys
print(max(0.0, float(sys.argv[1]) / 2.0))
PY
)"

ffmpeg -v error -ss 5 -i "$PQH_VIDEO" -frames:v 1 control_frames/frame_start.png
ffmpeg -v error -ss "$MIDPOINT" -i "$PQH_VIDEO" -frames:v 1 control_frames/frame_middle.png
ffmpeg -v error -sseof -5 -i "$PQH_VIDEO" -frames:v 1 control_frames/frame_end.png

test -s control_frames/frame_start.png
test -s control_frames/frame_middle.png
test -s control_frames/frame_end.png

cp "$PQH_VIDEO" delivery/VarianceComprehensiveWorkshop_NATIVE_pqh.mp4
cp "$JOB_DIR/main.py" delivery/variance_workshop_rendered.py
cp pql_render.log pqh_render.log ffprobe.txt full_decode.log delivery/
cp -r control_frames delivery/

cat > delivery/RENDER_INFO.txt <<'EOF'
Scene: VarianceComprehensiveWorkshop
Source: variance_workshop_rendered.py
ManimCE: 0.20.1
Test command:
manim -pql main.py VarianceComprehensiveWorkshop --format=mp4 --disable_caching
Final command:
manim -pqh main.py VarianceComprehensiveWorkshop --format=mp4 --disable_caching
Source modification from user upload:
Only five Unicode em dashes inside Tex strings were replaced by LaTeX-safe double hyphens (--). No dataset, formula, timing, layout, animation, or scene logic was changed.
EOF

(
  cd delivery
  sha256sum \
    VarianceComprehensiveWorkshop_NATIVE_pqh.mp4 \
    variance_workshop_rendered.py \
    pql_render.log \
    pqh_render.log \
    ffprobe.txt \
    full_decode.log \
    control_frames/*.png \
    RENDER_INFO.txt > SHA256SUMS.txt
)

ls -lh delivery
cat delivery/ffprobe.txt
cat delivery/SHA256SUMS.txt
