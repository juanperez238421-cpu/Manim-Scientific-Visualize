#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Free Fall / Weight / Apparent Weight / Weightlessness
Senior QA V3 — cinematic classroom rebuild

ManimCE 0.20.x
1920x1080 @ 30 fps
No external assets
"""

from __future__ import annotations
import math
import os
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#F4F7FA"

G = 9.81
M = 60.0
H = 20.0
T_HIT = math.sqrt(2 * H / G)
V_HIT = G * T_HIT
A_E = 3.0
N0 = M * G
NUP = M * (G + A_E)
NDOWN = M * (G - A_E)
R_E = 6371.0
H_ORB = 400.0
G_ORB = G * (R_E / (R_E + H_ORB)) ** 2
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BG = "#F4F7FA"
INK = "#102A43"
BLUE = "#1976D2"
CYAN = "#00838F"
RED = "#C62828"
GREEN = "#2E7D32"
ORANGE = "#EF6C00"
PURPLE = "#6A1B9A"
MID = "#52606D"
LIGHT = "#D9E2EC"
WHITE2 = "#FFFFFF"
PBLUE = "#EAF3FF"
PRED = "#FDECEC"
PGREEN = "#EAF6EC"
PORANGE = "#FFF2E5"
PPURPLE = "#F3EAF8"


def validate():
    assert abs(N0 - 588.6) < 1e-9
    assert abs(NUP - 768.6) < 1e-9
    assert abs(NDOWN - 408.6) < 1e-9
    assert abs(0.5 * G * T_HIT**2 - H) < 1e-10
    assert abs(V_HIT - math.sqrt(2 * G * H)) < 1e-10
    assert 0.88 < G_ORB / G < 0.89


class Physics9FreeFallSeniorQAV3(MovingCameraScene):
    def setup(self):
        super().setup()
        validate()
        self.camera.background_color = BG
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Core style
    # ------------------------------------------------------------------
    def txt(self, s, size=30, weight=NORMAL, color=INK, **kwargs):
        return Text(s, font_size=size, weight=weight, color=color, line_spacing=0.9, **kwargs)

    def math(self, s, size=40, color=INK):
        return MathTex(s, font_size=size, color=color)

    def fit(self, mob, w=14.6, h=7.4):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def section(self, n, title, subtitle):
        badge = RoundedRectangle(
            width=0.68, height=0.52, corner_radius=0.14,
            stroke_width=0, fill_color=INK, fill_opacity=1,
        )
        num = self.txt(str(n), 21, BOLD, WHITE).move_to(badge)
        title_m = self.txt(title, 30, BOLD, INK)
        head = VGroup(VGroup(badge, num), title_m).arrange(RIGHT, buff=0.18)
        self.fit(head, 14.3, 0.62)

        sub = self.txt(subtitle, 20, color=MID)
        self.fit(sub, 14.4, 0.50)
        group = VGroup(head, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        group.to_edge(UP, buff=0.26).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT*7.45, RIGHT*7.45, color=LIGHT, stroke_width=1.8)
        rule.next_to(group, DOWN, buff=0.13)

        self.play(FadeIn(group, shift=RIGHT*0.14), Create(rule), run_time=0.45)
        return VGroup(group, rule)

    def clear_stage(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.42)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def card(self, title, lines, width=5.8, height=None, fill=WHITE2, accent=INK,
             title_size=25, body_size=22):
        title_m = self.txt(title, title_size, BOLD, accent)
        body = VGroup(*[self.txt(line, body_size, color=INK) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width-0.62, 4.5)
        hh = height if height else max(1.35, content.height + 0.60)
        box = RoundedRectangle(
            width=width, height=hh, corner_radius=0.16,
            stroke_color=LIGHT, stroke_width=1.6,
            fill_color=fill, fill_opacity=1,
        )
        bar = Rectangle(
            width=0.10, height=hh-0.16,
            stroke_width=0, fill_color=accent, fill_opacity=1,
        ).next_to(box.get_left(), RIGHT, buff=0.07)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.40)
        return VGroup(box, bar, content)

    def formula(self, expr, width=6.0, height=1.05, size=40, fill=PBLUE, color=INK):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=LIGHT, stroke_width=1.5,
            fill_color=fill, fill_opacity=1,
        )
        eq = self.math(expr, size, color)
        self.fit(eq, width-0.45, height-0.23)
        eq.move_to(box)
        return VGroup(box, eq)

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def ball(self, center, r=0.26, color=BLUE):
        c = Circle(
            radius=r, stroke_color=color, stroke_width=3,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(center)
        shine = Dot(np.array(center) + LEFT*0.07 + UP*0.08, radius=r*0.14, color=color)
        return VGroup(c, shine)

    def block(self, center, label, side=0.92, color=BLUE):
        b = RoundedRectangle(
            width=side, height=side, corner_radius=0.10,
            stroke_color=color, stroke_width=3,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(center)
        t = self.txt(label, 20, BOLD, color).move_to(b)
        return VGroup(b, t)

    def person(self, center, scale=1.0):
        c = np.array(center)
        head = Circle(
            radius=0.18*scale, stroke_color=INK, stroke_width=3,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(c + UP*0.70*scale)
        body = Line(c+UP*0.50*scale, c+DOWN*0.25*scale, color=INK, stroke_width=4)
        arms = VGroup(
            Line(c+UP*0.26*scale, c+LEFT*0.34*scale, color=INK, stroke_width=3),
            Line(c+UP*0.26*scale, c+RIGHT*0.34*scale, color=INK, stroke_width=3),
        )
        legs = VGroup(
            Line(c+DOWN*0.25*scale, c+LEFT*0.25*scale+DOWN*0.72*scale, color=INK, stroke_width=3),
            Line(c+DOWN*0.25*scale, c+RIGHT*0.25*scale+DOWN*0.72*scale, color=INK, stroke_width=3),
        )
        return VGroup(head, body, arms, legs)

    def vector(self, start, vec, label, color, side=RIGHT, label_size=28, stroke=6):
        a = Arrow(
            start=start, end=start+vec, buff=0,
            color=color, stroke_width=stroke,
            max_tip_length_to_length_ratio=0.17,
        )
        l = self.math(label, label_size, color).next_to(a, side, buff=0.10)
        return VGroup(a, l)

    def cabin(self, center, width=5.8, height=5.4):
        c = np.array(center)
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.16,
            stroke_color=INK, stroke_width=3,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(c)
        floor = Line(
            c+LEFT*(width*0.42)+DOWN*(height*0.31),
            c+RIGHT*(width*0.42)+DOWN*(height*0.31),
            color=INK, stroke_width=4,
        )
        roof = Line(
            c+LEFT*(width*0.42)+UP*(height*0.31),
            c+RIGHT*(width*0.42)+UP*(height*0.31),
            color=LIGHT, stroke_width=2,
        )
        return VGroup(shell, floor, roof)

    def scale_pad(self, center):
        pad = RoundedRectangle(
            width=1.75, height=0.30, corner_radius=0.05,
            stroke_color=GREEN, stroke_width=2.7,
            fill_color=PGREEN, fill_opacity=1,
        ).move_to(center)
        display = RoundedRectangle(
            width=0.82, height=0.38, corner_radius=0.05,
            stroke_color=GREEN, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).next_to(pad, DOWN, buff=0.10)
        return VGroup(pad, display)

    def earth(self, center, r=1.72):
        body = Circle(
            radius=r, stroke_color=BLUE, stroke_width=3,
            fill_color=PBLUE, fill_opacity=1,
        ).move_to(center)
        land1 = Arc(
            radius=r*0.68, start_angle=0.2, angle=1.35,
            color=GREEN, stroke_width=6,
        ).move_to(np.array(center)+LEFT*0.24+UP*0.08)
        land2 = Arc(
            radius=r*0.48, start_angle=2.7, angle=1.35,
            color=CYAN, stroke_width=6,
        ).move_to(np.array(center)+RIGHT*0.28+DOWN*0.25)
        return VGroup(body, land1, land2)

    # ------------------------------------------------------------------
    # Main
    # ------------------------------------------------------------------
    def construct(self):
        self.opening()
        self.chapter_release_and_toss()
        self.chapter_mass_and_force()
        self.chapter_apparent_weight()
        self.chapter_weightlessness()
        self.chapter_motion_and_graphs()
        self.chapter_drag()
        self.chapter_qa()
        self.closing()

    # ------------------------------------------------------------------
    # Opening hook
    # ------------------------------------------------------------------
    def opening(self):
        # Large elevator cutaway
        cab = self.cabin(LEFT*3.65, 6.0, 6.0)
        scale = self.scale_pad(LEFT*3.65 + DOWN*2.05)
        human = self.person(LEFT*3.65 + DOWN*0.80, 1.35)
        w = self.vector(LEFT*2.78+UP*0.05, DOWN*1.55, r"\vec W", RED)
        n = self.vector(LEFT*4.52+DOWN*1.42, UP*1.55, r"\vec N", GREEN, LEFT)

        big_q = self.txt("¿POR QUÉ FLOTAMOS\nSI LA GRAVEDAD SIGUE AHÍ?", 42, BOLD, INK)
        big_q.move_to(RIGHT*3.25 + UP*1.35)
        self.fit(big_q, 6.7, 2.0)

        premise = self.card(
            "IDEA CENTRAL",
            [
                "Peso gravitatorio: W = mg",
                "Lectura de báscula: N",
                "En caída libre: N → 0, pero W ≠ 0",
            ],
            6.2, 2.45, fill=PPURPLE, accent=PURPLE,
            title_size=25, body_size=24,
        ).move_to(RIGHT*3.25 + DOWN*0.70)

        self.play(FadeIn(cab), FadeIn(scale), FadeIn(human), run_time=0.8)
        self.play(FadeIn(w), FadeIn(n), run_time=0.7)
        self.play(FadeIn(big_q, shift=UP*0.15), FadeIn(premise), run_time=0.8)
        self.wait(2.0)

        free = self.txt("CAÍDA LIBRE", 31, BOLD, BLUE).move_to(RIGHT*3.25 + DOWN*2.45)
        self.play(
            FadeOut(n),
            human.animate.shift(UP*0.55),
            scale.animate.shift(DOWN*0.13),
            cab.animate.shift(DOWN*0.20),
            FadeIn(free),
            run_time=1.0,
        )
        self.wait(1.7)

        title = self.txt("CAÍDA LIBRE · PESO · INGRAVIDEZ", 36, BOLD, INK)
        title.to_edge(DOWN, buff=0.12)
        self.play(FadeIn(title))
        self.wait(1.8)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Chapter 1
    # ------------------------------------------------------------------
    def chapter_release_and_toss(self):
        self.section(
            1,
            "¿QUÉ CAMBIA AL SOLTAR UN OBJETO?",
            "La caída libre ideal se define por las fuerzas: después de soltar, la gravedad queda como fuerza relevante.",
        )

        # Central object with support
        support = RoundedRectangle(
            width=2.6, height=0.38, corner_radius=0.05,
            stroke_color=GREEN, stroke_width=3,
            fill_color=PGREEN, fill_opacity=1,
        ).move_to(LEFT*3.90 + DOWN*1.20)
        obj = self.block(LEFT*3.90 + DOWN*0.45, "m", 1.05, BLUE)
        ground = Line(LEFT*6.55+DOWN*2.20, LEFT*1.15+DOWN*2.20, color=INK, stroke_width=3)
        w = self.vector(obj.get_center()+RIGHT*0.82, DOWN*1.45, r"\vec W= m\vec g", RED)
        n = self.vector(obj.get_center()+LEFT*0.82+DOWN*0.45, UP*1.45, r"\vec N", GREEN, LEFT)

        before = self.card(
            "ANTES",
            ["N = W", "ΣF = 0", "a = 0"],
            5.7, 2.1, fill=PGREEN, accent=GREEN,
            title_size=26, body_size=27,
        ).move_to(RIGHT*3.45 + UP*0.35)

        self.play(Create(ground), FadeIn(support), FadeIn(obj))
        self.play(FadeIn(w), FadeIn(n), FadeIn(before))
        self.wait(1.8)

        release = self.txt("SOLTAR", 33, BOLD, ORANGE).move_to(ORIGIN+UP*1.65)
        self.play(FadeIn(release, scale=1.2))
        self.play(
            support.animate.shift(DOWN*1.0).set_opacity(0.15),
            FadeOut(n), FadeOut(before),
            run_time=0.85,
        )

        after = self.card(
            "DESPUÉS",
            ["N = 0", "ΣF = W = mg", "a = g hacia abajo"],
            5.7, 2.2, fill=PRED, accent=RED,
            title_size=26, body_size=27,
        ).move_to(RIGHT*3.45 + UP*0.35)
        a = self.vector(obj.get_center()+LEFT*0.82+UP*0.38, DOWN*1.45, r"\vec a=\vec g", ORANGE, LEFT)
        self.play(FadeIn(after), FadeIn(a), FadeOut(release))
        self.play(
            obj.animate.shift(DOWN*0.85),
            w.animate.shift(DOWN*0.85),
            a.animate.shift(DOWN*0.85),
            run_time=1.0,
        )

        law = self.formula(
            r"\boxed{\sum\vec F=m\vec a=m\vec g\Rightarrow \vec a=\vec g}",
            7.2, 1.10, 34, PBLUE,
        ).move_to(RIGHT*3.45 + DOWN*1.55)
        self.play(FadeIn(law))
        self.wait(2.2)

        # Transition to toss, use same object
        self.play(
            FadeOut(ground), FadeOut(support), FadeOut(w), FadeOut(a),
            FadeOut(after), FadeOut(law),
            obj.animate.move_to(LEFT*3.50 + DOWN*1.65),
            run_time=0.65,
        )

        toss_title = self.txt("SUBIR TAMBIÉN ES CAÍDA LIBRE", 28, BOLD, BLUE).move_to(RIGHT*2.75+UP*1.75)
        toss_note = self.card(
            "LA ACELERACIÓN NO SE APAGA",
            [
                "Subiendo: v > 0",
                "En la cima: v = 0 instantáneamente",
                "Bajando: v < 0",
                "Siempre: a = −g",
            ],
            6.7, 3.0, fill=PBLUE, accent=BLUE,
            title_size=24, body_size=22,
        ).move_to(RIGHT*2.75+DOWN*0.10)
        self.play(FadeIn(toss_title), FadeIn(toss_note))

        path = DashedLine(LEFT*3.50+DOWN*1.90, LEFT*3.50+UP*2.05, color=LIGHT, dash_length=0.12)
        acc = self.vector(LEFT*2.55+UP*1.55, DOWN*1.35, r"\vec a=-g\hat y", ORANGE)
        self.play(Create(path), FadeIn(acc))

        vup = self.vector(obj.get_center()+LEFT*0.72, UP*1.45, r"\vec v", BLUE, LEFT)
        self.play(FadeIn(vup))
        self.play(obj.animate.move_to(LEFT*3.50+UP*1.45), vup.animate.scale(0.35).shift(UP*3.05), run_time=1.35)
        self.play(FadeOut(vup))
        apex = self.txt("v = 0", 34, BOLD, BLUE).move_to(LEFT*4.55+UP*1.55)
        self.play(FadeIn(apex))
        self.wait(1.0)

        vdown = self.vector(LEFT*4.22+UP*1.10, DOWN*1.20, r"\vec v", BLUE, LEFT)
        self.play(FadeOut(apex), FadeIn(vdown))
        self.play(obj.animate.move_to(LEFT*3.50+DOWN*1.15), vdown.animate.scale(1.35).shift(DOWN*2.55), run_time=1.2)
        self.wait(2.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Chapter 2
    # ------------------------------------------------------------------
    def chapter_mass_and_force(self):
        self.section(
            2,
            "¿EL OBJETO MÁS PESADO CAE MÁS RÁPIDO?",
            "En vacío, no: más masa implica más peso, pero también más inercia.",
        )

        x1, x2 = -4.35, -1.35
        y0, yg = 1.75, -2.0
        rail1 = DashedLine([x1,y0,0],[x1,yg,0],color=LIGHT)
        rail2 = DashedLine([x2,y0,0],[x2,yg,0],color=LIGHT)
        b1 = self.block(np.array([x1,y0,0]), "1 kg", 1.0, CYAN)
        b5 = self.block(np.array([x2,y0,0]), "5 kg", 1.15, PURPLE)
        self.play(Create(rail1), Create(rail2), FadeIn(b1), FadeIn(b5))

        f1 = self.vector(b1.get_center()+RIGHT*0.75, DOWN*0.95, r"W_1", RED)
        f5 = self.vector(b5.get_center()+RIGHT*0.85, DOWN*1.45, r"W_5", RED)
        self.play(FadeIn(f1), FadeIn(f5))

        deriv = VGroup(
            self.formula(r"m_1a_1=m_1g\Rightarrow a_1=g", 6.2, 1.05, 35, PBLUE),
            self.formula(r"m_5a_5=m_5g\Rightarrow a_5=g", 6.2, 1.05, 35, PPURPLE),
            self.formula(r"\boxed{a_1=a_5=g}", 6.2, 1.05, 40, PGREEN),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT*3.65+UP*0.30)
        for eq in deriv:
            self.play(FadeIn(eq), run_time=0.45)

        dots = VGroup()
        for frac in [0.25,0.50,0.75]:
            yy = y0 - (y0-yg)*(frac**2)
            dots.add(Dot([x1,yy,0],radius=0.08,color=CYAN))
            dots.add(Dot([x2,yy,0],radius=0.08,color=PURPLE))
        self.play(FadeIn(dots, lag_ratio=0.08))

        self.play(
            b1.animate.move_to([x1,yg,0]),
            b5.animate.move_to([x2,yg,0]),
            f1.animate.shift(DOWN*(y0-yg)),
            f5.animate.shift(DOWN*(y0-yg)),
            run_time=2.0,
            rate_func=rate_functions.ease_in_quad,
        )
        together = self.txt("MISMO TIEMPO", 29, BOLD, GREEN).move_to(LEFT*2.80+DOWN*2.55)
        note = self.card(
            "CONDICIÓN",
            ["Esto vale para caída libre ideal.", "Con aire, la forma y el arrastre importan."],
            6.2, 1.75, fill=PORANGE, accent=ORANGE,
            title_size=23, body_size=22,
        ).move_to(RIGHT*3.65+DOWN*2.05)
        self.play(FadeIn(together), FadeIn(note))
        self.wait(2.4)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Chapter 3
    # ------------------------------------------------------------------
    def chapter_apparent_weight(self):
        self.section(
            3,
            "PESO REAL Y PESO APARENTE",
            "En esta clase: W = mg es la fuerza gravitatoria; la báscula responde a la fuerza normal N.",
        )

        cab = self.cabin(LEFT*3.55, 6.2, 5.6)
        scale = self.scale_pad(LEFT*3.55+DOWN*1.78)
        person = self.person(LEFT*3.55+DOWN*0.67,1.22)
        w = self.vector(LEFT*2.75+UP*0.10, DOWN*1.45, r"W=mg", RED)
        n = self.vector(LEFT*4.35+DOWN*1.10, UP*1.45, r"N", GREEN, LEFT)
        self.play(FadeIn(cab),FadeIn(scale),FadeIn(person),FadeIn(w),FadeIn(n))

        title = self.txt("REPOSO / v CONSTANTE", 27, BOLD, INK).move_to(RIGHT*3.45+UP*1.75)
        eq = self.formula(r"N-mg=0\Rightarrow N=mg",6.2,1.10,38,PGREEN).move_to(RIGHT*3.45+UP*0.70)
        read = self.card("BÁSCULA", [f"N = {N0:.1f} N"], 5.0, 1.35, fill=PGREEN, accent=GREEN,
                         title_size=23, body_size=28).move_to(RIGHT*3.45+DOWN*0.65)
        self.play(FadeIn(title),FadeIn(eq),FadeIn(read))
        self.wait(1.6)

        # Upward acceleration
        t2 = self.txt("ACELERA HACIA ARRIBA",27,BOLD,INK).move_to(title)
        e2 = self.formula(r"N=m(g+a)",6.2,1.10,42,PGREEN).move_to(eq)
        r2 = self.card("TE SIENTES MÁS PESADO",[f"N = {NUP:.1f} N"],5.0,1.35,fill=PGREEN,accent=GREEN,
                       title_size=22,body_size=28).move_to(read)
        n2 = self.vector(LEFT*4.35+DOWN*1.10,UP*1.85,r"N",GREEN,LEFT)
        au = self.vector(LEFT*1.05+DOWN*0.25,UP*1.35,r"\vec a",ORANGE)
        self.play(
            FadeOut(title),FadeOut(eq),FadeOut(read),
            FadeIn(t2),FadeIn(e2),FadeIn(r2),
            Transform(n,n2),FadeIn(au),run_time=0.72
        )
        title,eq,read = t2,e2,r2
        self.wait(1.5)

        # Downward acceleration
        t3 = self.txt("ACELERA HACIA ABAJO",27,BOLD,INK).move_to(title)
        e3 = self.formula(r"N=m(g-a)",6.2,1.10,42,PORANGE).move_to(eq)
        r3 = self.card("TE SIENTES MÁS LIVIANO",[f"N = {NDOWN:.1f} N"],5.0,1.35,fill=PORANGE,accent=ORANGE,
                       title_size=22,body_size=28).move_to(read)
        n3 = self.vector(LEFT*4.35+DOWN*1.10,UP*0.98,r"N",GREEN,LEFT)
        ad = self.vector(LEFT*1.05+UP*0.80,DOWN*1.35,r"\vec a",ORANGE)
        self.play(
            FadeOut(title),FadeOut(eq),FadeOut(read),
            FadeIn(t3),FadeIn(e3),FadeIn(r3),
            Transform(n,n3),Transform(au,ad),run_time=0.72
        )
        title,eq,read = t3,e3,r3
        self.wait(1.5)

        # Free fall
        t4 = self.txt("CAÍDA LIBRE DEL ASCENSOR",27,BOLD,BLUE).move_to(title)
        e4 = self.formula(r"N-mg=-mg\Rightarrow \boxed{N=0}",6.2,1.10,39,PPURPLE).move_to(eq)
        r4 = self.card("INGRAVIDEZ APARENTE",["La báscula deja de comprimirse."],5.0,1.45,fill=PPURPLE,accent=PURPLE,
                       title_size=22,body_size=22).move_to(read)
        af = self.vector(LEFT*1.05+UP*0.80,DOWN*1.55,r"\vec a=\vec g",ORANGE)
        self.play(
            FadeOut(title),FadeOut(eq),FadeOut(read),
            FadeIn(t4),FadeIn(e4),FadeIn(r4),
            FadeOut(n),Transform(au,af),
            person.animate.shift(UP*0.55),scale.animate.shift(DOWN*0.12),
            run_time=0.85,
        )
        title,eq,read = t4,e4,r4

        key = self.txt("N = 0   pero   W = mg ≠ 0",31,BOLD,PURPLE).move_to(RIGHT*3.45+DOWN*2.20)
        self.play(FadeIn(key,scale=1.08))
        self.wait(2.5)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Chapter 4
    # ------------------------------------------------------------------
    def chapter_weightlessness(self):
        self.section(
            4,
            "INGRAVIDEZ APARENTE: TODOS CAEN JUNTOS",
            "La persona, la nave y los objetos comparten casi la misma aceleración gravitatoria.",
        )

        # Left lab
        cab = self.cabin(LEFT*3.75,5.7,5.25)
        p = self.person(LEFT*4.25+UP*0.05,1.08)
        ball = self.ball(LEFT*2.85+UP*0.85,0.27,BLUE)
        coin = Dot(LEFT*2.95+DOWN*0.55,radius=0.13,color=ORANGE)
        self.play(FadeIn(cab),FadeIn(p),FadeIn(ball),FadeIn(coin))

        g1 = self.vector(LEFT*4.95+UP*1.48,DOWN*1.15,r"\vec g",ORANGE,LEFT,24)
        g2 = self.vector(LEFT*3.45+UP*1.48,DOWN*1.15,r"\vec g",ORANGE,LEFT,24)
        g3 = self.vector(LEFT*2.15+UP*1.48,DOWN*1.15,r"\vec g",ORANGE,RIGHT,24)
        self.play(FadeIn(g1),FadeIn(g2),FadeIn(g3))

        labnote = self.card(
            "DENTRO DE LA CABINA",
            ["N ≈ 0", "Objetos flotan relativamente", "No significa g = 0"],
            5.2,2.25,fill=PPURPLE,accent=PURPLE,
            title_size=24,body_size=23,
        ).move_to(LEFT*3.75+DOWN*2.35)
        self.play(FadeIn(labnote))
        self.play(p.animate.shift(UP*0.25),ball.animate.shift(DOWN*0.10),coin.animate.shift(UP*0.20),run_time=0.9)

        # Right orbit
        e = self.earth(RIGHT*3.75+DOWN*0.35,1.65)
        orbit = Circle(radius=2.42,stroke_color=LIGHT,stroke_width=2).move_to(RIGHT*3.75+DOWN*0.35)
        sat = RoundedRectangle(width=0.62,height=0.36,corner_radius=0.06,
                               stroke_color=PURPLE,stroke_width=2.5,fill_color=WHITE,fill_opacity=1).move_to(RIGHT*3.75+UP*2.08)
        vg = self.vector(sat.get_center()+RIGHT*0.10,RIGHT*1.35,r"\vec v",BLUE,UP,24)
        gg = self.vector(sat.get_center()+LEFT*0.30,DOWN*1.18,r"\vec g",ORANGE,LEFT,24)
        self.play(FadeIn(e),Create(orbit),FadeIn(sat),FadeIn(vg),FadeIn(gg))

        orbitnote = self.card(
            "ÓRBITA A 400 km",
            [f"g ≈ {G_ORB:.2f} m/s²",f"≈ {100*G_ORB/G:.1f}% de g superficial","Órbita = caída libre continua"],
            5.2,2.25,fill=PBLUE,accent=BLUE,
            title_size=24,body_size=22,
        ).move_to(RIGHT*3.75+DOWN*2.35)
        self.play(FadeIn(orbitnote))

        nuance = self.txt(
            "Matiz senior: la equivalencia es local; a gran escala quedan gradientes gravitatorios (marea).",
            21,BOLD,MID
        )
        self.fit(nuance,14.2,0.55)
        nuance.to_edge(DOWN,buff=0.10)
        self.play(FadeIn(nuance))
        self.wait(2.8)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Chapter 5
    # ------------------------------------------------------------------
    def chapter_motion_and_graphs(self):
        self.section(
            5,
            "CAÍDA DESDE 20 m: MOVIMIENTO Y GRÁFICAS A LA VEZ",
            "El mismo tiempo t fija simultáneamente posición, velocidad y aceleración.",
        )

        tracker = ValueTracker(0.0)
        tmax = T_HIT

        # Big physical lane
        x = -5.85
        ytop, yground = 1.90, -2.20
        lane = Line([x,yground,0],[x,ytop,0],color=LIGHT,stroke_width=4)
        ground = Line([x-0.8,yground,0],[x+0.8,yground,0],color=INK,stroke_width=3)
        self.play(Create(lane),Create(ground))

        labels = VGroup()
        for h in [0,5,10,15,20]:
            yy = yground + (h/H)*(ytop-yground)
            tick = Line([x-0.18,yy,0],[x+0.18,yy,0],color=MID,stroke_width=1.5)
            lab = self.txt(f"{h} m",17,color=MID).next_to(tick,LEFT,buff=0.08)
            labels.add(tick,lab)
        self.play(FadeIn(labels))

        moving = always_redraw(lambda: self.ball(
            np.array([
                x,
                yground + (max(0.0,H-0.5*G*min(tracker.get_value(),tmax)**2)/H)*(ytop-yground),
                0
            ]),0.23,BLUE
        ))
        v_arrow = always_redraw(lambda: Arrow(
            [x+0.55,moving.get_center()[1]+0.05,0],
            [x+0.55,moving.get_center()[1]+0.05-min(1.60,0.078*G*tracker.get_value()),0],
            buff=0,color=BLUE,stroke_width=5,max_tip_length_to_length_ratio=0.18
        ))
        self.add(moving,v_arrow)

        # Graphs, arranged as a strong 2x2 dashboard
        ax_y = Axes(
            x_range=[0,tmax,0.5],y_range=[0,20,5],x_length=4.2,y_length=2.25,
            axis_config={"color":INK,"stroke_width":1.7,"include_tip":False}
        ).move_to(LEFT*1.10+UP*0.55)
        ax_v = Axes(
            x_range=[0,tmax,0.5],y_range=[-20,0,5],x_length=4.2,y_length=2.25,
            axis_config={"color":INK,"stroke_width":1.7,"include_tip":False}
        ).move_to(RIGHT*3.55+UP*0.55)
        ax_a = Axes(
            x_range=[0,tmax,0.5],y_range=[-12,0,3],x_length=4.2,y_length=2.25,
            axis_config={"color":INK,"stroke_width":1.7,"include_tip":False}
        ).move_to(LEFT*1.10+DOWN*2.05)

        cy = ax_y.plot(lambda t:H-0.5*G*t*t,x_range=[0,tmax],color=PURPLE,stroke_width=3.5)
        cv = ax_v.plot(lambda t:-G*t,x_range=[0,tmax],color=BLUE,stroke_width=3.5)
        ca = ax_a.plot(lambda t:-G,x_range=[0,tmax],color=ORANGE,stroke_width=3.5)

        ly = self.txt("y(t)",22,BOLD,PURPLE).next_to(ax_y,UP,buff=0.08)
        lv = self.txt("v(t)",22,BOLD,BLUE).next_to(ax_v,UP,buff=0.08)
        la = self.txt("a(t)",22,BOLD,ORANGE).next_to(ax_a,UP,buff=0.08)
        self.play(FadeIn(ax_y),FadeIn(ax_v),FadeIn(ax_a),FadeIn(ly),FadeIn(lv),FadeIn(la))
        self.play(Create(cy),Create(cv),Create(ca),run_time=1.1)

        dy = always_redraw(lambda: Dot(ax_y.c2p(
            min(tracker.get_value(),tmax),
            max(0.0,H-0.5*G*min(tracker.get_value(),tmax)**2)
        ),radius=0.075,color=PURPLE))
        dv = always_redraw(lambda: Dot(ax_v.c2p(
            min(tracker.get_value(),tmax),
            -G*min(tracker.get_value(),tmax)
        ),radius=0.075,color=BLUE))
        da = always_redraw(lambda: Dot(ax_a.c2p(
            min(tracker.get_value(),tmax),-G
        ),radius=0.075,color=ORANGE))
        self.add(dy,dv,da)

        tnum = DecimalNumber(0,num_decimal_places=2,font_size=34,color=INK)
        tnum.add_updater(lambda d:d.set_value(tracker.get_value()))
        speednum = DecimalNumber(0,num_decimal_places=1,font_size=34,color=BLUE)
        speednum.add_updater(lambda d:d.set_value(G*tracker.get_value()))
        read_box = RoundedRectangle(
            width=4.45,height=1.90,corner_radius=0.16,
            stroke_color=LIGHT,stroke_width=1.6,
            fill_color=WHITE,fill_opacity=1,
        ).move_to(RIGHT*3.55+DOWN*2.12)
        read_bar = Rectangle(
            width=0.10,height=1.70,stroke_width=0,
            fill_color=INK,fill_opacity=1,
        ).next_to(read_box.get_left(),RIGHT,buff=0.07)
        read_title = self.txt("LECTURA EN VIVO",21,BOLD,INK)
        read_title.next_to(read_box.get_top(),DOWN,buff=0.18)
        read_title.align_to(read_box,LEFT).shift(RIGHT*0.42)
        trow = VGroup(self.txt("t =",23,BOLD,INK),tnum,self.txt("s",23,color=INK)).arrange(RIGHT,buff=0.08)
        vrow = VGroup(self.txt("|v| =",23,BOLD,BLUE),speednum,self.txt("m/s",23,color=BLUE)).arrange(RIGHT,buff=0.08)
        rgroup = VGroup(trow,vrow).arrange(DOWN,aligned_edge=LEFT,buff=0.13)
        rgroup.next_to(read_title,DOWN,buff=0.18).align_to(read_title,LEFT)
        readout = VGroup(read_box,read_bar,read_title,rgroup)
        self.play(FadeIn(readout))

        self.play(tracker.animate.set_value(tmax),run_time=4.8,rate_func=linear)
        tnum.clear_updaters(); speednum.clear_updaters()

        result = self.formula(
            r"t_{\rm hit}\approx 2.02\,s\qquad |v_{\rm hit}|\approx 19.81\,m/s",
            9.0,1.05,34,PGREEN
        ).to_edge(DOWN,buff=0.08)
        self.play(FadeIn(result))
        self.wait(2.5)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Chapter 6
    # ------------------------------------------------------------------
    def chapter_drag(self):
        self.section(
            6,
            "CON AIRE, YA NO ES CAÍDA LIBRE IDEAL",
            "El arrastre crece con la rapidez; la fuerza neta disminuye y puede aparecer una velocidad terminal.",
        )

        obj = self.ball(LEFT*4.40+UP*0.80,0.40,BLUE)
        w = self.vector(LEFT*3.55+UP*0.90,DOWN*2.0,r"W=mg",RED)
        d = self.vector(LEFT*5.25+UP*0.10,UP*0.60,r"D",CYAN,LEFT)
        self.play(FadeIn(obj),FadeIn(w),FadeIn(d))

        trail = VGroup(*[
            Line(LEFT*6.4+DOWN*1.5+UP*i*0.45,LEFT*2.2+DOWN*1.5+UP*i*0.45,color=LIGHT,stroke_width=2)
            for i in range(8)
        ])
        self.play(FadeIn(trail))

        state1 = self.card("AL PRINCIPIO",["D pequeña","F_net ≈ mg","a ≈ g"],4.4,2.25,fill=PBLUE,accent=BLUE).move_to(RIGHT*1.00+UP*0.40)
        state2 = self.card("MÁS RÁPIDO",["D aumenta","F_net disminuye","|a| disminuye"],4.4,2.25,fill=PORANGE,accent=ORANGE).move_to(RIGHT*5.40+UP*0.40)
        state3 = self.card("VELOCIDAD TERMINAL",["D ≈ mg","F_net ≈ 0","a ≈ 0"],5.0,2.20,fill=PGREEN,accent=GREEN).move_to(RIGHT*3.25+DOWN*2.00)
        self.play(FadeIn(state1))

        d2 = self.vector(LEFT*5.25+DOWN*0.05,UP*1.25,r"D",CYAN,LEFT)
        self.play(Transform(d,d2),obj.animate.shift(DOWN*0.55),FadeIn(state2),run_time=0.85)

        d3 = self.vector(LEFT*5.25+DOWN*0.75,UP*1.95,r"D\approx mg",CYAN,LEFT)
        self.play(Transform(d,d3),obj.animate.shift(DOWN*0.75),FadeIn(state3),run_time=0.85)

        eq = self.formula(r"mg-D=ma\qquad D\rightarrow mg\Rightarrow a\rightarrow 0",8.0,1.05,35,PORANGE)
        eq.to_edge(DOWN,buff=0.10).shift(LEFT*2.0)
        self.play(FadeIn(eq))
        self.wait(2.5)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Chapter 7
    # ------------------------------------------------------------------
    def chapter_qa(self):
        self.section(
            7,
            "SENIOR QA: CINCO ERRORES QUE YA NO DEBEN APARECER",
            "Cada afirmación se decide con fuerzas, signos y definiciones, no con intuiciones vagas.",
        )

        items = [
            ("En la cima: a = 0", "FALSO", "v = 0 solo un instante; a = −g."),
            ("Ingravidez: g = 0", "FALSO", "N ≈ 0, pero W = mg sigue actuando."),
            ("Más masa: mayor a en vacío", "FALSO", "mg = ma ⇒ a = g."),
            ("La báscula siempre mide mg", "FALSO", "Mide N, que depende de la aceleración."),
            ("Con aire, a siempre vale g", "FALSO", "El arrastre D modifica la fuerza neta."),
        ]

        current = None
        for i,(claim,verdict,why) in enumerate(items,1):
            badge = RoundedRectangle(width=0.80,height=0.80,corner_radius=0.16,fill_color=INK,fill_opacity=1,stroke_width=0)
            badge_n = self.txt(str(i),26,BOLD,WHITE).move_to(badge)
            claim_t = self.txt(claim,36,BOLD,INK)
            self.fit(claim_t,10.8,0.80)
            verdict_t = self.txt(verdict,34,BOLD,RED)
            why_t = self.txt(why,27,color=MID)
            self.fit(why_t,11.5,0.65)

            group = VGroup(
                VGroup(badge,badge_n),
                claim_t,
                verdict_t,
                why_t,
            ).arrange(DOWN,buff=0.35)
            self.fit(group,12.8,4.8)
            group.move_to(ORIGIN+DOWN*0.20)

            panel = RoundedRectangle(
                width=13.2,height=4.9,corner_radius=0.20,
                stroke_color=LIGHT,stroke_width=1.7,
                fill_color=WHITE,fill_opacity=1
            ).move_to(group)
            full = VGroup(panel,group)

            if current is None:
                self.play(FadeIn(full,shift=UP*0.15),run_time=0.55)
            else:
                self.play(FadeOut(current,shift=LEFT*0.25),FadeIn(full,shift=RIGHT*0.25),run_time=0.55)
            current = full
            self.wait(1.25)

        takeaway = self.formula(
            r"\boxed{W=mg\neq 0\quad\text{puede coexistir con}\quad N=0}",
            9.0,1.15,36,PPURPLE
        ).to_edge(DOWN,buff=0.15)
        self.play(FadeIn(takeaway))
        self.wait(2.8)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Closing
    # ------------------------------------------------------------------
    def closing(self):
        title = self.txt("LA IDEA QUE DEBE QUEDAR",40,BOLD,INK)
        main = self.txt(
            "INGRAVIDEZ APARENTE ≠ AUSENCIA DE GRAVEDAD",
            38,BOLD,PURPLE
        )
        sub = self.txt(
            "Es ausencia de apoyo sostenido: N → 0 mientras la gravedad sigue acelerando el sistema.",
            27,BOLD,INK
        )
        self.fit(sub,13.7,0.75)

        route = VGroup(
            self.card("1 · FUERZAS",["Identifica W, N, D, T..."],2.6,1.45,fill=PRED,accent=RED,title_size=21,body_size=18),
            self.card("2 · NEWTON",["ΣF = ma"],2.6,1.45,fill=PORANGE,accent=ORANGE,title_size=21,body_size=18),
            self.card("3 · MOVIMIENTO",["a → v(t) → y(t)"],2.6,1.45,fill=PBLUE,accent=BLUE,title_size=21,body_size=18),
            self.card("4 · INTERPRETA",["Peso real vs aparente"],2.6,1.45,fill=PPURPLE,accent=PURPLE,title_size=21,body_size=18),
        ).arrange(RIGHT,buff=0.24)

        group = VGroup(title,main,sub,route).arrange(DOWN,buff=0.45)
        self.fit(group,14.3,6.5)
        self.play(FadeIn(title,shift=UP*0.15))
        self.play(FadeIn(main,scale=1.05))
        self.play(FadeIn(sub))
        self.play(LaggedStart(*[FadeIn(c,shift=UP*0.10) for c in route],lag_ratio=0.15),run_time=1.5)
        self.wait(4.0)
        self.clear_stage()
