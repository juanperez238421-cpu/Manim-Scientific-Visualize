#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Metro relativity V2: simplified, human-centered redesign.

This scene intentionally subclasses the audited V1 render so the project keeps
its proven render infrastructure, but replaces the pedagogical and visual layer.
The V2 design removes tiny 3D/stick people, reduces simultaneous information,
uses large flat human pictograms, and reserves 3D for the metro and light pulse.
"""
from __future__ import annotations

import numpy as np
from manim import *
from metro_relativity_lesson import Physics9MetroRelativity, RUN_QUICK, RUN_NORMAL, RUN_SLOW, RUN_CAMERA, PAUSE_READ, PAUSE_EXPLAIN, PAUSE_WORK, PAUSE_FINAL, BLACK_LINE, MID_GRAY, LIGHT_GRAY, PAPER_GRAY, DARK_GRAY, LIGHT_COLOR


class Physics9MetroRelativityV2(Physics9MetroRelativity):
    """Simplified Spanish classroom version with improved human figures."""

    def limb(self, a, b, width=8):
        line = Line(a, b, color=BLACK_LINE, stroke_width=width)
        return VGroup(line, Dot(a, radius=0.045, color=BLACK_LINE), Dot(b, radius=0.045, color=BLACK_LINE))

    def person(self, pose="stand", scale=1.0, phase=1, lamp=False):
        head = Circle(radius=0.28, stroke_color=BLACK_LINE, stroke_width=3,
                      fill_color=WHITE, fill_opacity=1).shift(UP * 0.98)
        torso = RoundedRectangle(width=0.62, height=1.03, corner_radius=0.22,
                                 stroke_color=BLACK_LINE, stroke_width=3,
                                 fill_color=PAPER_GRAY, fill_opacity=1).shift(UP * 0.16)
        shoulder_y, hip_y = 0.48, -0.32

        if pose == "sit":
            torso.rotate(-6 * DEGREES)
            limbs = VGroup(
                self.limb(np.array([-0.28, shoulder_y, 0]), np.array([-0.52, 0.02, 0]), 7),
                self.limb(np.array([0.28, shoulder_y, 0]), np.array([0.48, 0.05, 0]), 7),
                self.limb(np.array([-0.18, hip_y, 0]), np.array([-0.62, -0.58, 0]), 8),
                self.limb(np.array([-0.62, -0.58, 0]), np.array([-0.60, -1.18, 0]), 8),
                self.limb(np.array([0.18, hip_y, 0]), np.array([0.28, -0.60, 0]), 8),
                self.limb(np.array([0.28, -0.60, 0]), np.array([0.28, -1.18, 0]), 8),
            )
        elif pose == "walk":
            p = 1 if phase >= 0 else -1
            limbs = VGroup(
                self.limb(np.array([-0.28, shoulder_y, 0]), np.array([0.35 * p, -0.02, 0]), 7),
                self.limb(np.array([0.28, shoulder_y, 0]), np.array([-0.35 * p, -0.02, 0]), 7),
                self.limb(np.array([-0.15, hip_y, 0]), np.array([0.46 * p, -1.12, 0]), 9),
                self.limb(np.array([0.15, hip_y, 0]), np.array([-0.46 * p, -1.12, 0]), 9),
            )
        else:
            limbs = VGroup(
                self.limb(np.array([-0.28, shoulder_y, 0]), np.array([-0.40, -0.12, 0]), 7),
                self.limb(np.array([0.28, shoulder_y, 0]), np.array([0.40, -0.12, 0]), 7),
                self.limb(np.array([-0.15, hip_y, 0]), np.array([-0.24, -1.12, 0]), 9),
                self.limb(np.array([0.15, hip_y, 0]), np.array([0.24, -1.12, 0]), 9),
            )

        icon = VGroup(limbs, torso, head)
        if lamp:
            bulb = Circle(radius=0.14, stroke_color=BLACK_LINE, stroke_width=2,
                          fill_color=LIGHT_COLOR, fill_opacity=0.9)
            handle = RoundedRectangle(width=0.12, height=0.26, corner_radius=0.03,
                                      stroke_color=BLACK_LINE, stroke_width=1.6,
                                      fill_color=DARK_GRAY, fill_opacity=1).next_to(bulb, DOWN, buff=0.01)
            icon.add(VGroup(bulb, handle).move_to(RIGHT * 0.62 + UP * 0.08))
        return icon.scale(scale)

    def seat(self, scale=1.0):
        cushion = RoundedRectangle(width=1.15, height=0.30, corner_radius=0.10,
                                   stroke_color=BLACK_LINE, stroke_width=2.4,
                                   fill_color=LIGHT_GRAY, fill_opacity=0.55)
        back = RoundedRectangle(width=0.28, height=1.10, corner_radius=0.08,
                                stroke_color=BLACK_LINE, stroke_width=2.4,
                                fill_color=LIGHT_GRAY, fill_opacity=0.55)
        back.next_to(cushion, LEFT, buff=-0.08).shift(UP * 0.36)
        return VGroup(back, cushion).scale(scale)

    def metro_clean(self, width=11.5, height=3.65):
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.22,
                                 stroke_color=BLACK_LINE, stroke_width=3,
                                 fill_color=WHITE, fill_opacity=1)
        windows = VGroup(*[
            RoundedRectangle(width=1.28, height=0.75, corner_radius=0.08,
                             stroke_color=MID_GRAY, stroke_width=1.8,
                             fill_color=PAPER_GRAY, fill_opacity=1)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.48).shift(UP * 1.02)
        floor = Line(LEFT * (width / 2 - 0.25) + DOWN * 1.25,
                     RIGHT * (width / 2 - 0.25) + DOWN * 1.25,
                     color=BLACK_LINE, stroke_width=3)
        poles = VGroup(*[
            Line([x, -1.25, 0], [x, 1.50, 0], color=LIGHT_GRAY, stroke_width=2)
            for x in (-2.4, 0, 2.4)
        ])
        return VGroup(shell, windows, floor, poles)

    def walk(self, person, start, end, scale=1.0, steps=6, run_time=3.6, lamp=False):
        for i in range(1, steps + 1):
            target = self.person("walk", scale=scale, phase=1 if i % 2 else -1, lamp=lamp)
            target.move_to(interpolate(np.array(start), np.array(end), i / steps))
            self.play(Transform(person, target), run_time=run_time / steps, rate_func=linear)

    def big_result(self, expression, width=6.0, size=44):
        return self.formula_panel(expression, width=width, height=1.18, size=size)

    def construct(self):
        self.opening_v2()
        self.frames_v2()
        self.inside_v2()
        self.outside_v2()
        self.compare_v2()
        self.lamp_v2()
        self.light_v2()
        self.summary_v2()

    def opening_v2(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES, zoom=0.90)
        tracks = self.platform_3d()
        metro = self.make_train_3d().shift(LEFT * 4.2)
        self.play(Create(tracks), FadeIn(metro), run_time=RUN_SLOW)
        title = VGroup(
            self.text("FÍSICA 9 · RELATIVIDAD", 26, BOLD),
            self.text("METRO, MOVIMIENTO RELATIVO Y LUZ", 46, BOLD),
            self.text("Una misma situación vista desde dos observadores", 28),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.45)
        self.show_fixed(title, run_time=RUN_SLOW)
        direction = self.text("Dirección Sur = +x", 26, BOLD).to_edge(DOWN, buff=0.42)
        self.show_fixed(direction)
        self.play(metro.animate.shift(RIGHT * 8.4), run_time=4.0, rate_func=linear)
        self.wait(PAUSE_EXPLAIN)
        self.clear_content(keep_header=False)
        self.header = None

    def frames_v2(self):
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)
        self.set_header(1, "DOS OBSERVADORES, DOS SISTEMAS DE REFERENCIA",
                        "Dentro: una estudiante sentada. Fuera: una persona quieta en la estación.")
        metro = self.metro_clean(9.4).move_to(LEFT * 2.3 + DOWN * 0.1)
        seated = self.person("sit", 1.0).move_to(LEFT * 4.15 + DOWN * 0.05)
        seat = self.seat(1.0).move_to(LEFT * 4.75 + DOWN * 0.56)
        walker = self.person("stand", 1.0).move_to(LEFT * 0.2 + DOWN * 0.08)
        ground = Line(RIGHT * 3.9 + DOWN * 1.50, RIGHT * 6.7 + DOWN * 1.50, color=BLACK_LINE, stroke_width=4)
        observer = self.person("stand", 0.92).move_to(RIGHT * 5.35 + DOWN * 0.35)
        self.play(FadeIn(metro), FadeIn(seat), FadeIn(seated), FadeIn(walker), Create(ground), FadeIn(observer), run_time=RUN_SLOW)
        left = self.note_panel("DENTRO DEL METRO", ["El metro está en reposo para ti.", "Mides lo que ocurre en el pasillo."], width=5.0, body_size=25)
        right = self.note_panel("EN LA ESTACIÓN", ["El suelo está en reposo.", "El metro pasa a 80 km/h."], width=5.0, body_size=25)
        left.move_to(LEFT * 4.2 + DOWN * 2.65)
        right.move_to(RIGHT * 4.7 + DOWN * 2.65)
        self.show_fixed(left); self.show_fixed(right)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def inside_v2(self):
        self.set_header(2, "DESDE EL ASIENTO: LA PERSONA CAMINA A 2 km/h",
                        "Las paredes del metro no se mueven respecto a ti; solo ves a la persona avanzar.")
        metro = self.metro_clean(12.4).move_to(DOWN * 0.08)
        seat = self.seat(1.08).move_to(LEFT * 5.0 + DOWN * 0.58)
        seated = self.person("sit", 1.08).move_to(LEFT * 4.35 + DOWN * 0.08)
        start, end = np.array([-1.9, -0.06, 0]), np.array([2.45, -0.06, 0])
        walker = self.person("walk", 1.10, phase=1).move_to(start)
        self.play(FadeIn(metro), FadeIn(seat), FadeIn(seated), FadeIn(walker), run_time=RUN_SLOW)
        you = self.text("OBSERVADOR DENTRO", 23, BOLD).next_to(seated, UP, buff=0.18)
        self.play(Write(you), run_time=RUN_NORMAL)
        self.walk(walker, start, end, scale=1.10)
        result = self.big_result(r"v_{\mathrm{persona/metro}}=2\;\mathrm{km/h}", width=6.6)
        result.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(result, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def outside_v2(self):
        self.set_header(3, "DESDE LA ESTACIÓN: EL METRO LLEVA A LA PERSONA",
                        "A velocidades cotidianas sumamos la velocidad del metro y la velocidad de caminar.")
        ground = Line(LEFT * 7 + DOWN * 1.55, RIGHT * 7 + DOWN * 1.55, color=BLACK_LINE, stroke_width=4)
        observer = self.person("stand", 0.95).move_to(RIGHT * 6 + DOWN * 0.35)
        metro = self.metro_clean(8.0).scale(0.78).move_to(LEFT * 4.7 + DOWN * 0.05)
        walker = self.person("walk", 0.82, phase=1).move_to(LEFT * 5.1 + DOWN * 0.08)
        self.play(Create(ground), FadeIn(observer), FadeIn(metro), FadeIn(walker), run_time=RUN_SLOW)
        arrow = Arrow(LEFT * 6.4 + DOWN * 2.30, LEFT * 1.6 + DOWN * 2.30, buff=0, color=BLACK_LINE, stroke_width=4)
        lab = self.math(r"80\;\mathrm{km/h}", 30).next_to(arrow, UP, buff=0.10)
        self.play(GrowArrow(arrow), Write(lab), run_time=RUN_NORMAL)
        self.play(metro.animate.shift(RIGHT * 6.4), walker.animate.shift(RIGHT * 6.62), run_time=4.0, rate_func=linear)
        eq1 = self.big_result(r"80+2", width=3.5, size=48).move_to(LEFT * 3.8 + UP * 1.80)
        eq2 = self.big_result(r"82\;\mathrm{km/h}", width=4.5, size=48).move_to(LEFT * 3.8 + UP * 0.40)
        self.play(FadeIn(eq1), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(TransformFromCopy(eq1, eq2), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def compare_v2(self):
        self.set_header(4, "MISMA PERSONA · DOS VELOCIDADES CORRECTAS",
                        "2 km/h y 82 km/h corresponden a observadores diferentes.")
        divider = Line(UP * 2.4, DOWN * 3.2, color=LIGHT_GRAY, stroke_width=2)
        left = self.person("walk", 1.20, phase=1).move_to(LEFT * 4.1 + DOWN * 0.20)
        right = self.person("walk", 1.20, phase=-1).move_to(RIGHT * 4.1 + DOWN * 0.20)
        self.play(Create(divider), FadeIn(left), FadeIn(right), run_time=RUN_SLOW)
        ltitle = self.text("DENTRO", 31, BOLD).move_to(LEFT * 4.1 + UP * 1.80)
        rtitle = self.text("ESTACIÓN", 31, BOLD).move_to(RIGHT * 4.1 + UP * 1.80)
        lres = self.big_result(r"2\;\mathrm{km/h}", 4.0, 48).move_to(LEFT * 4.1 + DOWN * 2.05)
        rres = self.big_result(r"82\;\mathrm{km/h}", 4.0, 48).move_to(RIGHT * 4.1 + DOWN * 2.05)
        self.play(Write(ltitle), Write(rtitle), FadeIn(lres), FadeIn(rres), run_time=RUN_NORMAL)
        takeaway = self.text("La velocidad depende del sistema de referencia.", 32, BOLD).to_edge(DOWN, buff=0.24)
        self.play(Write(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def lamp_v2(self):
        self.set_header(5, "LA PERSONA ENCIENDE UNA LÁMPARA",
                        "Corrección importante: la velocidad de la luz es aproximadamente 300 000 km/s, no km/h.")
        metro = self.metro_clean(11.8).move_to(DOWN * 0.10)
        seated = self.person("sit", 1.02).move_to(LEFT * 4.75 + DOWN * 0.05)
        seat = self.seat(1.0).move_to(LEFT * 5.30 + DOWN * 0.55)
        source = self.person("stand", 1.18, lamp=True).move_to(LEFT * 1.8 + DOWN * 0.04)
        self.play(FadeIn(metro), FadeIn(seat), FadeIn(seated), FadeIn(source), run_time=RUN_SLOW)
        wrong = self.math(r"300\,000\;\mathrm{km/h}", 43).move_to(RIGHT * 3.7 + UP * 1.35)
        cross = Line(wrong.get_corner(UL) + LEFT * 0.1, wrong.get_corner(DR) + RIGHT * 0.1, color=MID_GRAY, stroke_width=4)
        correct = self.big_result(r"c\approx300\,000\;\mathrm{km/s}", 5.8, 42).move_to(RIGHT * 3.7 + DOWN * 0.10)
        self.play(Write(wrong), Create(cross), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(correct, shift=UP * 0.10), run_time=RUN_NORMAL)
        center = source.get_center() + RIGHT * 0.70 + UP * 0.10
        rings = VGroup(*[Circle(radius=r, color=LIGHT_COLOR, stroke_width=3).move_to(center) for r in (0.25, 0.55, 0.90, 1.30)])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.18), run_time=RUN_SLOW)
        statement = self.text("Dentro del metro, la estudiante mide c.", 31, BOLD).to_edge(DOWN, buff=0.25)
        self.play(Write(statement), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def light_v2(self):
        self.set_header(6, "DESDE LA ESTACIÓN, LA LUZ TAMBIÉN VIAJA A c",
                        "Aquí aparece la relatividad especial: no usamos c + 80.")
        self.move_camera(phi=62 * DEGREES, theta=-46 * DEGREES, zoom=0.92, run_time=RUN_CAMERA)
        tracks = self.platform_3d()
        metro = self.make_train_3d().shift(LEFT * 2.5)
        emission = np.array([-2.5, -1.15, 0.10])
        pulse = self.light_pulse(emission)
        flash = Sphere(radius=0.11, resolution=(10, 18)).set_fill(LIGHT_COLOR, opacity=0.95).set_stroke(LIGHT_COLOR, opacity=0.95).move_to(emission)
        self.play(Create(tracks), FadeIn(metro), FadeIn(flash), FadeIn(pulse), run_time=RUN_SLOW)
        self.play(pulse.animate.scale(8.0), metro.animate.shift(RIGHT * 5.2), run_time=4.2, rate_func=linear)
        not_cplus = self.text("NO: c + 80", 31, BOLD).move_to(LEFT * 4.8 + DOWN * 2.55)
        yes_c = self.text("SÍ: c", 39, BOLD).move_to(RIGHT * 4.7 + DOWN * 2.55)
        self.show_fixed(not_cplus); self.show_fixed(yes_c)
        self.wait(PAUSE_EXPLAIN)
        law = self.big_result(r"u=\frac{u'+v}{1+\frac{u'v}{c^2}}\;\;\xrightarrow{\;u'=c\;}\;\;u=c", 9.8, 38).to_edge(DOWN, buff=0.18)
        self.show_fixed(law)
        self.wait(PAUSE_WORK)
        self.clear_content()

    def summary_v2(self):
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=RUN_CAMERA)
        self.set_header(7, "RESUMEN FINAL", "Materia cotidiana: suma clásica. Luz: todos los observadores inerciales miden c.")
        rows = [
            ("Metro", "0 km/h", "80 km/h"),
            ("Persona", "2 km/h", "82 km/h"),
            ("Luz", "c", "c"),
        ]
        headers = VGroup(self.text("OBJETO", 25, BOLD), self.text("DENTRO", 25, BOLD), self.text("ESTACIÓN", 25, BOLD)).arrange(RIGHT, buff=2.25)
        headers.move_to(UP * 1.65)
        self.play(Write(headers), run_time=RUN_NORMAL)
        table_rows = VGroup()
        for name, inside, outside in rows:
            row = VGroup(self.text(name, 27, BOLD), self.text(inside, 27), self.text(outside, 27))
            row[0].set_x(-4.0); row[1].set_x(0); row[2].set_x(4.0)
            table_rows.add(row)
        table_rows.arrange(DOWN, buff=0.62).move_to(DOWN * 0.10)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in table_rows], lag_ratio=0.15), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        final = VGroup(
            self.text("80 + 2 = 82 km/h", 33, BOLD),
            self.text("pero la luz: c → c", 33, BOLD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.30)
        self.play(Write(final), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        question = VGroup(
            self.text("PREGUNTA DE SALIDA", 25, BOLD),
            self.text("¿Por qué c + 80 no describe la velocidad de la luz?", 34, BOLD),
        ).arrange(DOWN, buff=0.18)
        self.play(FadeOut(headers), FadeOut(table_rows), FadeOut(final), run_time=RUN_NORMAL)
        self.play(FadeIn(question, shift=UP * 0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)


# Preview: manim -pql metro_relativity_v2_simplified.py Physics9MetroRelativityV2 --disable_caching
# Final:   manim -pqh metro_relativity_v2_simplified.py Physics9MetroRelativityV2 --disable_caching
