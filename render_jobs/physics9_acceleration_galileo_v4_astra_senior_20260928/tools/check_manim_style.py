#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ABSOLUTE_PATHS = [
    re.compile(r"[A-Za-z]:\\\\"),
    re.compile(r"/Users/"),
    re.compile(r"/home/[^/]+/"),
]

FAIL = []


def call_name(node: ast.Call) -> str:
    f = node.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return ""


def int_arg(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, int) else None


files = [Path(p) for p in sys.argv[1:]]
if not files:
    raise SystemExit("usage: check_manim_style.py FILE [FILE ...]")

all_source = ""
for path in files:
    source = path.read_text(encoding="utf-8")
    all_source += "\n" + source
    tree = ast.parse(source)

    for pattern in ABSOLUTE_PATHS:
        if pattern.search(source):
            FAIL.append(f"{path}: absolute machine-specific path detected")

    if re.search(r"\b(?:RED|BLUE|GREEN|YELLOW|PURPLE|ORANGE)\b", source):
        FAIL.append(f"{path}: non-monochrome emphasis constant detected")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = call_name(node)

        if name == "text" and len(node.args) >= 2:
            size = int_arg(node.args[1])
            if size is not None and size < 18:
                FAIL.append(f"{path}:{node.lineno}: text font size {size} < 18")

        if name == "MathTex":
            size = None
            for kw in node.keywords:
                if kw.arg == "font_size":
                    size = int_arg(kw.value)
            if size is not None and size < 36:
                FAIL.append(f"{path}:{node.lineno}: MathTex font size {size} < 36")

required = [
    "class Physics9AccelerationGalileoV4AstraSenior",
    "validate_lesson_data",
    "MOTION ↔ v(t)",
    "SLOPE ↔ ACCELERATION",
    "BUILD a(t): 0–60 min",
    "BUILD a(t): 60–120 min",
    "READ a(t)",
    "DERIVE  v = v₀ + at",
    "AREA → POSITION",
    "WHY GALILEO USED A RAMP",
    "TEST  x ∝ t²",
    "one focus state on screen at a time",
    "a SIGN ≠ MOTION DIRECTION",
    "For a rolling ball, the exact a depends on rotational inertia.",
    r"x-x_0=\left(\frac a2\right)t^2",
]
for item in required:
    if item not in all_source:
        FAIL.append(f"missing ASTRA contract element: {item}")

if "note_panel(" in all_source:
    FAIL.append("legacy note_panel usage detected in ASTRA V4 modules")

if FAIL:
    print("ASTRA STYLE QA: FAIL")
    for item in FAIL:
        print("FAIL:", item)
    raise SystemExit(1)

print("PASS: ASTRA senior structural/style checks passed.")
