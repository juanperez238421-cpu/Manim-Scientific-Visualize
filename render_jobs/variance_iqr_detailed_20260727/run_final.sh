#!/usr/bin/env bash
set -euo pipefail

SCRIPT="render_jobs/variance_workshop_20260726/run_render.sh"
python - "$SCRIPT" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
old = "962faaae40ddd631abebc1b0b8dea7402c3bd34450fd0e51d2644bc22990430f"
new = "e251a66dfc8685f3a43bc8ace8dfab7df664133c297e4e157b7e2dbb3e06c558"
if source.count(old) != 1:
    raise RuntimeError("Expected one detailed-IQR source hash in render script")
path.write_text(source.replace(old, new), encoding="utf-8")
PY

bash "$SCRIPT"
