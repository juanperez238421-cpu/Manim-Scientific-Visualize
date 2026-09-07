#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Noveno A · asignación fija de sillas por orden de lista · V2 Senior QA.

Mejoras V2:
- Revisión visual del render V1 y corrección de solapamientos.
- Tarjetas de asignación más grandes.
- Nombres largos con salto inteligente a dos líneas, sin compresión extrema.
- Etiquetas y números del mapa ampliados para proyección en aula.
- Transición PC07 separada de la tarjeta PC06; nunca cubre estudiantes.
- Títulos más compactos para reservar espacio al contenido útil.
- Validaciones de layout para evitar cruces entre filas.

Reglas:
- 24 estudiantes.
- 3 puestos por mesa/computador.
- La mesa/PC07 NO se usa.
- La asignación continúa de PC06 directamente a PC08.
- Disposición física:
  fila superior: PC09, PC06, PC03
  fila media:    PC08, PC05, PC02
  fila inferior: PC07, PC04, PC01

Target: ManimCE 0.20.1 · 1920x1080 · 30 fps.
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple

from manim import *


config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F2F2F2"
PAPER_GRAY = "#FAFAFA"

RUN_QUICK = 0.50
RUN_NORMAL = 0.82
RUN_SLOW = 1.10
PAUSE_SHORT = 0.55
PAUSE_READ = 1.25
PAUSE_EXPLAIN = 1.75
PAUSE_FINAL = 3.50

STUDENTS: List[str] = [
    "ARIAS ROMERO ANA MARIA",
    "ARISTIZABAL FRANCO SIMON",
    "CABARCAS YEPES PABLO",
    "CALLE GARCIA MIGUEL",
    "CARDONA BETANCUR SAMUEL",
    "CARDONA CORTES SANTIAGO",
    "CASTELLANO ESCOBAR ROSAR...",
    "CUERVO ESCOBAR JUANITA",
    "DUQUE NANCLARES MAXIMILI...",
    "GARZON DUEÑAS ISABELLA",
    "GIRALDO GALLEGO MARTINA",
    "GIRALDO MESIAS ALEJANDRO",
    "MEJIA SERNA PAULINA",
    "MONTOYA RUIZ JUAN JOSE",
    "OCHOA TOBON ANTONIO",
    "PACHON MARIN MARIANA",
    "PARDO ARANGO CAMILA",
    "PEREZ CORTES JUANITA",
    "RIVERA CORTINA LUCIANA",
    "TAMAYO YEPES JUAN PABLO",
    "USCATEGUI LARRAIN FELIX",
    "ZAPATA PARRA JUAN SEBAST...",
    "ZAPATA PEREZ PABLO",
    "ZULUAGA CORDOBA SOFIA",
]

SEAT_LETTERS: Tuple[str, ...] = ("A", "B", "C")
ACTIVE_PCS: Tuple[int, ...] = (1, 2, 3, 4, 5, 6, 8, 9)
BLOCKED_PC = 7

SEAT_ORDER: List[Tuple[int, str]] = [(pc, seat) for pc in ACTIVE_PCS for seat in SEAT_LETTERS]
ASSIGNMENTS: List[Tuple[int, str, int, str]] = []
for student_number, name in enumerate(STUDENTS, start=1):
    pc, seat = SEAT_ORDER[student_number - 1]
    ASSIGNMENTS.append((student_number, name, pc, seat))

PC_POSITIONS: Dict[int, Tuple[float, float]] = {
    9: (-2.75, 1.55), 6: (0.00, 1.55), 3: (2.75, 1.55),
    8: (-2.75, 0.00), 5: (0.00, 0.00), 2: (2.75, 0.00),
    7: (-2.75, -1.55), 4: (0.00, -1.55), 1: (2.75, -1.55),
}


def validate_roster() -> None:
    assert len(STUDENTS) == 24
    assert len(SEAT_ORDER) == 24
    assert len(ASSIGNMENTS) == 24
    assert len(set(STUDENTS)) == len(STUDENTS)
    assert set(PC_POSITIONS) == set(range(1, 10))
    assert all(pc != BLOCKED_PC for _n, _name, pc, _seat in ASSIGNMENTS)
    assert ASSIGNMENTS[0][2:] == (1, "A")
    assert ASSIGNMENTS[17][2:] == (6, "C")
    assert ASSIGNMENTS[18][2:] == (8, "A")
    assert ASSIGNMENTS[20][2:] == (8, "C")
    assert ASSIGNMENTS[21][2:] == (9, "A")
    assert ASSIGNMENTS[23][2:] == (9, "C")


def students_for_pc(pc: int) -> List[Tuple[int, str, str]]:
    return [(n, name, seat) for n, name, assigned_pc, seat in ASSIGNMENTS if assigned_pc == pc]


class ScaledScene(Scene):
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)


class Lab9AFixedSeatingNoPC07(ScaledScene):
    def construct(self) -> None:
        validate_roster()
        self.camera.background_color = WHITE
        self.opening()
        self.assignment_rule()
        self.room_orientation()
        self.assign_students()
        self.final_summary()

    def txt(self, content: str, size: int = 30, weight=NORMAL, color=BLACK_TEXT) -> Text:
        return Text(content, font_size=size, color=color, weight=weight)

    def fit(self, mob: Mobject, max_width: float, max_height: float) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def clear(self) -> None:
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)

    def title_block(self, title: str, subtitle: str) -> VGroup:
        t = self.txt(title, 37, BOLD)
        s = self.txt(subtitle, 22, NORMAL, DARK_GRAY)
        self.fit(t, 14.7, 0.62)
        self.fit(s, 14.5, 0.48)
        group = VGroup(t, s).arrange(DOWN, buff=0.09)
        group.to_edge(UP, buff=0.20)
        return group

    def panel(self, width: float, height: float, fill=PAPER_GRAY) -> RoundedRectangle:
        return RoundedRectangle(width=width, height=height, corner_radius=0.14,
                                stroke_color=BLACK_LINE, stroke_width=1.8,
                                fill_color=fill, fill_opacity=1.0)

    @staticmethod
    def _balanced_two_lines(name: str) -> Tuple[str, str]:
        words = name.split()
        if len(words) <= 1:
            return name, ""
        best = None
        for cut in range(1, len(words)):
            a = " ".join(words[:cut])
            b = " ".join(words[cut:])
            score = max(len(a), len(b)) + 0.22 * abs(len(a) - len(b))
            if best is None or score < best[0]:
                best = (score, a, b)
        assert best is not None
        return best[1], best[2]

    def name_label(self, name: str, max_width: float = 4.35) -> Mobject:
        single = self.txt(name, 23, MEDIUM)
        if single.width <= max_width:
            return single
        line1, line2 = self._balanced_two_lines(name)
        wrapped = VGroup(self.txt(line1, 21, MEDIUM), self.txt(line2, 21, MEDIUM))
        wrapped.arrange(DOWN, aligned_edge=LEFT, buff=0.055)
        self.fit(wrapped, max_width, 0.70)
        return wrapped

    def make_room_map(self, scale_factor: float = 1.0, show_numbers: bool = False):
        room_box = RoundedRectangle(width=8.85, height=5.65, corner_radius=0.18,
                                    stroke_color=BLACK_LINE, stroke_width=2.0,
                                    fill_color=WHITE, fill_opacity=1.0)
        room_label = self.txt("VISTA SUPERIOR DEL LABORATORIO", 23, BOLD)
        room_label.next_to(room_box, UP, buff=0.10)
        desks: Dict[int, VGroup] = {}
        seat_outlines: Dict[Tuple[int, str], Circle] = {}
        desk_group = VGroup()
        number_lookup = {(pc, seat): n for n, _name, pc, seat in ASSIGNMENTS}

        for pc in range(1, 10):
            x, y = PC_POSITIONS[pc]
            desk = RoundedRectangle(width=2.18, height=1.10, corner_radius=0.10,
                                    stroke_color=BLACK_LINE,
                                    stroke_width=1.7 if pc != BLOCKED_PC else 2.8,
                                    fill_color=VERY_LIGHT_GRAY if pc == BLOCKED_PC else WHITE,
                                    fill_opacity=1.0).move_to([x, y, 0])
            label_text = f"PC{pc:02d}" if pc != BLOCKED_PC else "PC07 · NO USAR"
            label = self.txt(label_text, 18 if pc != BLOCKED_PC else 16, BOLD)
            self.fit(label, 1.85, 0.30)
            label.move_to(desk.get_center() + UP * 0.25)
            seat_group = VGroup()
            for idx, seat in enumerate(SEAT_LETTERS):
                sx = x + (idx - 1) * 0.57
                sy = y - 0.27
                circle = Circle(radius=0.19, stroke_color=BLACK_LINE, stroke_width=1.25,
                                fill_color=WHITE, fill_opacity=1.0).move_to([sx, sy, 0])
                seat_letter = self.txt(seat, 13, BOLD).next_to(circle, DOWN, buff=0.018)
                seat_group.add(circle, seat_letter)
                seat_outlines[(pc, seat)] = circle
                if show_numbers and (pc, seat) in number_lookup:
                    seat_group.add(self.txt(str(number_lookup[(pc, seat)]), 16, BOLD).move_to(circle))
            desk_parts = VGroup(desk, label, seat_group)
            if pc == BLOCKED_PC:
                cross1 = Line(desk.get_corner(UL) + RIGHT*0.12 + DOWN*0.12,
                              desk.get_corner(DR) + LEFT*0.12 + UP*0.12,
                              color=BLACK_LINE, stroke_width=3.2)
                cross2 = Line(desk.get_corner(DL) + RIGHT*0.12 + UP*0.12,
                              desk.get_corner(UR) + LEFT*0.12 + DOWN*0.12,
                              color=BLACK_LINE, stroke_width=3.2)
                desk_parts.add(cross1, cross2)
            desks[pc] = desk_parts
            desk_group.add(desk_parts)

        map_group = VGroup(room_box, desk_group, room_label)
        map_group.scale(scale_factor)
        return map_group, desks, seat_outlines

    def student_card(self, pc: int) -> VGroup:
        students = students_for_pc(pc)
        box = self.panel(6.45, 4.35)
        title = self.txt(f"PC{pc:02d} · ASIGNACIÓN", 31, BOLD)
        self.fit(title, 5.55, 0.54)
        title.move_to(box.get_top() + DOWN * 0.46)
        row_y = (0.52, -0.52, -1.56)
        rows = VGroup()
        for (n, name, seat), y in zip(students, row_y):
            badge = Circle(radius=0.285, stroke_color=BLACK_LINE, stroke_width=1.6,
                           fill_color=WHITE, fill_opacity=1.0).move_to([-2.68, y, 0])
            num = self.txt(str(n), 18, BOLD).move_to(badge)
            seat_box = RoundedRectangle(width=0.74, height=0.52, corner_radius=0.06,
                                        stroke_color=BLACK_LINE, stroke_width=1.3,
                                        fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0).move_to([-1.86, y, 0])
            seat_txt = self.txt(seat, 19, BOLD).move_to(seat_box)
            name_mob = self.name_label(name, max_width=4.28)
            name_mob.set_x(-1.30 + name_mob.width / 2)
            name_mob.set_y(y)
            rows.add(VGroup(VGroup(badge, num), VGroup(seat_box, seat_txt), name_mob))
        for upper, lower in zip(rows[:-1], rows[1:]):
            assert upper.get_bottom()[1] > lower.get_top()[1] + 0.08
        return VGroup(box, title, rows)

    def opening(self) -> None:
        title = self.txt("NOVENO A · ASIGNACIÓN DE SILLAS", 44, BOLD)
        subtitle = self.txt("Laboratorio · orden oficial de lista", 29, NORMAL, DARK_GRAY)
        rule = Line(LEFT * 5.8, RIGHT * 5.8, color=LIGHT_GRAY, stroke_width=2.0)
        note = self.txt("MESA 7: SIN ESTUDIANTES", 33, BOLD)
        group = VGroup(title, subtitle, rule, note).arrange(DOWN, buff=0.28)
        self.fit(group, 14.4, 4.4)
        group.move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP * 0.15), run_time=RUN_SLOW)
        self.play(FadeIn(subtitle), Create(rule), run_time=RUN_NORMAL)
        self.play(FadeIn(note, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear()

    def assignment_rule(self) -> None:
        header = self.title_block("CRITERIO DE ASIGNACIÓN",
                                  "La posición depende únicamente del número de lista; no se utiliza la mesa 7.")
        rules_box = self.panel(6.8, 4.85)
        rules_title = self.txt("REGLAS", 31, BOLD)
        rules = VGroup(
            self.txt("1. Seguir el orden oficial: 1 → 24", 25, MEDIUM),
            self.txt("2. Tres estudiantes por mesa: A → B → C", 25, MEDIUM),
            self.txt("3. PC07 / mesa 7 queda completamente libre", 25, MEDIUM),
            self.txt("4. Después de PC06 se continúa en PC08", 25, MEDIUM),
            self.txt("5. PC09 recibe los estudiantes 22 → 24", 25, MEDIUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.31)
        rules_group = VGroup(rules_title, rules).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        self.fit(rules_group, 6.05, 4.00)
        rules_group.move_to(rules_box).align_to(rules_box, LEFT).shift(RIGHT * 0.34)

        mapping_box = self.panel(6.05, 4.85)
        mapping_title = self.txt("MAPA NUMÉRICO", 31, BOLD)
        mapping = VGroup(
            self.txt("PC01: 1–3    PC02: 4–6", 25, BOLD),
            self.txt("PC03: 7–9    PC04: 10–12", 25, BOLD),
            self.txt("PC05: 13–15  PC06: 16–18", 25, BOLD),
            self.txt("PC07: NO USAR", 28, BOLD),
            self.txt("PC08: 19–21  PC09: 22–24", 25, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        mapping_group = VGroup(mapping_title, mapping).arrange(DOWN, aligned_edge=LEFT, buff=0.31)
        self.fit(mapping_group, 5.35, 4.00)
        mapping_group.move_to(mapping_box).align_to(mapping_box, LEFT).shift(RIGHT * 0.34)
        body = VGroup(VGroup(rules_box, rules_group), VGroup(mapping_box, mapping_group)).arrange(RIGHT, buff=0.50)
        body.move_to(DOWN * 0.48)
        self.play(FadeIn(header), run_time=RUN_NORMAL)
        self.play(FadeIn(body[0], shift=RIGHT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(body[1], shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear()

    def room_orientation(self) -> None:
        header = self.title_block("UBICACIÓN FÍSICA DEL LABORATORIO",
                                  "La mesa 7 sigue visible como referencia espacial, pero queda bloqueada para este grupo.")
        room, desks, _seats = self.make_room_map(scale_factor=1.04)
        room.move_to(LEFT * 2.85 + DOWN * 0.48)
        note_box = self.panel(4.85, 4.85)
        note_title = self.txt("LECTURA DEL MAPA", 28, BOLD)
        note_lines = VGroup(
            self.txt("Fila superior: PC09 · PC06 · PC03", 22, MEDIUM),
            self.txt("Fila media: PC08 · PC05 · PC02", 22, MEDIUM),
            self.txt("Fila inferior: PC07 · PC04 · PC01", 22, MEDIUM),
            self.txt("PC07 = NO USAR", 27, BOLD),
            self.txt("La secuencia salta PC07.", 23, MEDIUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        note_group = VGroup(note_title, note_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.31)
        self.fit(note_group, 4.15, 4.00)
        note_group.move_to(note_box)
        note = VGroup(note_box, note_group).move_to(RIGHT * 5.20 + DOWN * 0.48)
        self.play(FadeIn(header), run_time=RUN_NORMAL)
        self.play(FadeIn(room), run_time=RUN_NORMAL)
        self.play(FadeIn(note, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        pc7_focus = SurroundingRectangle(desks[7], buff=0.08, color=BLACK_LINE, stroke_width=3.2)
        pc7_label = self.txt("MESA 7 · BLOQUEADA", 24, BOLD).next_to(pc7_focus, UP, buff=0.08)
        self.play(Create(pc7_focus), FadeIn(pc7_label, shift=UP * 0.05), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(pc7_focus), FadeOut(pc7_label), run_time=RUN_QUICK)
        self.clear()

    def pc07_transition(self, desks: Dict[int, VGroup]) -> None:
        panel = RoundedRectangle(width=6.35, height=2.05, corner_radius=0.14,
                                 stroke_color=BLACK_LINE, stroke_width=2.2,
                                 fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0)
        top = self.txt("PC07 SE OMITE", 32, BOLD)
        bottom = self.txt("CONTINUAMOS EN PC08 → ESTUDIANTES 19–21", 23, BOLD)
        self.fit(bottom, 5.70, 0.48)
        words = VGroup(top, bottom).arrange(DOWN, buff=0.22).move_to(panel)
        callout = VGroup(panel, words).move_to(RIGHT * 4.30 + DOWN * 0.48)
        self.play(FadeIn(callout, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.play(Indicate(desks[7], scale_factor=1.06), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeOut(callout, shift=UP * 0.05), run_time=RUN_QUICK)

    def assign_students(self) -> None:
        header = self.title_block("ASIGNACIÓN NOVENO A · ORDEN DE LISTA",
                                  "Cada bloque muestra los tres estudiantes de la mesa activa. PC07 se omite.")
        self.add(header)
        room, desks, seat_outlines = self.make_room_map(scale_factor=0.82)
        room.move_to(LEFT * 4.28 + DOWN * 0.48)
        self.play(FadeIn(room), run_time=RUN_NORMAL)
        current_card = None
        for pc in ACTIVE_PCS:
            if pc == 8:
                if current_card is not None:
                    self.play(FadeOut(current_card), run_time=RUN_QUICK)
                    current_card = None
                self.pc07_transition(desks)
            card = self.student_card(pc).move_to(RIGHT * 4.30 + DOWN * 0.48)
            if current_card is None:
                self.play(FadeIn(card, shift=LEFT * 0.08), run_time=RUN_NORMAL)
            else:
                self.play(ReplacementTransform(current_card, card), run_time=RUN_NORMAL)
            current_card = card
            focus = SurroundingRectangle(desks[pc], buff=0.06, color=BLACK_LINE, stroke_width=2.8)
            self.play(Create(focus), run_time=RUN_QUICK)
            for n, _name, seat in students_for_pc(pc):
                circle = seat_outlines[(pc, seat)]
                num = self.txt(str(n), 16, BOLD).move_to(circle.get_center())
                self.play(FadeIn(num, scale=0.85), Indicate(circle, scale_factor=1.18), run_time=RUN_QUICK)
            self.wait(PAUSE_READ)
            self.play(FadeOut(focus), run_time=RUN_QUICK)
        if current_card is not None:
            self.play(FadeOut(current_card), run_time=RUN_NORMAL)
        finish_box = self.panel(6.45, 2.35)
        finish_title = self.txt("ASIGNACIÓN COMPLETA", 32, BOLD)
        finish_lines = VGroup(self.txt("24 estudiantes · 24 puestos usados", 25, MEDIUM),
                              self.txt("PC07: 0 estudiantes", 28, BOLD)).arrange(DOWN, buff=0.24)
        finish = VGroup(finish_title, finish_lines).arrange(DOWN, buff=0.28).move_to(finish_box)
        finish_group = VGroup(finish_box, finish).move_to(RIGHT * 4.30 + DOWN * 0.48)
        self.play(FadeIn(finish_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear()

    def final_summary(self) -> None:
        header = self.title_block("MAPA FINAL · NOVENO A",
                                  "Ubique su número de lista, luego identifique el PC y la silla A, B o C.")
        room, _desks, _seats = self.make_room_map(scale_factor=1.04, show_numbers=True)
        room.move_to(LEFT * 2.85 + DOWN * 0.38)
        legend_box = self.panel(4.75, 5.35)
        legend_title = self.txt("RESUMEN", 31, BOLD)
        legend_lines = VGroup(
            self.txt("PC01 → 1–3", 23, BOLD), self.txt("PC02 → 4–6", 23, BOLD),
            self.txt("PC03 → 7–9", 23, BOLD), self.txt("PC04 → 10–12", 23, BOLD),
            self.txt("PC05 → 13–15", 23, BOLD), self.txt("PC06 → 16–18", 23, BOLD),
            self.txt("PC07 → NO USAR", 25, BOLD), self.txt("PC08 → 19–21", 23, BOLD),
            self.txt("PC09 → 22–24", 23, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        legend_group = VGroup(legend_title, legend_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        self.fit(legend_group, 4.00, 4.75)
        legend_group.move_to(legend_box).align_to(legend_box, LEFT).shift(RIGHT * 0.36)
        legend = VGroup(legend_box, legend_group).move_to(RIGHT * 5.18 + DOWN * 0.38)
        self.play(FadeIn(header), run_time=RUN_NORMAL)
        self.play(FadeIn(room), FadeIn(legend, shift=LEFT * 0.08), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        final_note_box = RoundedRectangle(width=9.25, height=0.82, corner_radius=0.10,
                                          stroke_color=BLACK_LINE, stroke_width=1.8,
                                          fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0)
        final_note = self.txt("IMPORTANTE: NINGÚN ESTUDIANTE DE NOVENO A SE UBICA EN LA MESA 7.", 24, BOLD)
        self.fit(final_note, 8.70, 0.50)
        final_note.move_to(final_note_box)
        note = VGroup(final_note_box, final_note).to_edge(DOWN, buff=0.16)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)


if __name__ == "__main__":
    validate_roster()
