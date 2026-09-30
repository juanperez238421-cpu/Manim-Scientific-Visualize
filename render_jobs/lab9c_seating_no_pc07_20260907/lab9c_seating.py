from __future__ import annotations

import os
from typing import Dict, List, Tuple
from manim import *

# -----------------------------------------------------------------------------
# Render configuration · JP classroom protocol
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
GROUP = "NOVENO C"
SUBJECT = "FUNDAMENTOS DE FÍSICA"
DATE_TEXT = "07/09/2026"

DARK = "#303030"
LIGHT = "#D7D7D7"
VERY_LIGHT = "#F2F2F2"
PAPER = "#FAFAFA"

T_QUICK = 0.50
T_NORMAL = 0.82
T_SLOW = 1.10
PAUSE_SHORT = 0.55
PAUSE_ROW = 1.20
PAUSE_SCENE = 1.80
PAUSE_FINAL = 3.30

STUDENTS: List[str] = [
    "ALVAREZ ACOSTA SAMUEL",
    "BETANCUR ESTRADA CAMILA",
    "BETANCUR MAYORGA SOFIA",
    "CORRALES DURAN MARIA ANTONIA",
    "CORTES GONZALEZ MATIAS",
    "DO NASCIMIENTO ROMERO FIONA MARCELA",
    "GALEANO FLOREZ VIOLETA",
    "GARCIA HERRERA SIMON",
    "GARCIA ZAPATA MANUELA",
    "GIRALDO RODRIGUEZ MATIAS",
    "HERNANDEZ DUQUE SEBASTIAN",
    "JIMENEZ TOBON MARIA ANTONIA",
    "LONDOÑO VILLAMIZAR AMALIA",
    "MEJIA SERNA ISABELLA",
    "OVALLE PUERTA SAMUEL",
    "RAMOS BEDOYA MARIA CAMILA",
    "RODRIGUEZ PEÑA SALOMON",
    "VAN DUNNE BENAVIDEZ EMMA CAROLINA",
    "VASQUEZ RAMIREZ THOMAS",
    "VERGARA VILLARREAL SALOME",
]

SEATS = ("A", "B", "C")
USED = (1, 2, 3, 4, 5, 6, 8)
BLOCKED = 7
FREE = (9,)

# PC07 remains physically blocked. Students 19–20 continue at PC08.
ORDER = [(pc, seat) for pc in USED for seat in SEATS][: len(STUDENTS)]
ASSIGN = [(i, name, *ORDER[i - 1]) for i, name in enumerate(STUDENTS, 1)]

# Same physical laboratory map used in the validated 9B version.
POS = {
    9: (-2.75, 1.55), 6: (0.00, 1.55), 3: (2.75, 1.55),
    8: (-2.75, 0.00), 5: (0.00, 0.00), 2: (2.75, 0.00),
    7: (-2.75, -1.55), 4: (0.00, -1.55), 1: (2.75, -1.55),
}


def by_pc(pc: int):
    return [(i, n, s) for i, n, p, s in ASSIGN if p == pc]


def validate() -> None:
    assert len(STUDENTS) == 20
    assert len(ORDER) == 20
    assert len(ASSIGN) == 20
    assert ASSIGN[0][2:] == (1, "A")
    assert ASSIGN[17][2:] == (6, "C")
    assert ASSIGN[18][2:] == (8, "A")
    assert ASSIGN[19][2:] == (8, "B")
    assert all(pc != BLOCKED for _, _, pc, _ in ASSIGN)
    assert all(pc not in FREE for _, _, pc, _ in ASSIGN)
    assert len(by_pc(8)) == 2


class ScaledScene(Scene):
    """Applies LESSON_TIME_SCALE without changing pedagogical source timing."""

    def play(self, *args, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*args, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)


class Lab9CFixedSeatingNoPC07(ScaledScene):
    """Full-total 9C seating animation using official list order only."""

    def txt(self, text, size=30, weight=NORMAL, color=BLACK):
        return Text(text, font_size=size, weight=weight, color=color)

    def fit(self, mob, width, height):
        if mob.width > width:
            mob.scale_to_fit_width(width)
        if mob.height > height:
            mob.scale_to_fit_height(height)
        return mob

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=T_NORMAL)

    def panel(self, width, height, fill=PAPER):
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.14,
            stroke_color=BLACK,
            stroke_width=1.8,
            fill_color=fill,
            fill_opacity=1,
        )

    def header(self, title, subtitle):
        a = self.fit(self.txt(title, 37, BOLD), 14.7, 0.62)
        b = self.fit(self.txt(subtitle, 22, NORMAL, DARK), 14.5, 0.48)
        return VGroup(a, b).arrange(DOWN, buff=0.09).to_edge(UP, buff=0.20)

    def wrap_name(self, name: str, max_width=4.30):
        one = self.txt(name, 23, MEDIUM)
        if one.width <= max_width:
            return one
        words = name.split()
        candidates = []
        for k in range(1, len(words)):
            left = " ".join(words[:k])
            right = " ".join(words[k:])
            score = max(len(left), len(right)) + 0.20 * abs(len(left) - len(right))
            candidates.append((score, k))
        split = min(candidates)[1]
        two = VGroup(
            self.txt(" ".join(words[:split]), 21, MEDIUM),
            self.txt(" ".join(words[split:]), 21, MEDIUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.055)
        return self.fit(two, max_width, 0.72)

    def room(self, scale=0.90, numbers=False):
        box = RoundedRectangle(
            width=8.85,
            height=5.65,
            corner_radius=0.18,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        title = self.txt("VISTA SUPERIOR DEL LABORATORIO", 23, BOLD).next_to(box, UP, buff=0.10)
        desks: Dict[int, VGroup] = {}
        circles: Dict[Tuple[int, str], Circle] = {}
        desk_group = VGroup()
        lookup = {(p, s): i for i, _, p, s in ASSIGN}

        for pc in range(1, 10):
            x, y = POS[pc]
            desk = RoundedRectangle(
                width=2.18,
                height=1.10,
                corner_radius=0.10,
                stroke_color=BLACK,
                stroke_width=2.8 if pc == BLOCKED else 1.7,
                fill_color=VERY_LIGHT if pc == BLOCKED else WHITE,
                fill_opacity=1,
            ).move_to([x, y, 0])

            label_text = "PC07 · NO USAR" if pc == BLOCKED else f"PC{pc:02d}"
            label = self.txt(label_text, 16 if pc == BLOCKED else 18, BOLD)
            self.fit(label, 1.86, 0.30)
            label.move_to(desk.get_center() + UP * 0.25)

            seat_group = VGroup()
            for j, seat in enumerate(SEATS):
                c = Circle(
                    radius=0.19,
                    stroke_color=BLACK,
                    stroke_width=1.25,
                    fill_color=WHITE,
                    fill_opacity=1,
                ).move_to([x + (j - 1) * 0.57, y - 0.27, 0])
                seat_group.add(c, self.txt(seat, 13, BOLD).next_to(c, DOWN, buff=0.018))
                circles[(pc, seat)] = c
                if numbers and (pc, seat) in lookup:
                    seat_group.add(self.txt(str(lookup[(pc, seat)]), 16, BOLD).move_to(c))

            parts = VGroup(desk, label, seat_group)

            if pc == BLOCKED:
                parts.add(
                    Line(
                        desk.get_corner(UL) + RIGHT * 0.12 + DOWN * 0.12,
                        desk.get_corner(DR) + LEFT * 0.12 + UP * 0.12,
                        stroke_width=3.2,
                        color=BLACK,
                    ),
                    Line(
                        desk.get_corner(DL) + RIGHT * 0.12 + UP * 0.12,
                        desk.get_corner(UR) + LEFT * 0.12 + DOWN * 0.12,
                        stroke_width=3.2,
                        color=BLACK,
                    ),
                )
            elif pc in FREE:
                free = self.fit(self.txt("SIN ASIGNACIÓN", 12, BOLD, DARK), 1.70, 0.22)
                free.move_to(desk.get_center() + UP * 0.02)
                parts.add(free)
            elif pc == 8:
                note = self.fit(self.txt("19–20 · C libre", 12, BOLD, DARK), 1.65, 0.22)
                note.move_to(desk.get_center() + UP * 0.02)
                parts.add(note)

            desks[pc] = parts
            desk_group.add(parts)

        group = VGroup(box, desk_group, title).scale(scale)
        return group, desks, circles

    def card(self, pc: int):
        entries = by_pc(pc)
        box = self.panel(6.45, 4.35)
        title = self.fit(self.txt(f"PC{pc:02d} · ASIGNACIÓN", 31, BOLD), 5.55, 0.54)
        title.move_to(box.get_top() + DOWN * 0.46)

        if len(entries) == 3:
            ys = (0.52, -0.52, -1.56)
        elif len(entries) == 2:
            ys = (0.18, -1.02)
        else:
            ys = tuple(0.4 - 0.95 * j for j in range(len(entries)))

        rows = VGroup()
        for (i, name, seat), y in zip(entries, ys):
            num_circle = Circle(
                radius=0.285,
                stroke_color=BLACK,
                stroke_width=1.6,
                fill_color=WHITE,
                fill_opacity=1,
            ).move_to([-2.68, y, 0])
            num = self.txt(str(i), 18, BOLD).move_to(num_circle)

            seat_box = RoundedRectangle(
                width=0.74,
                height=0.52,
                corner_radius=0.06,
                stroke_color=BLACK,
                stroke_width=1.3,
                fill_color=VERY_LIGHT,
                fill_opacity=1,
            ).move_to([-1.86, y, 0])
            seat_txt = self.txt(seat, 19, BOLD).move_to(seat_box)

            name_mob = self.wrap_name(name)
            name_mob.set_x(-1.30 + name_mob.width / 2)
            name_mob.set_y(y)
            rows.add(VGroup(VGroup(num_circle, num), VGroup(seat_box, seat_txt), name_mob))

        if len(rows) > 1:
            for upper, lower in zip(rows[:-1], rows[1:]):
                assert upper.get_bottom()[1] > lower.get_top()[1] + 0.07
        assert title.get_bottom()[1] > rows[0].get_top()[1] + 0.10
        return VGroup(box, title, rows)

    def construct(self):
        validate()
        self.opening()
        self.rules()
        self.orientation()
        self.assignment_sequence()
        self.final_map()

    def opening(self):
        title = self.txt(f"{GROUP} · ASIGNACIÓN DE SILLAS", 44, BOLD)
        subtitle = self.txt(f"{SUBJECT} · {DATE_TEXT}", 27, NORMAL, DARK)
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=LIGHT, stroke_width=2)
        alert = self.txt("PC07: NO USAR", 34, BOLD)
        summary = self.txt("20 estudiantes · 7 mesas con asignación", 25, MEDIUM, DARK)
        detail = self.txt("PC08 recibe los números 19–20; su silla C queda libre.", 22, MEDIUM, DARK)
        group = VGroup(title, subtitle, line, alert, summary, detail).arrange(DOWN, buff=0.22)
        self.fit(group, 14.4, 5.0)

        self.play(FadeIn(title, shift=UP * 0.15), run_time=T_SLOW)
        self.play(FadeIn(subtitle), Create(line), run_time=T_NORMAL)
        self.play(FadeIn(alert), FadeIn(summary), run_time=T_NORMAL)
        self.play(FadeIn(detail), run_time=T_NORMAL)
        self.wait(PAUSE_SCENE)
        self.clear_scene()

    def rules(self):
        head = self.header(
            "CRITERIO DE ASIGNACIÓN",
            "La ubicación depende únicamente del número oficial de lista; no se usan calificaciones.",
        )

        left_box = self.panel(6.85, 4.90)
        left_title = self.txt("REGLAS", 31, BOLD)
        left_lines = VGroup(*[
            self.txt("1. Seguir el orden oficial: 1 → 20", 24, MEDIUM),
            self.txt("2. Cada mesa usa sillas A → B → C", 24, MEDIUM),
            self.txt("3. PC01 a PC06 reciben 1 → 18", 24, MEDIUM),
            self.txt("4. PC07 permanece completamente bloqueada", 23, MEDIUM),
            self.txt("5. PC08 recibe 19–20; PC09 queda libre", 23, MEDIUM),
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        left_group = VGroup(left_title, left_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        self.fit(left_group, 6.10, 4.05)
        left_group.move_to(left_box).align_to(left_box, LEFT).shift(RIGHT * 0.34)

        right_box = self.panel(6.25, 4.90)
        right_title = self.txt("MAPA NUMÉRICO", 31, BOLD)
        right_lines = VGroup(*[
            self.txt("PC01: 1–3     PC02: 4–6", 25, BOLD),
            self.txt("PC03: 7–9     PC04: 10–12", 25, BOLD),
            self.txt("PC05: 13–15   PC06: 16–18", 25, BOLD),
            self.txt("PC07: NO USAR", 27, BOLD),
            self.txt("PC08: 19–20   PC09: SIN ASIGNACIÓN", 22, BOLD),
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.31)
        right_group = VGroup(right_title, right_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        self.fit(right_group, 5.55, 4.05)
        right_group.move_to(right_box).align_to(right_box, LEFT).shift(RIGHT * 0.34)

        body = VGroup(VGroup(left_box, left_group), VGroup(right_box, right_group)).arrange(RIGHT, buff=0.55)
        body.move_to(DOWN * 0.45)

        self.play(FadeIn(head), run_time=T_NORMAL)
        self.play(FadeIn(body[0]), run_time=T_NORMAL)
        self.wait(PAUSE_ROW)
        self.play(FadeIn(body[1]), run_time=T_NORMAL)
        self.wait(PAUSE_SCENE)
        self.clear_scene()

    def orientation(self):
        head = self.header(
            "UBICACIÓN FÍSICA DEL LABORATORIO",
            "Se conserva el mismo mapa espacial: PC07 sigue visible, pero no se utiliza.",
        )
        room, desks, _ = self.room(1.10)
        room.move_to(LEFT * 2.70 + DOWN * 0.45)

        note_box = self.panel(4.65, 4.85)
        note_title = self.txt("LECTURA DEL MAPA", 27, BOLD)
        note_lines = VGroup(*[
            self.txt("Fila superior: PC09 · PC06 · PC03", 21, MEDIUM),
            self.txt("Fila media: PC08 · PC05 · PC02", 21, MEDIUM),
            self.txt("Fila inferior: PC07 · PC04 · PC01", 21, MEDIUM),
            self.txt("PC07 = NO USAR", 25, BOLD),
            self.txt("PC08 = estudiantes 19–20", 23, BOLD),
            self.txt("PC09 = sin asignación", 22, BOLD),
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        note_group = VGroup(note_title, note_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.27)
        self.fit(note_group, 4.05, 4.10)
        note_group.move_to(note_box)
        note = VGroup(note_box, note_group).move_to(RIGHT * 5.25 + DOWN * 0.45)

        self.play(FadeIn(head), run_time=T_NORMAL)
        self.play(FadeIn(room), run_time=T_NORMAL)
        self.play(FadeIn(note), run_time=T_NORMAL)
        self.wait(PAUSE_ROW)

        blocked = SurroundingRectangle(desks[7], buff=0.08, stroke_width=3.2, color=BLACK)
        blocked_label = self.txt("MESA 7 · BLOQUEADA", 23, BOLD).next_to(blocked, UP, buff=0.08)
        self.play(Create(blocked), FadeIn(blocked_label), run_time=T_NORMAL)
        self.wait(PAUSE_ROW)

        pc8 = SurroundingRectangle(desks[8], buff=0.08, stroke_width=2.8, color=BLACK)
        pc8_label = self.txt("PC08 · NÚMEROS 19–20", 22, BOLD).next_to(pc8, UP, buff=0.08)
        self.play(FadeOut(blocked), FadeOut(blocked_label), Create(pc8), FadeIn(pc8_label), run_time=T_NORMAL)
        self.wait(PAUSE_SCENE)
        self.play(FadeOut(pc8), FadeOut(pc8_label), run_time=T_QUICK)
        self.clear_scene()

    def assignment_sequence(self):
        head = self.header(
            f"ASIGNACIÓN {GROUP} · ORDEN DE LISTA",
            "Cada bloque muestra los estudiantes asignados a una mesa activa.",
        )
        self.add(head)

        room, desks, circles = self.room(0.90)
        room.move_to(LEFT * 4.15 + DOWN * 0.52)
        self.play(FadeIn(room), run_time=T_NORMAL)

        current = None
        for pc in USED:
            card = self.card(pc).move_to(RIGHT * 3.55 + DOWN * 0.52)
            if current is None:
                self.play(FadeIn(card), run_time=T_NORMAL)
            else:
                self.play(ReplacementTransform(current, card), run_time=T_NORMAL)
            current = card

            focus = SurroundingRectangle(desks[pc], buff=0.06, stroke_width=2.6, color=BLACK)
            self.play(Create(focus), run_time=T_QUICK)
            for i, _, seat in by_pc(pc):
                c = circles[(pc, seat)]
                num = self.txt(str(i), 16, BOLD).move_to(c)
                self.play(FadeIn(num, scale=0.85), Indicate(c, scale_factor=1.18), run_time=T_QUICK)
            self.wait(PAUSE_SHORT if pc != 8 else PAUSE_ROW)
            self.play(FadeOut(focus), run_time=T_QUICK)

        self.wait(PAUSE_ROW)
        self.play(FadeOut(current), run_time=T_NORMAL)

        box = self.panel(6.45, 2.75)
        done = VGroup(
            self.txt("ASIGNACIÓN COMPLETA", 31, BOLD),
            VGroup(
                self.txt("20 estudiantes · 20 puestos usados", 24, MEDIUM),
                self.txt("PC07: 0 estudiantes", 26, BOLD),
                self.txt("PC08: 19–20 · silla C libre", 23, BOLD),
                self.txt("PC09: sin asignación", 22, MEDIUM),
            ).arrange(DOWN, buff=0.16),
        ).arrange(DOWN, buff=0.23)
        done.move_to(box)
        final_card = VGroup(box, done).move_to(RIGHT * 3.55 + DOWN * 0.52)
        self.play(FadeIn(final_card), run_time=T_NORMAL)
        self.wait(PAUSE_SCENE)
        self.clear_scene()

    def final_map(self):
        head = self.header(
            f"MAPA FINAL · {GROUP}",
            "Busque su número de lista y luego identifique el PC y la silla A, B o C.",
        )
        room, _, _ = self.room(1.06, numbers=True)
        room.move_to(LEFT * 2.75 + DOWN * 0.45)

        legend_box = self.panel(4.75, 5.45)
        legend_lines = VGroup(*[
            self.txt("PC01 → 1–3", 22, BOLD),
            self.txt("PC02 → 4–6", 22, BOLD),
            self.txt("PC03 → 7–9", 22, BOLD),
            self.txt("PC04 → 10–12", 22, BOLD),
            self.txt("PC05 → 13–15", 22, BOLD),
            self.txt("PC06 → 16–18", 22, BOLD),
            self.txt("PC07 → NO USAR", 24, BOLD),
            self.txt("PC08 → 19–20", 22, BOLD),
            self.txt("PC09 → SIN ASIGNACIÓN", 20, BOLD),
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        legend = VGroup(self.txt("RESUMEN", 29, BOLD), legend_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(legend, 4.08, 4.75)
        legend.move_to(legend_box).align_to(legend_box, LEFT).shift(RIGHT * 0.34)
        legend_group = VGroup(legend_box, legend).move_to(RIGHT * 5.20 + DOWN * 0.45)

        self.play(FadeIn(head), run_time=T_NORMAL)
        self.play(FadeIn(room), FadeIn(legend_group), run_time=T_SLOW)
        self.wait(PAUSE_SCENE)

        note_box = RoundedRectangle(
            width=9.80,
            height=0.82,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=1.8,
            fill_color=VERY_LIGHT,
            fill_opacity=1,
        )
        note_text = self.fit(
            self.txt(
                f"IMPORTANTE: NINGÚN ESTUDIANTE DE {GROUP} SE UBICA EN PC07. LOS NÚMEROS 19–20 VAN A PC08.",
                22,
                BOLD,
            ),
            9.25,
            0.50,
        )
        note_text.move_to(note_box)
        note = VGroup(note_box, note_text).to_edge(DOWN, buff=0.16)
        self.play(FadeIn(note), run_time=T_NORMAL)
        self.wait(PAUSE_FINAL)
