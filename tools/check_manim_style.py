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

TEACHING_TEXT_MIN = 23
GRAPH_TICK_MIN = 18
FORMULA_MIN = 29


def class_base_names(node: ast.ClassDef) -> set[str]:
    names: set[str] = set()
    for base in node.bases:
        if isinstance(base, ast.Name):
            names.add(base.id)
        elif isinstance(base, ast.Attribute):
            names.add(base.attr)
    return names


def _numeric_arg(call: ast.Call, index: int) -> int | float | None:
    if len(call.args) <= index:
        return None
    node = call.args[index]
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    return None


def audit_typography(tree: ast.AST, failures: list[str], warnings: list[str]) -> None:
    """Detect explicit font-size regressions in lesson source."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id
        else:
            func_name = None

        if func_name == "text":
            size = _numeric_arg(node, 1)
            if size is not None:
                if size < GRAPH_TICK_MIN:
                    failures.append(f"Line {node.lineno}: Text size {size} < {GRAPH_TICK_MIN}.")
                elif size < TEACHING_TEXT_MIN:
                    warnings.append(
                        f"Line {node.lineno}: Text size {size} is secondary-label territory; "
                        "do not use it for teaching-critical prose."
                    )

        if func_name == "math":
            size = _numeric_arg(node, 1)
            if size is not None and size < FORMULA_MIN:
                warnings.append(
                    f"Line {node.lineno}: Math size {size} < {FORMULA_MIN}; "
                    "reserve it for compact labels, not derivations."
                )

        if func_name in {"Tex", "Text", "MathTex"}:
            for keyword in node.keywords:
                if keyword.arg == "font_size" and isinstance(keyword.value, ast.Constant):
                    value = keyword.value.value
                    if isinstance(value, (int, float)) and value < GRAPH_TICK_MIN:
                        failures.append(
                            f"Line {node.lineno}: explicit font_size {value} < {GRAPH_TICK_MIN}."
                        )


def audit_layout_contract(source: str, failures: list[str], warnings: list[str]) -> None:
    if "text_block(" not in source:
        warnings.append("No text_block() usage detected; long prose should wrap instead of silently shrinking.")
    if "assert_content_safe(" not in source and "assert_text_safe(" not in source:
        warnings.append("No explicit runtime safe-margin assertion detected in lesson source.")

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

    audit_typography(tree, failures, warnings)
    audit_layout_contract(source, failures, warnings)

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