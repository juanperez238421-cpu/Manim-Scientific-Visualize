"""Structured return objects used by the visual helpers."""
from __future__ import annotations
from dataclasses import dataclass
from manim import Mobject, Rectangle, RoundedRectangle, VGroup

@dataclass
class TableDiagram:
    group: VGroup
    rectangles: list[list[Rectangle]]
    entries: list[list[Mobject]]
    rows: list[VGroup]
    columns: list[VGroup]
    header: VGroup
    body: VGroup

@dataclass
class FigurePanel:
    group: VGroup
    box: RoundedRectangle
    figure: Mobject
    title: Mobject | None
    caption: Mobject | None

@dataclass
class SplitLayout:
    group: VGroup
    left: Mobject
    right: Mobject
