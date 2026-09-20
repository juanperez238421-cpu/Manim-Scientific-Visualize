#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Variable velocity, senior classroom version.

Pedagogical focus
-----------------
Move from the ideal MRU model to a more realistic trip where velocity changes
with time because the driver accelerates, stops, brakes near an accident,
passes through heavy traffic, and accelerates again.

This version follows the JP Classroom Manim Standard:
- 1920x1080 / 30 fps / white background;
- monochrome hierarchy;
- standard opening + persistent numbered headers;
- safe layout assertions;
- integrated visual + explanation panels;
- validated numerical claims;
- modular scene sections.

Target: Manim Community Edition 0.20.x.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from library.jp_classroom_style import *  # noqa: F401,F403,E402


PROFILE = [
    (0.0, 0.0),
    (10.0, 70.0),
    (35.0, 70.0),
    (40.0, 0.0),
    (55.0, 0.0),
    (60.0, 65.0),
    (75.0, 65.0),
    (82.0, 25.0),
    (92.0, 25.0),
    (100.0, 10.0),
    (108.0, 10.0),
    (115.0, 55.0),
    (120.0, 55.0),
]

EVENTS = [
    ("01", "Acelera", "0 → 70 km/h"),
    ("02", "Parada", "15 min detenido"),
    ("03", "Accidente", "reduce a 25 km/h"),
    ("04", "Tráfico", "avanza a 10 km/h"),
    ("05", "Recupera", "sube a 55 km/h"),
]


def velocity_at(t_min: float) -> float:
    """Piecewise-linear velocity profile, t in minutes and v in km/h."""
    if t_min <= PROFILE[0][0]:
        return PROFILE[0][1]
    if t_min >= PROFILE[-1][0]:
        return PROFILE[-1][1]
    for (t0, v0), (t1, v1) in zip(PROFILE[:-1], PROFILE[1:]):
        if t0 <= t_min <= t1:
            alpha = (t_min - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    raise ValueError(f"t outside profile: {t_min}")


def position_at(t_min: float) -> float:
    """Numerical integral of the velocity profile; returns travelled km."""
    samples = np.linspace(0.0, t_min, max(2, int(t_min * 6) + 2))
    values = np.array([velocity_at(float(t)) for t in samples])
    return float(np.trapezoid(values, samples / 60.0))


FINAL_DISTANCE_KM = position_at(120.0)


class Physics9VariableVelocitySeniorV2(JPMathClassroomScene):
    """Senior classroom scene: MRU -> realistic variable velocity."""

    def validate_lesson_data(self) -> None:
        assert_close(FINAL_DISTANCE_KM, 78.3333333333, tol=0.02, label="route distance")
        assert velocity_at(47.0) == 0.0
        assert velocity_at(104.0) == 10.0
        assert velocity_at(120.0) == 55.0
        sample_t = np.linspace(0, 120, 121)
        positions = [position_at(float(t)) for t in sample_t]
        assert all(b >= a - 1e-6 for a, b in zip(positions[:-1], positions[1:])), "x(t) must be nondecreasing"
        assert all(velocity_at(float(t)) >= 0 for t in sample_t), "speed must stay nonnegative"

    def construct(self) -> None:
        self.opening()
        self.section_1_mru_reference()
        self.section_2_real_trip()
        self.section_3_position_time()
        self.section_4_velocity_time()
        self.section_5_acceleration()
        self.section_6_synthesis()
        self.standard_closing(
            "Un movimiento real se describe siguiendo cómo cambia la velocidad con el tiempo."
        )

    def make_car(self, scale: float = 1.0) -> VGroup:
        body = RoundedRectangle(
            width=1.25,
            height=0.44,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=2.2,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        )
        roof = Polygon(
            [-0.34, 0.22, 0],
            [-0.13, 0.50, 0],
            [0.32, 0.50, 0],
            [0.48, 0.22, 0],
            stroke_color=BLACK_LINE,
            stroke_width=2.2,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        wheels = VGroup(
            Circle(0.115, color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1.0).move_to([-0.38, -0.24, 0]),
            Circle(0.115, color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1.0).move_to([0.38, -0.24, 0]),
        )
        return VGroup(body, roof, wheels).scale(scale)

    def make_road(self, width: float = 8.4, height: float = 1.08) -> VGroup:
        road = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.72,
        )
        dash_count = max(5, int(width / 0.85))
        lane = VGroup(*[
            Line(LEFT * 0.18, RIGHT * 0.18, color=WHITE, stroke_width=4.2)
            for _ in range(dash_count)
        ])
        lane.arrange(RIGHT, buff=0.38).move_to(road)
        lane.scale_to_fit_width(width - 0.55)
        return VGroup(road, lane)

    def road_panel(self, width: float = 8.7, height: float = 2.6) -> FigurePanel:
        road = self.make_road(width=7.75)
        city_a = self.text("CIUDAD A", 20, BOLD).next_to(road, LEFT, buff=0.14)
        city_b = self.text("CIUDAD B", 20, BOLD).next_to(road, RIGHT, buff=0.14)
        route = VGroup(road, city_a, city_b)
        return self.figure_panel(
            route,
            width=width,
            height=height,
            title="Ruta entre dos ciudades",
            caption="El mismo recorrido puede incluir muchos regímenes de velocidad.",
        )

    def event_card(self, number: str, title: str, detail: str) -> VGroup:
        badge = RoundedRectangle(
            width=0.64,
            height=0.50,
            corner_radius=0.08,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        )
        badge_text = self.text(number, 18, BOLD).move_to(badge)
        title_mob = self.text(title, 25, BOLD)
        detail_mob = self.text(detail, 21)
        text_group = VGroup(title_mob, detail_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        content = VGroup(VGroup(badge, badge_text), text_group).arrange(RIGHT, buff=0.20)
        self.fit(content, 4.75, 1.0)
        box = RoundedRectangle(
            width=5.10,
            height=1.25,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.5,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        content.move_to(box)
        return VGroup(box, content)

    def speed_panel(self, value: float = 0.0) -> tuple[VGroup, DecimalNumber]:
        title = self.text("VELOCIDAD DEL AUTO", 20, BOLD)
        speed = DecimalNumber(value, num_decimal_places=0, font_size=44, color=BLACK_TEXT)
        unit = self.text("km/h", 21, MEDIUM).next_to(speed, RIGHT, buff=0.12)
        numeric = VGroup(speed, unit)
        content = VGroup(title, numeric).arrange(DOWN, buff=0.14)
        box = RoundedRectangle(
            width=3.15,
            height=1.45,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        content.move_to(box)
        return VGroup(box, content), speed

    def graph_panel(
        self,
        *,
        kind: str,
        width: float = 8.7,
        height: float = 5.15,
    ) -> tuple[FigurePanel, Axes, VMobject]:
        if kind == "position":
            axes = Axes(
                x_range=[0, 120, 20],
                y_range=[0, 80, 10],
                x_length=7.2,
                y_length=3.45,
                axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
                tips=False,
            )
            ts = np.linspace(0, 120, 180)
            points = [axes.c2p(float(t), position_at(float(t))) for t in ts]
            curve = VMobject(stroke_color=BLACK_LINE, stroke_width=4.0).set_points_smoothly(points)
            x_label = self.text("tiempo (min)", 18)
            y_label = self.text("posición (km)", 18).rotate(PI / 2)
            x_label.next_to(axes.x_axis, DOWN, buff=0.18)
            y_label.next_to(axes.y_axis, LEFT, buff=0.18)
            fig = VGroup(axes, curve, x_label, y_label)
            panel = self.figure_panel(
                fig,
                width=width,
                height=height,
                title="Gráfica posición–tiempo",
                caption="La pendiente local indica qué tan rápido cambia la posición.",
            )
            return panel, axes, curve

        if kind == "velocity":
            axes = Axes(
                x_range=[0, 120, 20],
                y_range=[0, 80, 10],
                x_length=7.2,
                y_length=3.45,
                axis_config={"color": BLACK_LINE, "stroke_width": 1.8, "include_ticks": True},
                tips=False,
            )
            ts = np.linspace(0, 120, 240)
            points = [axes.c2p(float(t), velocity_at(float(t))) for t in ts]
            curve = VMobject(stroke_color=BLACK_LINE, stroke_width=4.0).set_points_as_corners(points)
            x_label = self.text("tiempo (min)", 18)
            y_label = self.text("velocidad (km/h)", 18).rotate(PI / 2)
            x_label.next_to(axes.x_axis, DOWN, buff=0.18)
            y_label.next_to(axes.y_axis, LEFT, buff=0.18)
            fig = VGroup(axes, curve, x_label, y_label)
            panel = self.figure_panel(
                fig,
                width=width,
                height=height,
                title="Gráfica velocidad–tiempo",
                caption="Ahora una sola velocidad no basta: v depende del tiempo.",
            )
            return panel, axes, curve

        raise ValueError(f"Unknown graph kind: {kind}")

    def opening(self) -> None:
        self.standard_opening(
            "FUNDAMENTOS DE FÍSICA 9°",
            "CUANDO LA VELOCIDAD DEJA DE SER CONSTANTE",
            "Del MRU ideal a una descripción más realista de un viaje entre dos ciudades.",
            "Primero observamos el movimiento. Después leemos sus gráficas.",
        )

    def section_1_mru_reference(self) -> None:
        self.set_header(
            1,
            "EL PUNTO DE PARTIDA: MRU",
            "El MRU supone una velocidad constante: distancias iguales durante intervalos de tiempo iguales.",
        )

        road = self.make_road(width=6.1).move_to(ORIGIN)
        car = self.make_car(0.70).move_to(road[0].get_left() + RIGHT * 0.55 + UP * 0.10)
        ticks = VGroup(*[
            Line(DOWN * 0.11, UP * 0.11, color=BLACK_LINE, stroke_width=2.0)
            for _ in range(5)
        ])
        for tick, x in zip(ticks, np.linspace(-2.35, 2.35, 5)):
            tick.move_to([x, -0.47, 0])
        labels = VGroup(*[self.text(f"{15*i} min", 16) for i in range(5)])
        for label, tick in zip(labels, ticks):
            label.next_to(tick, DOWN, buff=0.08)
        visual = VGroup(road, ticks, labels, car)
        left_panel = self.figure_panel(
            visual,
            width=8.7,
            height=4.75,
            title="Modelo ideal de velocidad constante",
            caption="Cada 15 min el auto avanza aproximadamente la misma distancia.",
        )

        formula = self.formula_panel(r"x(t)=x_0+vt", width=4.7, height=1.18, font_size=38)
        idea = self.note_panel(
            "LECTURA FÍSICA",
            [
                "Una sola velocidad describe todo el tramo.",
                "La pendiente de x–t permanece constante.",
                "Es un modelo útil, pero idealizado.",
            ],
            width=4.7,
            body_size=21,
        )
        right = VGroup(formula, idea).arrange(DOWN, buff=0.34)
        layout = self.split_layout(left_panel.group, right, left_width=9.0, right_width=4.8, max_height=5.25, center_y=-0.42)
        self.assert_content_safe(layout.group, "section 1 layout")

        self.play(FadeIn(left_panel.group), FadeIn(right), run_time=RUN_NORMAL)
        for i, x in enumerate(np.linspace(-2.35, 2.35, 5)[1:], start=1):
            self.play(car.animate.move_to([x, 0.10, 0]), run_time=0.72, rate_func=linear)
            self.wait(PAUSE_SHORT * 0.40)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_2_real_trip(self) -> None:
        self.set_header(
            2,
            "UN VIAJE REAL: LA VELOCIDAD CAMBIA",
            "Una ruta de aproximadamente 78 km incluye aceleraciones, una parada, un accidente y tráfico intenso.",
        )

        panel = self.road_panel(width=9.2, height=2.65)
        panel.group.move_to([-2.15, 0.72, 0])
        road = panel.figure[0]
        car = self.make_car(0.63)
        road_left = road[0].get_left()[0] + 0.35
        road_right = road[0].get_right()[0] - 0.35
        car.move_to([road_left, road[0].get_center()[1] + 0.10, 0])
        panel.figure.add(car)

        speed_group, speed = self.speed_panel(0)
        speed_group.move_to([5.10, 0.78, 0])

        event = self.event_card("00", "Inicio", "sale de Ciudad A")
        event.move_to([2.15, -1.72, 0])

        distance_note = self.note_panel(
            "IDEA CENTRAL",
            [
                "En el viaje real no existe una sola v.",
                "La velocidad cambia durante el recorrido.",
            ],
            width=4.7,
            body_size=21,
        )
        distance_note.move_to([-4.20, -1.72, 0])

        stage = VGroup(panel.group, speed_group, event, distance_note)
        self.assert_content_safe(stage, "section 2 stage")
        self.play(FadeIn(panel.group), FadeIn(speed_group), FadeIn(event), FadeIn(distance_note))

        segments = [
            (0.17, 70, EVENTS[0], 1.15),
            (0.35, 70, ("01", "Crucero", "velocidad casi estable"), 1.10),
            (0.43, 0, EVENTS[1], 0.92),
            (0.59, 65, ("02", "Retoma", "vuelve a la carretera"), 1.12),
            (0.70, 25, EVENTS[2], 0.95),
            (0.82, 10, EVENTS[3], 1.15),
            (0.96, 55, EVENTS[4], 1.15),
        ]
        current_event = event
        for fraction, target_v, event_data, run_time in segments:
            number, title, detail = event_data
            target_event = self.event_card(number, title, detail).move_to(current_event)
            x = road_left + fraction * (road_right - road_left)
            self.play(
                car.animate.move_to([x, road[0].get_center()[1] + 0.10, 0]),
                ChangeDecimalToValue(speed, target_v),
                ReplacementTransform(current_event, target_event),
                run_time=run_time,
                rate_func=smooth,
            )
            current_event = target_event
            self.wait(PAUSE_SHORT * 0.55)

        conclusion = self.formula_panel(r"v=v(t)", width=4.4, height=1.02, font_size=39)
        conclusion.move_to([2.15, -3.18, 0])
        self.assert_content_safe(conclusion, "section 2 conclusion")
        self.play(FadeIn(conclusion, shift=UP * 0.10))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_3_position_time(self) -> None:
        self.set_header(
            3,
            "POSICIÓN VS. TIEMPO: LA PENDIENTE CUENTA LA HISTORIA",
            "Si la pendiente cambia, la velocidad también cambia. Un tramo horizontal significa que el auto está detenido.",
        )

        panel, axes, curve = self.graph_panel(kind="position", width=9.0, height=5.25)
        panel.group.move_to([-2.55, -0.50, 0])
        formula = self.formula_panel(r"v\;\longleftrightarrow\;\text{pendiente de }x(t)", width=4.75, height=1.20, font_size=34)
        formula.move_to([5.18, 1.55, 0])
        interpretation = self.event_card("A", "Primer tramo", "pendiente estable → v estable")
        interpretation.move_to([5.18, -0.25, 0])
        concept = self.note_panel(
            "QUÉ DEBO MIRAR",
            [
                "más pendiente → mayor velocidad",
                "menos pendiente → menor velocidad",
                "horizontal → v = 0",
            ],
            width=4.75,
            body_size=20,
        )
        concept.move_to([5.18, -2.35, 0])
        stage = VGroup(panel.group, formula, interpretation, concept)
        self.assert_content_safe(stage, "section 3 stage")

        panel.figure.remove(curve)
        self.play(FadeIn(panel.group), FadeIn(formula), FadeIn(interpretation), FadeIn(concept))
        self.play(Create(curve), run_time=2.0)

        markers = [
            (25, "A", "Crucero", "pendiente casi constante"),
            (48, "B", "Parada", "tramo horizontal → v = 0"),
            (85, "C", "Accidente", "pendiente menor → reduce v"),
            (104, "D", "Tráfico", "pendiente muy pequeña"),
        ]
        current = interpretation
        dot = Dot(axes.c2p(25, position_at(25)), radius=0.085, color=BLACK_LINE)
        guide = DashedLine(
            axes.c2p(25, 0), axes.c2p(25, position_at(25)),
            dash_length=0.07, color=MID_GRAY, stroke_width=1.5,
        )
        self.play(FadeIn(dot), Create(guide))
        for t, number, title, detail in markers:
            target = self.event_card(number, title, detail).move_to(current)
            new_dot = Dot(axes.c2p(t, position_at(t)), radius=0.085, color=BLACK_LINE)
            new_guide = DashedLine(
                axes.c2p(t, 0), axes.c2p(t, position_at(t)),
                dash_length=0.07, color=MID_GRAY, stroke_width=1.5,
            )
            self.play(
                ReplacementTransform(current, target),
                Transform(dot, new_dot),
                Transform(guide, new_guide),
                run_time=0.80,
            )
            current = target
            self.wait(PAUSE_READ * 0.55)

        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_4_velocity_time(self) -> None:
        self.set_header(
            4,
            "VELOCIDAD VS. TIEMPO: AHORA v DEPENDE DE t",
            "La gráfica v–t permite ver directamente cuándo el auto acelera, se detiene, frena o avanza lentamente.",
        )

        panel, axes, curve = self.graph_panel(kind="velocity", width=9.0, height=5.25)
        panel.group.move_to([-2.55, -0.50, 0])
        formula = self.formula_panel(r"v=v(t)", width=4.75, height=1.15, font_size=42)
        formula.move_to([5.18, 1.55, 0])
        event = self.event_card("01", "Acelera", "la gráfica sube")
        event.move_to([5.18, -0.15, 0])
        note = self.note_panel(
            "LECTURA RÁPIDA",
            [
                "sube → velocidad aumenta",
                "baja → velocidad disminuye",
                "sobre v = 0 → auto detenido",
                "horizontal arriba → v constante",
            ],
            width=4.75,
            body_size=19,
        )
        note.move_to([5.18, -2.35, 0])
        stage = VGroup(panel.group, formula, event, note)
        self.assert_content_safe(stage, "section 4 stage")

        panel.figure.remove(curve)
        self.play(FadeIn(panel.group), FadeIn(formula), FadeIn(event), FadeIn(note))
        self.play(Create(curve), run_time=2.0)

        sequence = [
            (10, "01", "Acelera", "0 → 70 km/h"),
            (47, "02", "Parada", "v = 0 durante 15 min"),
            (82, "03", "Accidente", "70 aprox. → 25 km/h"),
            (104, "04", "Tráfico", "avanza a 10 km/h"),
            (115, "05", "Recupera", "acelera hasta 55 km/h"),
        ]
        current = event
        dot = Dot(axes.c2p(10, velocity_at(10)), radius=0.085, color=BLACK_LINE)
        guide = DashedLine(
            axes.c2p(10, 0), axes.c2p(10, velocity_at(10)),
            dash_length=0.07, color=MID_GRAY, stroke_width=1.5,
        )
        self.play(FadeIn(dot), Create(guide))
        for t, number, title, detail in sequence:
            target = self.event_card(number, title, detail).move_to(current)
            new_dot = Dot(axes.c2p(t, velocity_at(t)), radius=0.085, color=BLACK_LINE)
            new_guide = DashedLine(
                axes.c2p(t, 0), axes.c2p(t, velocity_at(t)),
                dash_length=0.07, color=MID_GRAY, stroke_width=1.5,
            )
            self.play(
                ReplacementTransform(current, target),
                Transform(dot, new_dot),
                Transform(guide, new_guide),
                run_time=0.82,
            )
            current = target
            self.wait(PAUSE_READ * 0.50)

        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_5_acceleration(self) -> None:
        self.set_header(
            5,
            "CUANDO CAMBIA v, APARECE LA ACELERACIÓN",
            "Para un intervalo de tiempo usamos la aceleración promedio: mide cuánto cambia la velocidad durante ese intervalo.",
        )

        formula = self.formula_panel(
            r"a_{\mathrm{prom}}=\frac{\Delta v}{\Delta t}",
            width=6.0,
            height=1.30,
            font_size=45,
        )
        formula.move_to([0, 1.60, 0])

        cards = self.process_map(
            [
                ("01", "Acelerar: v aumenta"),
                ("02", "Frenar: v disminuye"),
                ("03", "Detenido: v = 0"),
                ("04", "Crucero: v casi constante"),
            ],
            card_width=5.4,
            card_height=1.20,
            columns=2,
        )
        cards.move_to([0, -0.55, 0])

        note = self.note_panel(
            "PRECISIÓN FÍSICA",
            [
                "Los cambios reales ocurren durante intervalos de tiempo.",
                "No necesitamos imaginar saltos instantáneos de velocidad.",
            ],
            width=11.0,
            body_size=21,
        )
        note.move_to([0, -3.05, 0])
        stage = VGroup(formula, cards, note)
        self.assert_content_safe(stage, "section 5 stage")

        self.play(Write(formula[1]), FadeIn(formula[0]))
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in cards], lag_ratio=0.12), run_time=RUN_SLOW)
        self.play(FadeIn(note))
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def section_6_synthesis(self) -> None:
        self.set_header(
            6,
            "DEL MODELO IDEAL A UNA DESCRIPCIÓN MÁS REALISTA",
            "La física comienza con modelos simples y añade detalle cuando la situación lo exige.",
        )

        ideal = self.note_panel(
            "MRU — MODELO IDEAL",
            [
                "v constante",
                "x–t con pendiente constante",
                "a ≈ 0",
                "una sola velocidad puede bastar",
            ],
            width=6.3,
            body_size=22,
        )
        realistic = self.note_panel(
            "MOVIMIENTO REAL",
            [
                "v cambia con el tiempo",
                "la pendiente de x–t cambia",
                "hay aceleraciones y frenadas",
                "necesitamos v = v(t)",
            ],
            width=6.3,
            body_size=22,
        )
        comparison = self.split_layout(
            ideal,
            realistic,
            left_width=6.55,
            right_width=6.55,
            max_height=3.6,
            gap=0.75,
            center_y=0.10,
        )

        process = self.process_map(
            [
                ("1", "Observa el recorrido"),
                ("2", "Lee x–t"),
                ("3", "Lee v–t"),
                ("4", "Describe los cambios de v"),
            ],
            card_width=3.35,
            card_height=1.08,
            columns=4,
        )
        process.move_to([0, -2.85, 0])
        stage = VGroup(comparison.group, process)
        self.assert_content_safe(stage, "section 6 stage")

        self.play(FadeIn(ideal), FadeIn(realistic))
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in process], lag_ratio=0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()
