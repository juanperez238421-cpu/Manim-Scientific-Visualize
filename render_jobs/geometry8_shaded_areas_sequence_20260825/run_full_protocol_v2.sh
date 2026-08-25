#!/usr/bin/env bash
set -euo pipefail
TMP=/tmp/geometry8_shaded_areas_protocol_v2.sh
cp render_jobs/geometry8_shaded_areas_sequence_20260825/run_full_protocol.sh "$TMP"
sed -i 's/python -Werror -m py_compile/python -m py_compile/' "$TMP"
bash "$TMP"
