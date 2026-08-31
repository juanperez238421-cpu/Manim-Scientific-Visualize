#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fixed seating plan — Physics Laboratory — Group 8B.

Built with the consolidated JP Classroom ManimCE style and designed as the
base template for the remaining groups.

Render target: ManimCE 0.20.1, 1920x1080, 30 fps.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
from manim import *

from library.jp_classroom_style import *


# =============================================================================
# AUTHORITATIVE CLASS DATA
# =============================================================================
STUDENTS: List[str] = [
    "ARIZA MORALES SAMUEL",
    "ARROYAVE ECHAVARRIA PABL...",
    "CARDONA VELASQUEZ ALICIA",
    "CARREÑO MONSALVE NICOLAS",
    "DUQUE BETANCUR EMILIANO",
    "ECHEVERRI URIBE MATIAS",
    "GAVIRIA TORRES ANTONIO",
    "GIRALDO ZORA SAMUEL",
    "HENAO OSORIO LUCIA",
    "HOYOS URIBE MATIAS",
    "JACQUES DE DIXMUDE VALLE...",
    "JARAMILLO ECHEVERRY ANTO...",
    "JIMENEZ VILLADA FRANCO",
    "MARIN ARISTIZABAL FEDERI...",
    "MAZO LOPEZ MANUELA",
    "MONCADA ESTRADA MARIA AN...",
    "PARRA DIAZ NICOLAS",
    "PEREZ JARAMILLO VIOLETA",
    "RAMIREZ GARCIA MARTINA",
    "RIVERA PERDOMO SALOME",
    "SANCHEZ CASTRO MARTIN",
    "ZAPATA ALARCON MARIA ANT...",
    "ZAPATA CADENA SAMUEL ALE...",
]

SEAT_LETTERS = ("A", "B", "C")

# Actual room disposition from the laboratory top-view map.
# Coordinates are local to the room diagram and keep the real visual order:
# top: PC09, PC06, PC03; middle: PC08, PC05, PC02; bottom: PC07, PC04, PC01.
PC_POSITIONS: Dict[int, Tuple[float, float]] = {
    9: (-2.75, 1.55), 6: (0.0, 1.55), 3: (2.75, 1.55),
    8: (-2.75, 0.00), 5: (0.0, 0.00), 2: (2.75, 0.00),
    7: (-2.75, -1.55), 4: (0.0, -1.55), 1: (2.75, -1.55),
}

ASSIGNMENTS: List[Tuple[int, str, int, str]] = []
for student_number, name in enumerate(STUDENTS, start=1):
    pc = ((student_number - 1) // 3) + 1
    seat = SEAT_LETTERS[(student_number - 1) % 3]
    ASSIGNMENTS.append((student_number, name, pc, seat))

AVAILABLE = [
    "PC08-C",
    "PC09-A", "PC09-B", "PC09-C",
]


# =============================================================================
# SMALL STRUCTURED COMPONENTS
# =============================================================================
@dataclass
class LabDiagram:
    group: VGroup
    desks: Dict[int, VGroup]
    seat_points: Dict[Tuple[int, str], np.ndarray]
    seat_outlines: Dict[Tuple[int, str], Circle]


def validate_roster() -> None:
    assert len(STUDENTS) == 23
    assert len(ASSIGNMENTS) == 23
    assert ASSIGNMENTS[0][2:] == (1, "A")
    assert ASSIGNMENTS[-1][2:] == (8, "B")
    assert len(AVAILABLE) == 4
    assert len(set(STUDENTS)) == len(STUDENTS)
    assert set(PC_POSITIONS.keys()) == set(range(1, 10))


# =============================================================================
# MAIN SCENE
# =============================================================================
class Lab8BFixedSeating(JPMathClassroomScene):
    """Animated fixed seating plan for group 8B."""

    def validate_lesson_data(self) -> None:
        validate_roster()

    def construct(self) -> None:
        self.opening()
        self.room_orientation()
        self.assignment_sequence()
        self.empty_positions()
        self.behavior_rules()
        self.final_map()

    # ------------------------------------------------------------------
    # Reusable drawing helpers
    # ------------------------------------------------------------------
    def make_lab_diagram(self, scale: float = 1.0) -> LabDiagram:
        room = RoundedRectangle(
            width=8.95,
            height=5.45,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )

        board = Rectangle(
            width=3.35,
            height=0.26,
            stroke_color=BLACK_LINE,
            stroke_width=1.3,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        ).move_to([0, -2.42, 0])
        board_label = self.text("TABLERO", 14, BOLD).move_to(board)

        teacher = RoundedRectangle(
            width=1.65,
            height=0.48,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=1.2,
            fill_color=PAPER_GRAY,
            fill_opacity=1.0,
        ).move_to([0.10, -2.00, 0])
        teacher_label = self.text("DOCENTE", 13, BOLD).move_to(teacher)

        entrance = VGroup(
            Line([3.45, 2.69, 0], [4.15, 2.69, 0], color=BLACK_LINE, stroke_width=2),
            self.text("ENTRADA", 13, BOLD).move_to([3.80, 2.48, 0]),
        )

        shelf_left = Rectangle(
            width=0.28,
            height=3.55,
            stroke_color=BLACK_LINE,
            stroke_width=1.2,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        ).move_to([-4.18, 0.15, 0])
        shelf_right = shelf_left.copy().move_to([4.18, 0.15, 0])
        left_label = self.text("REPISAS", 11, BOLD).rotate(PI / 2).move_to(shelf_left)
        right_label = self.text("REPISAS", 11, BOLD).rotate(-PI / 2).move_to(shelf_right)

        desks: Dict[int, VGroup] = {}
        seat_points: Dict[Tuple[int, str], np.ndarray] = {}
        seat_outlines: Dict[Tuple[int, str], Circle] = {}
        desk_groups = VGroup()

        for pc in range(1, 10):
            x, y = PC_POSITIONS[pc]
            desk = RoundedRectangle(
                width=2.05,
                height=1.05,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.35,
                fill_color=PAPER_GRAY,
                fill_opacity=1.0,
            ).move_to([x, y, 0])
            monitor = Rectangle(
                width=0.58,
                height=0.25,
                stroke_color=BLACK_LINE,
                stroke_width=1.1,
                fill_color=WHITE_FILL,
                fill_opacity=1.0,
            ).move_to([x, y + 0.23, 0])
            pc_label = self.text(f"PC {pc:02d}", 14, BOLD).move_to([x, y + 0.43, 0])

            seat_group = VGroup()
            for idx, seat in enumerate(SEAT_LETTERS):
                sx = x + (idx - 1) * 0.57
                sy = y - 0.34
                circle = Circle(
                    radius=0.19,
                    stroke_color=BLACK_LINE,
                    stroke_width=1.1,
                    fill_opacity=0,
                ).move_to([sx, sy, 0])
                letter = self.text(seat, 11, BOLD).next_to(circle, DOWN, buff=0.035)
                seat_group.add(circle, letter)
                seat_points[(pc, seat)] = np.array([sx, sy, 0])
                seat_outlines[(pc, seat)] = circle

            group = VGroup(desk, monitor, pc_label, seat_group)
            desks[pc] = group
            desk_groups.add(group)

        orientation = VGroup(
            self.text("PC09   PC06   PC03", 12, BOLD).move_to([0, 2.31, 0]),
            self.text("PC08   PC05   PC02", 12, BOLD).move_to([0, 0.77, 0]),
            self.text("PC07   PC04   PC01", 12, BOLD).move_to([0, -0.78, 0]),
        ).set_opacity(0)

        group = VGroup(
            room,
            board,
            board_label,
            teacher,
            teacher_label,
            entrance,
            shelf_left,
            shelf_right,
            left_label,
            right_label,
            desk_groups,
            orientation,
        )
        group.scale(scale)

        if scale != 1.0:
            seat_points = {key: point * scale for key, point in seat_points.items()}

        return LabDiagram(group, desks, seat_points, seat_outlines)

    def seat_marker(self, number: int, point: np.ndarray, scale: float = 1.0) -> VGroup:
        circle = Circle(
            radius=0.18 * scale,
            stroke_color=BLACK_LINE,
            stroke_width=1.3,
            fill_color=BLACK_LINE,
            fill_opacity=1.0,
        ).move_to(point)
        label = Text(
            str(number),
            font_size=max(12, int(18 * scale)),
            color=WHITE,
            weight=BOLD,
        ).move_to(circle)
        return VGroup(circle, label)

    def workstation_panel(self, pc: int, entries: List[Tuple[int, str, str]]) -> VGroup:
        title = self.text(f"PC {pc:02d} · 3 PUESTOS", 27, BOLD)
        rows = VGroup()
        for number, name, seat in entries:
            badge = Circle(
                radius=0.22,
                stroke_color=BLACK_LINE,
                stroke_width=1.4,
                fill_color=BLACK_LINE,
                fill_opacity=1.0,
            )
            badge_text = Text(str(number), font_size=18, color=WHITE, weight=BOLD).move_to(badge)
            seat_box = RoundedRectangle(
                width=1.05,
                height=0.46,
                corner_radius=0.07,
                stroke_color=BLACK_LINE,
                stroke_width=1.2,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1.0,
            )
            seat_text = self.text(f"PC{pc:02d}-{seat}", 16, BOLD).move_to(seat_box)
            name_mob = self.text(name, 18, MEDIUM)
            self.fit(name_mob, 4.6, 0.45)
            row = VGroup(VGroup(badge, badge_text), name_mob, VGroup(seat_box, seat_text))
            row.arrange(RIGHT, buff=0.18)
            rows.add(row)
        if pc == 8:
            free_badge = Circle(
                radius=0.22,
                stroke_color=BLACK_LINE,
                stroke_width=1.4,
                fill_opacity=0,
            )
            free_mark = self.text("—", 18, BOLD).move_to(free_badge)
            free_box = RoundedRectangle(
                width=1.05,
                height=0.46,
                corner_radius=0.07,
                stroke_color=BLACK_LINE,
                stroke_width=1.2,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1.0,
            )
            free_code = self.text("PC08-C", 16, BOLD).move_to(free_box)
            free_name = self.text("PUESTO DISPONIBLE", 18, MEDIUM)
            self.fit(free_name, 4.6, 0.45)
            rows.add(VGroup(VGroup(free_badge, free_mark), free_name, VGroup(free_box, free_code)).arrange(RIGHT, buff=0.18))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.30)

        rule = Line(LEFT * 2.65, RIGHT * 2.65, color=LIGHT_GRAY, stroke_width=1.5)
        content = VGroup(title, rule, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        self.fit(content, 5.35, 4.20)
        box = RoundedRectangle(
            width=5.70,
            height=4.80,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
        return VGroup(box, content)

    def forbidden_icon(self, symbol: Mobject, label: str) -> VGroup:
        ring = Circle(radius=0.55, stroke_color=BLACK_LINE, stroke_width=2.2)
        slash = Line(DL * 0.43, UR * 0.43, color=BLACK_LINE, stroke_width=3.0)
        self.fit(symbol, 0.65, 0.65)
        symbol.move_to(ring)
        icon = VGroup(ring, symbol, slash)
        text = self.text(label, 21, BOLD)
        self.fit(text, 3.3, 0.70)
        return VGroup(icon, text).arrange(DOWN, buff=0.18)

    # ------------------------------------------------------------------
    # Scene sections
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "GRUPO 8B · LABORATORIO DE FÍSICA",
            "UBICACIÓN FIJA EN EL LABORATORIO",
            "23 estudiantes · 9 computadores · 3 puestos por computador",
            "Cada estudiante tendrá un puesto estable, fácil de identificar por número de lista.",
        )

    def room_orientation(self) -> None:
        self.set_header(
            1,
            "PRIMERO: LEER LA DISPOSICIÓN REAL DEL LABORATORIO",
            "La numeración de los computadores se conserva exactamente como aparece en el aula: PC01 abajo a la derecha y PC09 arriba a la izquierda.",
        )

        lab = self.make_lab_diagram(scale=0.98)
        lab.group.move_to(DOWN * 0.45)
        note = self.note_panel(
            "CRITERIO FIJO",
            [
                "Orden de lista: 1 → 23",
                "Computadores: PC01 → PC09",
                "Dentro de cada PC: silla A → B → C",
                "Los puestos no cambian entre clases.",
            ],
            width=5.3,
            title_size=25,
            body_size=21,
        )
        layout = self.split_layout(lab.group, note, left_width=8.8, right_width=5.2, max_height=5.25, center_y=-0.55)
        self.assert_content_safe(layout.group, "room orientation")

        self.play(FadeIn(lab.group), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(note, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        for pc in range(1, 10):
            focus = SurroundingRectangle(lab.desks[pc], buff=0.05, color=BLACK_LINE, stroke_width=2.4)
            self.play(Create(focus), run_time=0.28)
            self.wait(0.15)
            self.play(FadeOut(focus), run_time=0.20)

        self.wait(PAUSE_READ)
        self.clear_stage()

    def assignment_sequence(self) -> None:
        self.set_header(
            2,
            "ASIGNACIÓN 8B: TRES ESTUDIANTES POR COMPUTADOR",
            "La animación avanza PC por PC. El número dentro del círculo corresponde al número oficial del estudiante en la lista de 8B.",
        )

        lab = self.make_lab_diagram(scale=0.90)
        lab.group.move_to(LEFT * 3.25 + DOWN * 0.55)
        self.play(FadeIn(lab.group), run_time=RUN_NORMAL)

        lab_shift = lab.group.get_center()
        seat_scene_points: Dict[Tuple[int, str], np.ndarray] = {}
        for (pc, seat), local_point in lab.seat_points.items():
            seat_scene_points[(pc, seat)] = local_point + lab_shift

        all_markers = VGroup()
        current_panel = None

        for pc in range(1, 9):
            group_entries = []
            for number, name, assn_pc, seat in ASSIGNMENTS:
                if assn_pc == pc:
                    group_entries.append((number, name, seat))

            panel = self.workstation_panel(pc, group_entries)
            panel.move_to(RIGHT * 4.55 + DOWN * 0.55)

            highlight = SurroundingRectangle(
                lab.desks[pc],
                buff=0.06,
                color=BLACK_LINE,
                stroke_width=2.8,
            )

            if current_panel is None:
                self.play(FadeIn(panel, shift=LEFT * 0.12), Create(highlight), run_time=RUN_NORMAL)
            else:
                self.play(ReplacementTransform(current_panel, panel), Create(highlight), run_time=RUN_NORMAL)
            current_panel = panel

            for number, name, seat in group_entries:
                marker = self.seat_marker(number, seat_scene_points[(pc, seat)], scale=0.90)
                all_markers.add(marker)
                self.play(GrowFromCenter(marker), run_time=0.55)
                self.wait(0.45)

            self.wait(1.15)
            self.play(FadeOut(highlight), run_time=0.35)

        self.wait(PAUSE_EXPLAIN)
        if current_panel is not None:
            self.play(FadeOut(current_panel), run_time=RUN_NORMAL)

        summary = self.note_panel(
            "RESULTADO",
            [
                "Estudiantes 1–3   → PC01",
                "Estudiantes 4–6   → PC02",
                "Estudiantes 7–9   → PC03",
                "Estudiantes 10–12 → PC04",
                "Estudiantes 13–15 → PC05",
                "Estudiantes 16–18 → PC06",
                "Estudiantes 19–21 → PC07",
                "Estudiantes 22–23 → PC08",
            ],
            width=5.35,
            title_size=25,
            body_size=19,
            max_text_height=4.15,
        )
        summary.move_to(RIGHT * 4.55 + DOWN * 0.55)
        self.play(FadeIn(summary), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def empty_positions(self) -> None:
        self.set_header(
            3,
            "PUESTOS QUE QUEDAN DISPONIBLES",
            "Con 23 estudiantes quedan libres cuatro puestos: PC08-C y los tres puestos de PC09; estos espacios solo se usarán si el docente lo indica.",
        )

        lab = self.make_lab_diagram(scale=0.92)
        lab.group.move_to(LEFT * 2.75 + DOWN * 0.55)

        assigned_markers = VGroup()
        shift = lab.group.get_center()
        for number, _name, pc, seat in ASSIGNMENTS:
            point = lab.seat_points[(pc, seat)] + shift
            assigned_markers.add(self.seat_marker(number, point, scale=0.92))

        available_cards = VGroup()
        for code in AVAILABLE:
            box = RoundedRectangle(
                width=2.05,
                height=0.58,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.4,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1.0,
            )
            label = self.text(code, 20, BOLD).move_to(box)
            available_cards.add(VGroup(box, label))
        available_cards.arrange_in_grid(cols=2, buff=(0.20, 0.20))
        available_title = self.text("4 PUESTOS DISPONIBLES", 25, BOLD)
        available_panel = VGroup(available_title, available_cards).arrange(DOWN, buff=0.32)
        available_panel.move_to(RIGHT * 4.85 + DOWN * 0.55)

        self.play(FadeIn(lab.group), FadeIn(assigned_markers), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        for pc in (8, 9):
            focus = SurroundingRectangle(lab.desks[pc], buff=0.06, color=BLACK_LINE, stroke_width=2.8)
            self.play(Create(focus), run_time=RUN_NORMAL)
            self.wait(PAUSE_EXPLAIN)
            self.play(FadeOut(focus), run_time=RUN_QUICK)

        self.play(FadeIn(available_panel, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def behavior_rules(self) -> None:
        self.set_header(
            4,
            "NORMAS BÁSICAS DE COMPORTAMIENTO",
            "El puesto fijo facilita el cuidado del laboratorio: cada estudiante responde por su computador, su silla y el material que utiliza.",
        )

        phone = VGroup(
            RoundedRectangle(width=0.33, height=0.62, corner_radius=0.05, stroke_color=BLACK_LINE, stroke_width=1.8),
            Dot(DOWN * 0.22, radius=0.025, color=BLACK_LINE),
        )
        food = VGroup(
            Rectangle(width=0.48, height=0.30, stroke_color=BLACK_LINE, stroke_width=1.8),
            Line(UP * 0.15, UP * 0.43 + RIGHT * 0.20, color=BLACK_LINE, stroke_width=1.8),
        )

        no_phone = self.forbidden_icon(phone, "NO CELULARES")
        no_food = self.forbidden_icon(food, "NO COMER NI BEBER")

        other_rules = VGroup(
            self.note_panel("CUIDADO", ["Cuidar computador, silla y materiales."], width=4.25, title_size=23, body_size=20),
            self.note_panel("PUESTO FIJO", ["Permanecer en el puesto asignado."], width=4.25, title_size=23, body_size=20),
            self.note_panel("CONVIVENCIA", ["Hablar en tono adecuado y seguir indicaciones."], width=4.25, title_size=23, body_size=20),
            self.note_panel("NOVEDADES", ["Reportar de inmediato cualquier daño o cambio."], width=4.25, title_size=23, body_size=20),
        )
        other_rules.arrange_in_grid(cols=2, buff=(0.28, 0.28))

        top_icons = VGroup(no_phone, no_food).arrange(RIGHT, buff=1.65)
        content = VGroup(top_icons, other_rules).arrange(DOWN, buff=0.48)
        content.move_to(DOWN * 0.55)
        self.fit(content, 13.6, 5.2)
        self.assert_content_safe(content, "behavior rules")

        self.play(FadeIn(no_phone, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(no_food, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(
            LaggedStart(*[FadeIn(rule, shift=UP * 0.08) for rule in other_rules], lag_ratio=0.18),
            run_time=RUN_SLOW * 1.5,
        )
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def final_map(self) -> None:
        self.set_header(
            5,
            "MAPA FINAL 8B — USAR ESTE PUESTO DE AHORA EN ADELANTE",
            "Para encontrar un estudiante: ubique su número de lista, identifique el computador y luego la silla A, B o C.",
        )

        lab = self.make_lab_diagram(scale=1.03)
        lab.group.move_to(DOWN * 0.58)
        shift = lab.group.get_center()

        markers = VGroup()
        for number, _name, pc, seat in ASSIGNMENTS:
            markers.add(self.seat_marker(number, lab.seat_points[(pc, seat)] + shift, scale=1.03))

        legend = VGroup(
            self.text("PC01: 1–3", 17, BOLD),
            self.text("PC02: 4–6", 17, BOLD),
            self.text("PC03: 7–9", 17, BOLD),
            self.text("PC04: 10–12", 17, BOLD),
            self.text("PC05: 13–15", 17, BOLD),
            self.text("PC06: 16–18", 17, BOLD),
            self.text("PC07: 19–21", 17, BOLD),
            self.text("PC08: 22–23", 17, BOLD),
            self.text("PC09: disponible", 17, BOLD),
        ).arrange_in_grid(cols=3, buff=(0.32, 0.12))
        legend.to_edge(DOWN, buff=0.20)
        self.fit(legend, 14.2, 1.10)

        self.play(FadeIn(lab.group), run_time=RUN_NORMAL)
        self.play(
            LaggedStart(*[GrowFromCenter(marker) for marker in markers], lag_ratio=0.04),
            run_time=RUN_SLOW * 2.0,
        )
        self.play(FadeIn(legend, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL * 1.35)
        self.standard_closing("8B · Puesto fijo = orden, cuidado y responsabilidad en el laboratorio.")


# Preview (protocol):
#   manim -pql lab8b_seating.py Lab8BFixedSeating --disable_caching
# Final (protocol):
#   manim -pqh lab8b_seating.py Lab8BFixedSeating --disable_caching
