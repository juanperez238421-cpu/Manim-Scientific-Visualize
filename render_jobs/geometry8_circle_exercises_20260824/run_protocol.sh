#!/usr/bin/env bash
set -euo pipefail

JOB=render_jobs/geometry8_circle_pedagogical_qa_20260819
SCENE=render_jobs/geometry8_circle_exercises_20260824/Geometry8_Circle_Exercises_Workshop_20260824.py
CLASS=Geometry8CircleExercisesWorkshop20260824

rm -rf out qa_out qa_media media
mkdir -p "$JOB" out qa_out qa_media media /tmp/manim-bin /tmp/manim-home

# Reconstruct the exact audited Circle V4 stack.
cat render_jobs/geometry8_circle_20260818/f_*.b64 | base64 -d | gzip -dc > "$JOB/Geometry8_Circle_Fundamentals_FINAL.py"
cat render_jobs/geometry8_circle_20260818/w_*.b64 | base64 -d | gzip -dc > "$JOB/Geometry8_Circle_Workshop_FINAL.py"
cat render_jobs/geometry8_circle_20260818/s_*.b64 | base64 -d | gzip -dc > "$JOB/jp_classroom_style.py"
cp render_jobs/geometry8_circle_class2_20260818/Geometry8_Circle_Class2_Parts_Arcs.py "$JOB/Geometry8_Circle_Class2_Parts_Arcs.py"

export PYTHONPATH="$PWD/$JOB:${PYTHONPATH:-}"

# Static and mathematical QA before any render.
python -Werror -m py_compile \
  "$JOB/jp_classroom_style.py" \
  "$JOB/Geometry8_Circle_Fundamentals_FINAL.py" \
  "$JOB/Geometry8_Circle_Class2_Parts_Arcs.py" \
  "$JOB/Geometry8_Circle_Workshop_FINAL.py" \
  "$JOB/Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA.py" \
  "$JOB/Geometry8_Circle_PEDAGOGICAL_SEQUENCE_SENIOR_QA_V2.py" \
  "$JOB/Geometry8_Circle_Measurement_To_Area_20260823.py" \
  "$JOB/Geometry8_Circle_Measurement_To_Area_20260823_V2.py" \
  "$JOB/Geometry8_Circle_V3_Primitives.py" \
  "$JOB/Geometry8_Circle_V3_Measurement.py" \
  "$JOB/Geometry8_Circle_V3_Area.py" \
  "$JOB/Geometry8_Circle_V3_Exercises.py" \
  "$JOB/Geometry8_Circle_Measurement_To_Area_20260823_V3.py" \
  "$JOB/Geometry8_Circle_V4_Senior_QA.py" \
  "$JOB/Geometry8_Circle_V4_Senior_QA_Fixes.py" \
  "$JOB/Geometry8_Circle_Measurement_To_Area_20260823_V4.py" \
  "$SCENE"

grep -Fq "class $CLASS" "$SCENE"
grep -Fq 'exercise_09_sector' "$SCENE"
grep -Fq 'self._v4_zoom' "$SCENE"
grep -Fq 'assert_content_safe' "$SCENE"
grep -Fq 'validate_lesson_data' "$SCENE"

python - <<'PY'
import av
from PIL import Image
print('PyAV:', av.__version__)
print('Pillow:', Image.__version__)
PY

# Neutralize -p preview in the headless container without changing literal protocol commands.
printf '#!/usr/bin/env bash\nexit 0\n' > /tmp/manim-bin/xdg-open
chmod +x /tmp/manim-bin/xdg-open
export PATH=/tmp/manim-bin:$PATH
export HOME=/tmp/manim-home

# PASS 1 — literal -pql full-timeline runtime/safe-frame gate.
export LESSON_TIME_SCALE=0.045
manim -pql "$SCENE" "$CLASS" \
  --fps 15 --format=mp4 --media_dir qa_media --disable_caching \
  2>&1 | tee qa_out/CIRCLE_EXERCISES_WORKSHOP_pql.log

PQL="$(find qa_media -type f -name "$CLASS.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
test -n "$PQL" && test -s "$PQL"
cp "$PQL" qa_out/Geometry8_Circle_Exercises_Workshop_20260824_pql.mp4

python - "$PQL" <<'PY'
import av, sys
path=sys.argv[1]
frames=0
with av.open(path) as c:
    stream=c.streams.video[0]
    for _ in c.decode(stream):
        frames += 1
assert frames > 0, 'PQL decoder returned zero frames'
print(f'PQL decoded successfully: {frames} frames')
PY

# PASS 2 — literal -pqh final render only after PQL success.
export LESSON_TIME_SCALE=1.0
manim -pqh "$SCENE" "$CLASS" \
  --fps 30 --format=mp4 --media_dir media --disable_caching \
  2>&1 | tee out/CIRCLE_EXERCISES_WORKSHOP_pqh.log

FINAL="$(find media -type f -name "$CLASS.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
test -n "$FINAL" && test -s "$FINAL"
cp "$FINAL" out/Geometry8_Circle_Exercises_Workshop_20260824_FINAL_pqh.mp4

# Technical QA — full decode and delivery-spec assertions.
F=out/Geometry8_Circle_Exercises_Workshop_20260824_FINAL_pqh.mp4
python - "$F" <<'PY' | tee out/VIDEO_TECHNICAL.txt
import av, sys, os
path=sys.argv[1]
with av.open(path) as c:
    s=c.streams.video[0]
    codec=s.codec_context.name
    width=s.codec_context.width
    height=s.codec_context.height
    fmt=s.codec_context.format.name if s.codec_context.format else ''
    fps=float(s.average_rate) if s.average_rate else 0.0
    duration=(float(c.duration) / float(av.time_base)) if c.duration else 0.0
    frames=0
    for _ in c.decode(s):
        frames += 1
size=os.path.getsize(path)
print(f'codec_name={codec}')
print(f'width={width}')
print(f'height={height}')
print(f'pix_fmt={fmt}')
print(f'fps={fps:.6f}')
print(f'duration={duration:.6f}')
print(f'frames_decoded={frames}')
print(f'size={size}')
assert width == 1920
assert height == 1080
assert abs(fps - 30.0) < 0.001
assert codec == 'h264'
assert fmt == 'yuv420p'
assert frames > 0
assert duration > 60.0
PY
sha256sum "$F" > out/SHA256SUMS.txt

# Visual QA evidence: 24 PQL samples + 48 final PQH samples/contact sheets.
mkdir -p out/frame_samples_final out/frame_samples_pql
python - <<'PY'
import av, os, math
from PIL import Image, ImageDraw

def sample(path, outdir, sheet_path, count):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return
    os.makedirs(outdir, exist_ok=True)
    saved=[]
    with av.open(path) as c:
        stream=c.streams.video[0]
        duration=(float(c.duration)/float(av.time_base)) if c.duration else 1.0
        targets=[duration*i/(count+1) for i in range(1,count+1)]
        ti=0
        for frame in c.decode(stream):
            if ti >= len(targets):
                break
            t=float(frame.pts * frame.time_base) if frame.pts is not None else 0.0
            if t >= targets[ti]:
                img=frame.to_image().convert('RGB')
                fp=f'{outdir}/frame_{ti+1:02d}_{targets[ti]:07.2f}.jpg'
                img.save(fp, quality=90)
                saved.append(fp)
                ti += 1
    thumbs=[]
    for fp in saved:
        im=Image.open(fp).convert('RGB')
        im.thumbnail((480,270))
        card=Image.new('RGB',(500,300),'white')
        card.paste(im,((500-im.width)//2,8))
        ImageDraw.Draw(card).text((10,280),os.path.basename(fp),fill='black')
        thumbs.append(card)
    if thumbs:
        cols=3
        rows=math.ceil(len(thumbs)/cols)
        sheet=Image.new('RGB',(cols*500,rows*300),'white')
        for i,im in enumerate(thumbs):
            sheet.paste(im,((i%cols)*500,(i//cols)*300))
        sheet.save(sheet_path, quality=90)
    print(f'{sheet_path}: {len(saved)} samples')

sample(
    'qa_out/Geometry8_Circle_Exercises_Workshop_20260824_pql.mp4',
    'out/frame_samples_pql',
    'out/Geometry8_Circle_Exercises_Workshop_PQL_contact_sheet.jpg',
    24,
)
sample(
    'out/Geometry8_Circle_Exercises_Workshop_20260824_FINAL_pqh.mp4',
    'out/frame_samples_final',
    'out/Geometry8_Circle_Exercises_Workshop_FINAL_contact_sheet.jpg',
    48,
)
PY

# Preserve exact source stack and logs with the artifact.
cp "$SCENE" out/
cp "$JOB/Geometry8_Circle_V4_Senior_QA.py" out/
cp "$JOB/Geometry8_Circle_V4_Senior_QA_Fixes.py" out/
cp "$JOB/Geometry8_Circle_Measurement_To_Area_20260823_V4.py" out/
cp "$JOB/jp_classroom_style.py" out/
cp qa_out/CIRCLE_EXERCISES_WORKSHOP_pql.log out/
cp qa_out/Geometry8_Circle_Exercises_Workshop_20260824_pql.mp4 out/
