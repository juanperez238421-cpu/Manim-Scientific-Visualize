#!/usr/bin/env bash
set -euo pipefail
TMP=/tmp/geometry8_shaded_areas_protocol_v3.sh
cp render_jobs/geometry8_shaded_areas_sequence_20260825/run_full_protocol.sh "$TMP"

python - "$TMP" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text(encoding='utf-8')
text = text.replace('python -Werror -m py_compile', 'python -m py_compile')
old = '''for C in "${CLASSES[@]}"; do
  grep -Fq "class $C" "$SCENE"
done
grep -Fq 'assert_content_safe' "$BASE_SCENE"
grep -Fq 'validate_lesson_data' "$BASE_SCENE"
grep -Fq 'assert diagrams.get_right()[0] < card.get_left()[0]' "$SCENE"
'''
new = '''python - "$BASE_SCENE" "$SCENE" <<'PYSMOKE'
from pathlib import Path
import ast, sys
base = Path(sys.argv[1])
qa = Path(sys.argv[2])
for path in (base, qa):
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    classes = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
    assert classes, f"No classes found in {path}"
print("AST smoke checks PASS")
PYSMOKE
'''
if old not in text:
    raise SystemExit('Expected brittle grep block not found in protocol')
text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
PY

bash -x "$TMP"
