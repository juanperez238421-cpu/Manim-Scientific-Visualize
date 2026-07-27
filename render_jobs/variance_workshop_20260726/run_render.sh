#!/usr/bin/env bash
set -euo pipefail

BASE_JOB_DIR="render_jobs/variance_workshop_20260726"
IQR_JOB_DIR="render_jobs/variance_iqr_detailed_20260727"
SCENE="VarianceComprehensiveWorkshop"
IMAGE="manimcommunity/manim:v0.20.1"

rm -rf media_pql media_pqh delivery control_frames
mkdir -p "$BASE_JOB_DIR" "$IQR_JOB_DIR" media_pql media_pqh delivery control_frames
cat "$BASE_JOB_DIR"/source_parts/part_*.b64 | base64 --decode > "$BASE_JOB_DIR/main.py"
test -s "$BASE_JOB_DIR/main.py"

# Preserve the two native-pdfLaTeX corrections validated in the previous render.
python - "$BASE_JOB_DIR/main.py" <<'PY'
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

# Replace only Scene 4 with the expanded eight-stage IQR construction.
cat "$IQR_JOB_DIR"/iqr_parts/part_*.b64 | base64 --decode > "$IQR_JOB_DIR/new_iqr_section.txt"
python - "$BASE_JOB_DIR/main.py" "$IQR_JOB_DIR/new_iqr_section.txt" <<'PY'
from pathlib import Path
import sys

source_path = Path(sys.argv[1])
section_path = Path(sys.argv[2])
source = source_path.read_text(encoding="utf-8")
new_section = section_path.read_text(encoding="utf-8")
start_marker = "    # ========================================================\n    # SCENE 4"
end_marker = "    # ========================================================\n    # SCENE 5"
start = source.index(start_marker)
end = source.index(end_marker, start)
source_path.write_text(source[:start] + new_section + "\n" + source[end:], encoding="utf-8")
print(f"Applied detailed IQR replacement: {len(new_section.splitlines())} lines")
PY

# Final visual-polish correction confirmed by contact-sheet inspection:
# move the off-axis lower-fence note away from quartile labels and stagger Q1/Q2/Q3.
python - "$BASE_JOB_DIR/main.py" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
changes = [
    (
        'lower_fence_note.move_to([-3.95, 2.04, 0])',
        'lower_fence_note.move_to([-4.65, -0.12, 0])',
    ),
    (
        'MathTex(r"Q_1=3.5", color=PURPLE).scale(0.43).next_to(q1_guide, UP, buff=0.08),',
        'MathTex(r"Q_1=3.5", color=PURPLE).scale(0.43).next_to(q1_guide, UP, buff=0.08).shift(LEFT * 0.22 + DOWN * 0.16),',
    ),
    (
        'MathTex(r"Q_2=5.5", color=GOLD).scale(0.43).next_to(q2_guide, UP, buff=0.08),',
        'MathTex(r"Q_2=5.5", color=GOLD).scale(0.43).next_to(q2_guide, UP, buff=0.08).shift(UP * 0.12),',
    ),
    (
        'MathTex(r"Q_3=7.5", color=TEAL).scale(0.43).next_to(q3_guide, UP, buff=0.08),',
        'MathTex(r"Q_3=7.5", color=TEAL).scale(0.43).next_to(q3_guide, UP, buff=0.08).shift(RIGHT * 0.22 + DOWN * 0.16),',
    ),
]
for old, new in changes:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one occurrence of {old!r}, found {count}")
    source = source.replace(old, new)
path.write_text(source, encoding="utf-8")
PY

python -W error -m py_compile "$BASE_JOB_DIR/main.py"
printf '%s  %s\n' \
  '5cfc11e6bfa06bb46547c5140cbaea18a1aa132c804a87ed265de11337374042' \
  "$BASE_JOB_DIR/main.py" | sha256sum --check --strict
grep -nE '^class VarianceComprehensiveWorkshop\(MovingCameraScene\)' "$BASE_JOB_DIR/main.py"

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
        ${BASE_JOB_DIR}/main.py \\
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

cp "$PQH_VIDEO" delivery/VarianceComprehensiveWorkshop_IQR_Detailed_Polished_NATIVE_pqh.mp4
cp "$BASE_JOB_DIR/main.py" delivery/variance_workshop_iqr_detailed_polished.py
cp pql_render.log pqh_render.log ffprobe.txt full_decode.log manim_version.txt delivery/
cp -r control_frames delivery/

cat > delivery/RENDER_INFO.txt <<'EOF'
Scene: VarianceComprehensiveWorkshop
Source: variance_workshop_iqr_detailed_polished.py
ManimCE: 0.20.1
Test command:
manim -pql main.py VarianceComprehensiveWorkshop --format=mp4 --disable_caching
Final command:
manim -pqh main.py VarianceComprehensiveWorkshop --format=mp4 --disable_caching
Instructional update:
Only scene_iqr_step_by_step was redesigned. It now explicitly animates sorting, ordered positions, Q2 calculation, lower/upper halves, Q1/Q3 calculations, IQR and Tukey fences, number-line classification, box/median/whisker/outlier assembly, and robustness to moving the outlier from 20 to 45.
Dataset for the detailed construction:
[2, 3, 4, 5, 6, 7, 8, 20]
Quartiles and fences:
Q1=3.5, Q2=5.5, Q3=7.5, IQR=4, lower fence=-2.5, upper fence=13.5.
Final visual-polish correction:
The lower-fence note was moved into the empty lower-left region and Q1/Q2/Q3 labels were staggered to remove overlap found during contact-sheet review.
All other workshop scenes retain the previously validated code.
Verification:
Native -pql and literal -pqh were executed in manimcommunity/manim:v0.20.1. ffprobe, full FFmpeg decoding, and three control-frame extractions were executed on the GitHub Ubuntu runner.
EOF

(
  cd delivery
  sha256sum \
    VarianceComprehensiveWorkshop_IQR_Detailed_Polished_NATIVE_pqh.mp4 \
    variance_workshop_iqr_detailed_polished.py \
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
