#!/usr/bin/env bash
set -euo pipefail
JOB=render_jobs/geometry8_circle_pedagogical_qa_20260819
SCENE=render_jobs/geometry8_circle_exercises_20260824/Geometry8_Circle_Exercises_Workshop_20260824_V4_LargeText.py
CLASS=Geometry8CircleExercisesWorkshop20260824V4LargeText
mkdir -p "$JOB" /tmp/manim-bin /tmp/manim-home diag_media diag
cat render_jobs/geometry8_circle_20260818/f_*.b64 | base64 -d | gzip -dc > "$JOB/Geometry8_Circle_Fundamentals_FINAL.py"
cat render_jobs/geometry8_circle_20260818/w_*.b64 | base64 -d | gzip -dc > "$JOB/Geometry8_Circle_Workshop_FINAL.py"
cat render_jobs/geometry8_circle_20260818/s_*.b64 | base64 -d | gzip -dc > "$JOB/jp_classroom_style.py"
cp render_jobs/geometry8_circle_class2_20260818/Geometry8_Circle_Class2_Parts_Arcs.py "$JOB/Geometry8_Circle_Class2_Parts_Arcs.py"
export PYTHONPATH="$PWD/$JOB:${PYTHONPATH:-}"
printf '#!/usr/bin/env bash\nexit 0\n' > /tmp/manim-bin/xdg-open
chmod +x /tmp/manim-bin/xdg-open
export PATH=/tmp/manim-bin:$PATH
export HOME=/tmp/manim-home
export LESSON_TIME_SCALE=0.045
set +e
manim -pql "$SCENE" "$CLASS" --fps 15 --format=mp4 --media_dir diag_media --disable_caching --progress_bar none > diag/full.log 2>&1
status=$?
set -e
if [ "$status" -ne 0 ]; then
  echo '=== CONCISE MANIM FAILURE ==='
  grep -E -B 10 -A 45 'Traceback|ValueError|TypeError|AttributeError|IndexError|KeyError|Exception|ERROR|exceeds|Error|padding|safe' diag/full.log | tail -n 180 || tail -n 180 diag/full.log
  echo "=== EXIT STATUS: $status ==="
  exit "$status"
fi
echo 'PQL_DIAGNOSTIC_SUCCESS'
