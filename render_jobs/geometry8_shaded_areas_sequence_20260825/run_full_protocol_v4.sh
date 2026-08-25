#!/usr/bin/env bash
set -euo pipefail
TMP=/tmp/geometry8_shaded_areas_protocol_v4.sh
cp render_jobs/geometry8_shaded_areas_sequence_20260825/run_full_protocol.sh "$TMP"
python - "$TMP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
t=p.read_text()
t=t.replace('python -Werror -m py_compile','python -m py_compile')
start='for C in "${CLASSES[@]}"; do\n'
end="grep -Fq 'assert diagrams.get_right()[0] < card.get_left()[0]' \"$SCENE\"\n"
i=t.index(start); j=t.index(end,i)+len(end)
t=t[:i]+'''python - "$BASE_SCENE" "$SCENE" <<'PYSMOKE'\nfrom pathlib import Path\nimport ast, sys\nfor arg in sys.argv[1:]:\n    path=Path(arg)\n    tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))\n    assert any(isinstance(n,ast.ClassDef) for n in ast.walk(tree))\nprint("AST smoke checks PASS")\nPYSMOKE\n'''+t[j:]
t=t.replace('pdflatex -interaction=nonstopmode -halt-on-error -output-directory out "$JOB/Geometry8_Shaded_Areas_Workshop_Student.tex" > out/STUDENT_PDF_BUILD.log','pdflatex -interaction=nonstopmode -halt-on-error -output-directory out "$JOB/Geometry8_Shaded_Areas_Workshop_Student.tex" 2>&1 | tee out/STUDENT_PDF_BUILD.log')
t=t.replace('pdflatex -interaction=nonstopmode -halt-on-error -output-directory out "$JOB/Geometry8_Shaded_Areas_Workshop_Teacher_Key.tex" > out/TEACHER_KEY_PDF_BUILD.log','pdflatex -interaction=nonstopmode -halt-on-error -output-directory out "$JOB/Geometry8_Shaded_Areas_Workshop_Teacher_Key.tex" 2>&1 | tee out/TEACHER_KEY_PDF_BUILD.log')
p.write_text(t)
PY
bash -x "$TMP"
