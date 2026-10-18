#!/usr/bin/env bash
# usage: tools/render.sh <spec.json> <name> <ql|qm|qh> [problems] [fps]
set -euo pipefail
cd "$(dirname "$0")/.."
SPEC=$1; NAME=$2; Q=${3:-qh}; PROBS=${4:-}; FPS=${5:-30}
PY=${P2V_PY:-python}
OUT=build/$NAME
mkdir -p "$OUT"
P2V_SPEC=$SPEC P2V_PROBLEMS=$PROBS P2V_OUT=$OUT "$(dirname "$PY")/manim" -$Q --fps "$FPS" --media_dir "$OUT/media" -o "$NAME" pdf2video/render/scene.py SolutionVideo > "$OUT/render.log" 2>&1
find "$OUT/media/videos" -name "$NAME.mp4" -exec cp {} "$OUT/$NAME.mp4" \;
echo "done $OUT/$NAME.mp4"
