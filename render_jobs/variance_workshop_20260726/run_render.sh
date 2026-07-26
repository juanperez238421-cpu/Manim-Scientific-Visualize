#!/usr/bin/env bash
set -euo pipefail

JOB_DIR="render_jobs/variance_workshop_20260726"
SCENE="VarianceComprehensiveWorkshop"
IMAGE="manimcommunity/manim:v0.20.1"

mkdir -p "$JOB_DIR" media_pql media_pqh delivery control_frames
cat "$JOB_DIR"/source_parts/part_*.b64 | base64 --decode > "$JOB_DIR/main.py"
test -s "$JOB_DIR/main.py"

# Apply only the two native-LaTeX corrections confirmed by the first -pql traceback.
python - "$JOB_DIR/main.py" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
changes = [
    (
        '"The IQR describes the central 50% of the sorted observations and resists extreme outliers."',
        'r"The IQR describes the central 50\\% of the sorted observations and resists extreme outliers."',
    ),
    (
        'Tex("Central 50%; preferred when outliers or skew are present.", color=INK)',
        'Tex(r"Central 50\\%; preferred when outliers or skew are present.", color=INK)',
    ),
]
for old, new in changes:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one occurrence of {old!r}, found {count}")
    source = source.replace(old, new)
path.write_text(source, encoding="utf-8")
PY

python -W error -m py_compile "$JOB_DIR/main.py"
printf '%s  %s\n' \
  'f198ae7d763d61b3a7277cb219223b4b809609a7770119dfda123d3e74e7f4e4' \
  "$JOB_DIR/main.py" | sha256sum --check --strict
grep -nE '^class VarianceComprehensiveWorkshop\(MovingCameraScene\)' "$JOB_DIR/main.py"

docker pull "$IMAGE"
docker run --rm "$IMAGE" manim --version | tee manim_version.txt
grep -q '0.20.1' manim_version.txt

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

command -v ffprobe
command -v ffmpeg

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
cp pql_render.log pqh_render.log ffprobe.txt full_decode.log manim_version.txt delivery/
cp -r control_frames delivery/

cat > delivery/RENDER_INFO.txt <<'EOF'
Scene: VarianceComprehensiveWorkshop
Source: variance_workshop_rendered.py
ManimCE: 0.20.1
Test command:
manim -pql main.py VarianceComprehensiveWorkshop --format=mp4 --disable_caching
Final command:
manim -pqh main.py VarianceComprehensiveWorkshop --format=mp4 --disable_caching
Source modifications required for native pdfLaTeX compatibility:
- Five Unicode em dashes inside Tex strings were replaced by LaTeX-safe double hyphens (--).
- Two prose percent signs passed through Tex were escaped as \%.
No dataset, formula, timing, layout, animation, or scene logic was changed.
Verification:
ffprobe, complete FFmpeg decoding, and control-frame extraction were executed on the GitHub Ubuntu runner after explicit installation of FFmpeg tools.
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
    manim_version.txt \
    control_frames/*.png \
    RENDER_INFO.txt > SHA256SUMS.txt
)

ls -lh delivery
cat delivery/manim_version.txt
cat delivery/ffprobe.txt
cat delivery/SHA256SUMS.txt
