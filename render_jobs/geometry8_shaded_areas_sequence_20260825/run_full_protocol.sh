#!/usr/bin/env bash
set -euo pipefail

JOB=render_jobs/geometry8_shaded_areas_sequence_20260825
BASE_SCENE="$JOB/Geometry8_Shaded_Areas_Calendar_Sequence_20260825.py"
SCENE="$JOB/Geometry8_Shaded_Areas_Calendar_Sequence_20260825_V2_QA.py"

CLASSES=(
  Geometry8Week4SimpleShadedAreasV2
  Geometry8Week5ComplexShadedAreasV2
  Geometry8Week6ScalingPerimeterAreaV2
  Geometry8Week7IntegratedAreaPerimeterChallengeV2
)
SLUGS=(
  Week4_Simple_Shaded_Areas
  Week5_Complex_Shaded_Areas
  Week6_Scaling_Perimeter_Area
  Week7_Integrated_Area_Perimeter
)

rm -rf out qa_out qa_media media /tmp/manim-bin /tmp/manim-home
mkdir -p out qa_out qa_media media /tmp/manim-bin /tmp/manim-home

# Reconstruct the exact audited JP classroom style from the accepted Circle stack.
cat render_jobs/geometry8_circle_20260818/s_*.b64 | base64 -d | gzip -dc > "$JOB/jp_classroom_style.py"
export PYTHONPATH="$PWD/$JOB:${PYTHONPATH:-}"

# -----------------------------------------------------------------------------
# Static + mathematical QA
# -----------------------------------------------------------------------------
python -Werror -m py_compile "$JOB/jp_classroom_style.py" "$BASE_SCENE" "$SCENE"
for C in "${CLASSES[@]}"; do
  grep -Fq "class $C" "$SCENE"
done
grep -Fq 'assert_content_safe' "$BASE_SCENE"
grep -Fq 'validate_lesson_data' "$BASE_SCENE"
grep -Fq 'assert diagrams.get_right()[0] < card.get_left()[0]' "$SCENE"

# Compile the student workshop and teacher key as part of the reproducible package.
pdflatex -interaction=nonstopmode -halt-on-error -output-directory out "$JOB/Geometry8_Shaded_Areas_Workshop_Student.tex" > out/STUDENT_PDF_BUILD.log
pdflatex -interaction=nonstopmode -halt-on-error -output-directory out "$JOB/Geometry8_Shaded_Areas_Workshop_Teacher_Key.tex" > out/TEACHER_KEY_PDF_BUILD.log
test -s out/Geometry8_Shaded_Areas_Workshop_Student.pdf
test -s out/Geometry8_Shaded_Areas_Workshop_Teacher_Key.pdf

# Neutralize literal -p preview in the headless container.
printf '#!/usr/bin/env bash\nexit 0\n' > /tmp/manim-bin/xdg-open
chmod +x /tmp/manim-bin/xdg-open
export PATH="/tmp/manim-bin:$PATH"
export HOME=/tmp/manim-home

# -----------------------------------------------------------------------------
# Render each scheduled lesson: literal PQL gate, then literal PQH final.
# -----------------------------------------------------------------------------
for i in "${!CLASSES[@]}"; do
  C="${CLASSES[$i]}"
  S="${SLUGS[$i]}"

  rm -rf "qa_media/$S" "media/$S"
  mkdir -p "qa_media/$S" "media/$S" "out/frame_samples_$S"

  export LESSON_TIME_SCALE=0.040
  manim -pql "$SCENE" "$C" \
    --fps 15 --format=mp4 --media_dir "qa_media/$S" --disable_caching \
    2>&1 | tee "qa_out/${S}_pql.log"

  PQL="$(find "qa_media/$S" -type f -name "$C.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
  test -n "$PQL" && test -s "$PQL"
  cp "$PQL" "qa_out/Geometry8_${S}_PQL.mp4"

  python - "$PQL" <<'PY'
import av, sys
path = sys.argv[1]
frames = 0
with av.open(path) as c:
    stream = c.streams.video[0]
    for _ in c.decode(stream):
        frames += 1
assert frames > 0, 'PQL decoder returned zero frames'
print(f'PQL full decode PASS: {frames} frames')
PY

  export LESSON_TIME_SCALE=1.0
  manim -pqh "$SCENE" "$C" \
    --fps 30 --format=mp4 --media_dir "media/$S" --disable_caching \
    2>&1 | tee "out/${S}_pqh.log"

  FINAL="$(find "media/$S" -type f -name "$C.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
  test -n "$FINAL" && test -s "$FINAL"
  DEST="out/Geometry8_${S}_FINAL_pqh.mp4"
  cp "$FINAL" "$DEST"

  python - "$DEST" "$S" <<'PY' | tee "out/${S}_VIDEO_TECHNICAL.txt"
import av, sys, os
path, slug = sys.argv[1], sys.argv[2]
with av.open(path) as c:
    s = c.streams.video[0]
    codec = s.codec_context.name
    width = s.codec_context.width
    height = s.codec_context.height
    fmt = s.codec_context.format.name if s.codec_context.format else ''
    fps = float(s.average_rate) if s.average_rate else 0.0
    duration = float(c.duration) / float(av.time_base) if c.duration else 0.0
    frames = 0
    for _ in c.decode(s):
        frames += 1
size = os.path.getsize(path)
print(f'slug={slug}')
print(f'codec_name={codec}')
print(f'width={width}')
print(f'height={height}')
print(f'pix_fmt={fmt}')
print(f'fps={fps:.6f}')
print(f'duration={duration:.6f}')
print(f'frames_decoded={frames}')
print(f'size={size}')
assert codec == 'h264'
assert width == 1920 and height == 1080
assert fmt == 'yuv420p'
assert abs(fps - 30.0) < 0.001
assert frames > 0
assert duration > 60.0
PY

done

# -----------------------------------------------------------------------------
# Distributed frame QA + contact sheets for all four finals.
# -----------------------------------------------------------------------------
python - <<'PY'
import av, os, math, glob
from PIL import Image, ImageDraw

for path in sorted(glob.glob('out/Geometry8_*_FINAL_pqh.mp4')):
    slug = os.path.basename(path).replace('Geometry8_', '').replace('_FINAL_pqh.mp4', '')
    outdir = f'out/frame_samples_{slug}'
    os.makedirs(outdir, exist_ok=True)
    count = 18
    saved = []
    with av.open(path) as c:
        stream = c.streams.video[0]
        duration = float(c.duration) / float(av.time_base) if c.duration else 1.0
        targets = [duration * i / (count + 1) for i in range(1, count + 1)]
        ti = 0
        for frame in c.decode(stream):
            if ti >= len(targets):
                break
            t = float(frame.pts * frame.time_base) if frame.pts is not None else 0.0
            if t >= targets[ti]:
                img = frame.to_image().convert('RGB')
                fp = f'{outdir}/frame_{ti+1:02d}_{targets[ti]:07.2f}.jpg'
                img.save(fp, quality=90)
                saved.append(fp)
                ti += 1
    thumbs = []
    for fp in saved:
        im = Image.open(fp).convert('RGB')
        im.thumbnail((480, 270))
        card = Image.new('RGB', (500, 300), 'white')
        card.paste(im, ((500-im.width)//2, 8))
        ImageDraw.Draw(card).text((10, 280), os.path.basename(fp), fill='black')
        thumbs.append(card)
    if thumbs:
        cols = 3
        rows = math.ceil(len(thumbs) / cols)
        sheet = Image.new('RGB', (cols*500, rows*300), 'white')
        for j, im in enumerate(thumbs):
            sheet.paste(im, ((j % cols)*500, (j // cols)*300))
        sheet.save(f'out/Geometry8_{slug}_FINAL_contact_sheet.jpg', quality=90)
    print(f'{slug}: {len(saved)} audit frames')
PY

# Preserve exact sources, planning alignment and logs.
cp "$BASE_SCENE" out/
cp "$SCENE" out/
cp "$JOB/jp_classroom_style.py" out/
cp "$JOB/CALENDAR_ALIGNMENT.md" out/
cp "$JOB/Geometry8_Shaded_Areas_Workshop_Student.tex" out/
cp "$JOB/Geometry8_Shaded_Areas_Workshop_Teacher_Key.tex" out/
cp qa_out/*_pql.log out/

cat > out/README_DELIVERY.txt <<'EOF'
GEOMETRY 8 — CALENDAR CONTINUATION COMPLETE PACKAGE

Final PQH videos:
1. Week 4 — Simple shaded areas
2. Week 5 — Complex shaded areas
3. Week 6 — Perimeter vs area under scaling
4. Week 7 — Integrated area/perimeter challenge

Documents:
- Student workshop PDF
- Teacher key PDF
- Calendar alignment
- Exact ManimCE source + V2 QA overrides
- Exact JP classroom style used for rendering
- PQL and PQH logs
- Technical QA reports
- Distributed audit frames + contact sheets
- SHA-256 checksums

Render protocol:
- ManimCE 0.20.1
- literal -pql gate before each final
- literal -pqh final
- 1920x1080, 30 fps, H.264/yuv420p
- full video decode validation
EOF

# SHA-256 after all primary deliverables exist.
(
  cd out
  sha256sum Geometry8_*_FINAL_pqh.mp4 Geometry8_Shaded_Areas_Workshop_Student.pdf Geometry8_Shaded_Areas_Workshop_Teacher_Key.pdf > SHA256SUMS.txt
)

# Build one downloadable complete package without relying on system zip.
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path('out')
target = root / 'Geometry8_Shaded_Areas_Calendar_Sequence_20260825_COMPLETE_PQH.zip'
with ZipFile(target, 'w', ZIP_DEFLATED, compresslevel=6) as z:
    for p in sorted(root.rglob('*')):
        if p == target or not p.is_file():
            continue
        z.write(p, p.relative_to(root))
print(target, target.stat().st_size)
PY

test -s out/Geometry8_Shaded_Areas_Calendar_Sequence_20260825_COMPLETE_PQH.zip
