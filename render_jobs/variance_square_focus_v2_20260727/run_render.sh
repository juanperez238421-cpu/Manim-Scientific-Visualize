#!/usr/bin/env bash
set -euo pipefail

JOB_DIR="render_jobs/variance_square_focus_v2_20260727"
SCENE="VarianceSquareMeaningMasterclass"
IMAGE="manimcommunity/manim:v0.20.1"
PHASE="$(tr -d '[:space:]' < "$JOB_DIR/phase.txt")"

case "$PHASE" in
  pql)
    QUALITY_FLAG="-pql"
    MEDIA_DIR="media_pql"
    OUTPUT_NAME="VarianceSquareMeaningMasterclass_FocusV3_PQL.mp4"
    ;;
  pqh)
    QUALITY_FLAG="-pqh"
    MEDIA_DIR="media_pqh"
    OUTPUT_NAME="VarianceSquareMeaningMasterclass_FocusV3_NATIVE_pqh.mp4"
    ;;
  *)
    echo "Unsupported phase: $PHASE" >&2
    exit 2
    ;;
esac

rm -rf "$MEDIA_DIR" delivery control_frames review_frames
mkdir -p "$JOB_DIR" "$MEDIA_DIR" delivery control_frames review_frames
base64 --decode "$JOB_DIR/source.py.gz.b64" | gzip -dc > "$JOB_DIR/main.py"
test -s "$JOB_DIR/main.py"
python -W error -m py_compile "$JOB_DIR/main.py"
printf '%s  %s\n' \
  'f1b0538da8e72e92f174678829c919b8089bd8585a96c3dcb4cd241e0b74e18b' \
  "$JOB_DIR/main.py" | sha256sum --check --strict
grep -nE '^class VarianceSquareMeaningMasterclass\(MovingCameraScene\)' "$JOB_DIR/main.py"

docker pull "$IMAGE"
docker run --rm "$IMAGE" manim --version | tee manim_version.txt
grep -q '0.20.1' manim_version.txt

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
    manim ${QUALITY_FLAG} \\
      ${JOB_DIR}/main.py \\
      ${SCENE} \\
      --format=mp4 \\
      --disable_caching \\
      --media_dir ${MEDIA_DIR}
  " 2>&1 | tee "${PHASE}_render.log"
status=${PIPESTATUS[0]}
set -e
test "$status" -eq 0

VIDEO="$(find "$MEDIA_DIR" -type f -name "${SCENE}.mp4" -print -quit)"
test -n "$VIDEO"
test -s "$VIDEO"

command -v ffprobe
command -v ffmpeg
ffprobe -v error \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration,size \
  -of default=noprint_wrappers=1 \
  "$VIDEO" | tee ffprobe.txt

grep -q '^codec_name=h264$' ffprobe.txt
grep -q '^width=1920$' ffprobe.txt
grep -q '^height=1080$' ffprobe.txt
grep -q '^r_frame_rate=30/1$' ffprobe.txt
grep -q '^pix_fmt=yuv420p$' ffprobe.txt
ffmpeg -v error -i "$VIDEO" -f null - 2>&1 | tee full_decode.log

DURATION="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")"
MIDPOINT="$(python - "$DURATION" <<'PY'
import sys
print(max(0.0, float(sys.argv[1]) / 2.0))
PY
)"
ffmpeg -v error -ss 5 -i "$VIDEO" -frames:v 1 control_frames/frame_start.png
ffmpeg -v error -ss "$MIDPOINT" -i "$VIDEO" -frames:v 1 control_frames/frame_middle.png
ffmpeg -v error -sseof -5 -i "$VIDEO" -frames:v 1 control_frames/frame_end.png

ffmpeg -v error -i "$VIDEO" \
  -vf "fps=12/${DURATION}" \
  review_frames/frame_%02d.png
count="$(find review_frames -maxdepth 1 -type f -name 'frame_*.png' | wc -l)"
test "$count" -ge 12
ffmpeg -v error -framerate 1 -i review_frames/frame_%02d.png \
  -vf "scale=480:-1,tile=4x3:padding=8:margin=8:color=white" \
  -frames:v 1 delivery/contact_sheet.png

cp "$VIDEO" "delivery/$OUTPUT_NAME"
cp "$JOB_DIR/main.py" delivery/variance_square_meaning_masterclass_focus_v3.py
cp "${PHASE}_render.log" ffprobe.txt full_decode.log manim_version.txt delivery/
cp -r control_frames review_frames delivery/
cat > delivery/RENDER_INFO.txt <<EOF
Scene: VarianceSquareMeaningMasterclass
Source: variance_square_meaning_masterclass_focus_v3.py
ManimCE: 0.20.1
Phase: $PHASE
Command:
manim ${QUALITY_FLAG} main.py VarianceSquareMeaningMasterclass --format=mp4 --disable_caching
Source SHA-256:
f1b0538da8e72e92f174678829c919b8089bd8585a96c3dcb4cd241e0b74e18b
Revision focus:
Larger typography and geometry; clean close-ups with the persistent header hidden rather than clipped; nonfocused cards and comparison panels dimmed; the unit-flow diagram separated from the variance square; table and result-panel focus isolated; closing formula and explanatory rows rebuilt as non-overlapping stages. The original dataset, figures, equations, color semantics and nine-scene teaching logic are preserved.
EOF
(
  cd delivery
  sha256sum \
    "$OUTPUT_NAME" \
    variance_square_meaning_masterclass_focus_v3.py \
    "${PHASE}_render.log" \
    ffprobe.txt full_decode.log manim_version.txt \
    contact_sheet.png \
    control_frames/*.png review_frames/*.png \
    RENDER_INFO.txt > SHA256SUMS.txt
)
ls -lh delivery
cat delivery/manim_version.txt
cat delivery/ffprobe.txt
cat delivery/SHA256SUMS.txt
