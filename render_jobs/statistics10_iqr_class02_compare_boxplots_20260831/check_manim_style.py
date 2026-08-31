#!/usr/bin/env python3
"""Static QA checker for JP Classroom Manim Standard lesson files."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:[\\/]") ,
    re.compile(r"/Users/"),
    re.compile(r"/home/[^/]+/"),
]


def class_base_names(node: ast.ClassDef) -> set[str]:
    names: set[str] = set()
    for base in node.bases:
        if isinstance(base, ast.Name):
            names.add(base.id)
        elif isinstance(base, ast.Attribute):
            names.add(base.attr)
    return names


def main(path_str: str) -> int:
    path = Path(path_str)
    if not path.exists():
        print(f"FAIL: file does not exist: {path}")
        return 2

    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        print(f"FAIL: syntax error: {exc}")
        return 2

    failures: list[str] = []
    warnings: list[str] = []

    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    classroom_classes = [
        node for node in classes
        if class_base_names(node) & {
            "JPClassroomScene",
            "JPMathClassroomScene",
            "JPThreeDClassroomScene",
        }
    ]
    if not classroom_classes:
        warnings.append("No class inherits from the consolidated JP classroom base.")

    if "validate_lesson_data" not in source:
        warnings.append("No validate_lesson_data() hook found.")

    if "set_header(" not in source and "standard_opening(" not in source:
        warnings.append("No standard header/opening helper detected.")

    if "clear_stage(" not in source and "standard_closing(" not in source:
        warnings.append("No clear_stage()/standard_closing() helper detected.")

    for pattern in ABSOLUTE_PATH_PATTERNS:
        if pattern.search(source):
            failures.append("Absolute user/system path detected; assets must be project-relative.")
            break

    # Direct style regressions that often break consistency.
    if re.search(r"background_color\s*=\s*[\"']?(?!WHITE|#ffffff|#FFFFFF)", source):
        warnings.append("Review non-standard background_color assignment.")

    if "RED" in source or "BLUE" in source or "GREEN" in source:
        warnings.append("Colored emphasis detected. Standard default is monochrome unless explicitly requested.")

    # Heuristic for giant monolithic construct methods.
    for node in classes:
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "construct":
                line_count = (item.end_lineno or item.lineno) - item.lineno + 1
                if line_count > 80:
                    warnings.append(
                        f"{node.name}.construct is {line_count} lines; prefer orchestration + section methods."
                    )

    print(f"STYLE QA: {path}")
    if failures:
        for message in failures:
            print(f"FAIL: {message}")
    if warnings:
        for message in warnings:
            print(f"WARN: {message}")
    if not failures and not warnings:
        print("PASS: no structural/style issues detected.")
    elif not failures:
        print("PASS WITH WARNINGS")

    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/check_manim_style.py <lesson.py>")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
