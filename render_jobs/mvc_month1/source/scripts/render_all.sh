#!/usr/bin/env bash
set -euo pipefail

SCENES=(
  "scenes/week1_vectors.py W1_VectorBridge2D3D 01_vector_bridge_2d_3d"
  "scenes/week1_vectors.py W1_DotProductProjection 02_dot_product_projection"
  "scenes/week2_geometry3d.py W2_CrossProductArea 03_cross_product_area"
  "scenes/week2_geometry3d.py W2_LinesPlanesIntersection 04_lines_planes_intersection"
  "scenes/week3_functions.py W3_SurfaceToContours 05_surface_to_contours"
  "scenes/week3_functions.py W3_PathDependentLimit 06_path_dependent_limit"
  "scenes/week4_derivatives.py W4_PartialDerivativeSlices 07_partial_derivative_slices"
  "scenes/week4_derivatives.py W4_GradientAndTangentPlane 08_gradient_tangent_plane"
)

rm -rf delivery
mkdir -p delivery/videos delivery/code delivery/logs
: > delivery/render_commands.txt

for item in "${SCENES[@]}"; do
  read -r file scene out <<<"$item"
  command="manim -pqh $file $scene --format=mp4 --disable_caching"
  echo "$command" | tee -a delivery/render_commands.txt
  manim -pqh "$file" "$scene" --format=mp4 --disable_caching 2>&1 | tee "delivery/logs/${out}.log"

  video="$(find media -type f -name "${scene}.mp4" -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
  test -n "$video"
  test -s "$video"
  cp "$video" "delivery/videos/${out}_pqh.mp4"
done

cp mvc_manim_library.py manim.cfg requirements.txt README.md COURSE_MAP.md delivery/code/
cp -r scenes scripts delivery/code/

find "$PWD/delivery/videos" -maxdepth 1 -type f -name '[0-9][1-9]_*.mp4' \
  | sort \
  | sed "s#^#file '#" \
  | sed "s#$#'#" \
  > delivery/concat.txt

test "$(wc -l < delivery/concat.txt)" -eq 8

ffmpeg -y -f concat -safe 0 -i delivery/concat.txt -c copy \
  delivery/videos/00_month1_compilation_pqh.mp4 || \
ffmpeg -y -f concat -safe 0 -i delivery/concat.txt \
  -c:v libx264 -pix_fmt yuv420p -r 30 \
  delivery/videos/00_month1_compilation_pqh.mp4

test -s delivery/videos/00_month1_compilation_pqh.mp4
find delivery/videos delivery/code -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > delivery/SHA256SUMS.txt
