#!/usr/bin/env python3
"""Static QA checker for JP Manim Classroom Standard lessons."""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

ABSOLUTE_PATH_PATTERNS=[re.compile(r"[A-Za-z]:[\\/]"),re.compile(r"/Users/"),re.compile(r"/home/[^/]+/")]
RENDER_CONFIG_ATTRS={"pixel_width","pixel_height","frame_rate"}
VALID_BASES={"JPClassroomScene","JPMathClassroomScene","JPThreeDClassroomScene"}

def base_names(node: ast.ClassDef)->set[str]:
    out=set()
    for base in node.bases:
        if isinstance(base,ast.Name): out.add(base.id)
        elif isinstance(base,ast.Attribute): out.add(base.attr)
    return out

def main(path_str: str)->int:
    path=Path(path_str)
    if not path.is_file(): print(f"FAIL: file does not exist: {path}"); return 2
    source=path.read_text(encoding="utf-8")
    try: tree=ast.parse(source,filename=str(path))
    except SyntaxError as exc: print(f"FAIL: syntax error: {exc}"); return 2
    failures=[]; warnings=[]
    classes=[n for n in ast.walk(tree) if isinstance(n,ast.ClassDef)]
    if not [n for n in classes if base_names(n)&VALID_BASES]: failures.append("No class inherits from the JP classroom base classes.")
    if "validate_lesson_data" not in source: warnings.append("No validate_lesson_data() hook found.")
    if "set_header(" not in source and "standard_opening(" not in source: warnings.append("No standard opening/header helper detected.")
    if "clear_stage(" not in source and "standard_closing(" not in source: warnings.append("No stage cleanup/closing helper detected.")
    if any(p.search(source) for p in ABSOLUTE_PATH_PATTERNS): failures.append("Absolute user/system path detected; assets must be project-relative.")
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Attribute) and isinstance(target.value,ast.Name) and target.value.id=="config" and target.attr in RENDER_CONFIG_ATTRS:
                    failures.append(f"Lesson overrides config.{target.attr}; keep resolution/FPS in the render layer so preview optimization works.")
    if any(token in source for token in ("RED","BLUE","GREEN")): warnings.append("Colored emphasis detected; default standard is monochrome unless pedagogically justified.")
    for cls in classes:
        for item in cls.body:
            if isinstance(item,ast.FunctionDef) and item.name=="construct":
                line_count=(item.end_lineno or item.lineno)-item.lineno+1
                if line_count>80: warnings.append(f"{cls.name}.construct is {line_count} lines; prefer orchestration + section methods.")
    print(f"JP MANIM STYLE QA: {path}")
    for msg in failures: print(f"FAIL: {msg}")
    for msg in warnings: print(f"WARN: {msg}")
    if failures: return 1
    print("PASS" if not warnings else "PASS WITH WARNINGS"); return 0

if __name__=="__main__":
    if len(sys.argv)!=2: print("Usage: python tools/check_style.py <lesson.py>"); raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
