"""Custom table system with independently addressable cells."""
from __future__ import annotations
from collections.abc import Sequence
from manim import *
from .models import TableDiagram
from .theme import *

class TablesMixin:
    def build_table(self, headers: Sequence[str], body_rows: Sequence[Sequence[str]],
                    column_widths: Sequence[float] | None = None, math_columns: Sequence[int] = (),
                    row_height: float = 0.70, header_height: float = 0.78,
                    body_font_size: int = 27, header_font_size: int = 24) -> TableDiagram:
        data = [list(headers), *[list(r) for r in body_rows]]
        cols = len(headers)
        if any(len(r) != cols for r in data):
            raise ValueError("All table rows must match header length")
        widths = list(column_widths or [2.4] * cols)
        if len(widths) != cols:
            raise ValueError("column_widths length mismatch")
        rectangles: list[list[Rectangle]] = []
        entries: list[list[Mobject]] = []
        rows: list[VGroup] = []
        y = 0.0
        for r, values in enumerate(data):
            h = header_height if r == 0 else row_height
            x = -sum(widths) / 2
            rect_row, entry_row = [], []
            row_group = VGroup()
            for c, (value, width) in enumerate(zip(values, widths)):
                rect = Rectangle(width=width, height=h, stroke_color=LIGHT_GRAY, stroke_width=1.4,
                    fill_color=VERY_LIGHT_GRAY if r == 0 else WHITE_FILL, fill_opacity=1)
                rect.move_to([x + width/2, y - h/2, 0])
                entry = (self.math(value, body_font_size) if c in math_columns and r > 0
                         else self.text(value, header_font_size if r == 0 else body_font_size, BOLD if r == 0 else NORMAL))
                self.fit(entry, width - 0.22, h - 0.16).move_to(rect)
                rect_row.append(rect); entry_row.append(entry); row_group.add(rect, entry)
                x += width
            rectangles.append(rect_row); entries.append(entry_row); rows.append(row_group)
            y -= h
        group = VGroup(*rows).move_to(ORIGIN)
        columns = [VGroup(*[VGroup(rectangles[r][c], entries[r][c]) for r in range(len(rows))]) for c in range(cols)]
        header = rows[0]
        body = VGroup(*rows[1:])
        return TableDiagram(group, rectangles, entries, rows, columns, header, body)

    def shade_cells(self, table: TableDiagram, cells: Sequence[tuple[int, int]], color=VERY_LIGHT_GRAY):
        return AnimationGroup(*[table.rectangles[r][c].animate.set_fill(color, opacity=1) for r, c in cells])

    def animate_table_rows(self, table: TableDiagram, include_header: bool = True, pause: float = PAUSE_SHORT) -> None:
        start = 0 if include_header else 1
        for row in table.rows[start:]:
            self.play(FadeIn(row, shift=UP*0.05), run_time=RUN_QUICK)
            self.wait(pause)
