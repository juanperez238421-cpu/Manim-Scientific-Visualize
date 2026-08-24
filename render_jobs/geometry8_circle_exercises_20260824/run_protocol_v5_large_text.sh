#!/usr/bin/env bash
set -euo pipefail
TMP=/tmp/run_circle_workshop_v5_large_text.sh
cp render_jobs/geometry8_circle_exercises_20260824/run_protocol.sh "$TMP"
sed -i \
  's#SCENE=render_jobs/geometry8_circle_exercises_20260824/Geometry8_Circle_Exercises_Workshop_20260824.py#SCENE=render_jobs/geometry8_circle_exercises_20260824/Geometry8_Circle_Exercises_Workshop_20260824_V5_LargeText_QA.py#' \
  "$TMP"
sed -i \
  's#CLASS=Geometry8CircleExercisesWorkshop20260824#CLASS=Geometry8CircleExercisesWorkshop20260824V5LargeTextQA#' \
  "$TMP"
bash "$TMP"
