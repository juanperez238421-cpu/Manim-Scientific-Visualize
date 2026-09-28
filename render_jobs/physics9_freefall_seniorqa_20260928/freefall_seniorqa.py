#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Caída libre, peso e ingravidez
Senior QA classroom animation
ManimCE 0.20.x | 1920x1080 | 30 fps

Physical model:
- +y upward.
- Near Earth's surface, g = 9.81 m/s^2 downward.
- Ideal free fall means gravity is the only relevant force after release.
- Weight W = mg never disappears in ordinary free fall.
- Apparent weight is the support/normal force N; in free fall N = 0.
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
config.background_color = WHITE

G = 9.81
H = 20.0
T_HIT = math.sqrt(2 * H / G)
V_HIT = G * T_HIT
M = 60.0
W = M * G
A_E = 3.0
N_DOWN = M * (G - A_E)
N_UP = M * (G + A_E)
R_E = 6371.0
H_ORBIT = 400.0
G_ORBIT = G * (R_E / (R_E + H_ORBIT)) ** 2
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BLACK2 = "#222222"
MID = "#666666"
LIGHT = "#D9D9D9"
PALE = "#F4F4F4"


def verify_data():
    assert abs(0.5 * G * T_HIT**2 - H) < 1e-10
    assert abs(V_HIT - math.sqrt(2 * G * H)) < 1e-10
    assert abs(W - 588.6) < 1e-9
    assert abs(N_DOWN - 408.6) < 1e-9
    assert abs(N_UP - 768.6) < 1e-9
    assert 0.88 < G_ORBIT / G < 0.89


class Physics9FreeFallSeniorQA(Scene):
    def setup(self):
        verify_data()
        self.camera.background_color = WHITE

    def play(self, *animations, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1.0) * TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ---------- layout ----------
    def t(self, s, size=30, weight=NORMAL, color=BLACK2):
        return Text(s, font_size=size, weight=weight, color=color, line_spacing=0.9)

    def m(self, s, size=38, color=BLACK2):
        return MathTex(s, font_size=size, color=color)

    def fit(self, mob, w=14.5, h=7.2):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def header(self, n, title, subtitle):
        badge = Circle(radius=0.28, stroke_color=BLACK2, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        num = self.t(str(n), 22, BOLD).move_to(badge)
        title_m = self.t(title, 31, BOLD)
        left = VGroup(badge, num, title_m).arrange(RIGHT, buff=0.18)
        sub = self.t(subtitle, 21, color=MID)
        self.fit(sub, 14.4, 0.55)
        g = VGroup(left, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        g.to_edge(UP, buff=0.27).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT*7.5, RIGHT*7.5, color=LIGHT, stroke_width=1.6).next_to(g, DOWN, buff=0.12)
        self.add(g, rule)
        return VGroup(g, rule)

    def clear(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(x) for x in mobs], run_time=0.45)

    def panel(self, title, lines, width=6.4, height=None):
        tt = self.t(title, 25, BOLD)
        body = VGroup(*[self.t(x, 21) for x in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(tt, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width-0.55, 4.6)
        hh = height if height else max(1.25, content.height + 0.55)
        box = RoundedRectangle(width=width, height=hh, corner_radius=0.12, stroke_color=BLACK2,
                               stroke_width=1.7, fill_color=WHITE, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.28)
        return VGroup(box, content)

    def formula_box(self, expr, width=6.0, size=42):
        box = RoundedRectangle(width=width, height=1.08, corner_radius=0.10, stroke_color=BLACK2,
                               stroke_width=1.8, fill_color=PALE, fill_opacity=1)
        eq = self.m(expr, size)
        self.fit(eq, width-0.45, 0.80)
        eq.move_to(box)
        return VGroup(box, eq)

    def block(self, p, label="m", side=0.62):
        sq = RoundedRectangle(width=side, height=side, corner_radius=0.07,
                              stroke_color=BLACK2, stroke_width=2,
                              fill_color=WHITE, fill_opacity=1).move_to(p)
        lab = self.t(label, 20, BOLD).move_to(sq)
        return VGroup(sq, lab)

    def force_arrow(self, start, vec, label, label_side=RIGHT):
        a = Arrow(start, start+vec, buff=0, color=BLACK2, stroke_width=4,
                  max_tip_length_to_length_ratio=0.18)
        l = self.m(label, 26).next_to(a, label_side, buff=0.10)
        return VGroup(a, l)

    def person(self, c):
        head = Circle(radius=0.16, color=BLACK2, stroke_width=2).move_to(c+UP*0.62)
        body = Line(c+UP*0.45, c+DOWN*0.25, color=BLACK2, stroke_width=3)
        arms = VGroup(
            Line(c+UP*0.20, c+LEFT*0.30, color=BLACK2, stroke_width=2.4),
            Line(c+UP*0.20, c+RIGHT*0.30, color=BLACK2, stroke_width=2.4),
        )
        legs = VGroup(
            Line(c+DOWN*0.25, c+LEFT*0.23+DOWN*0.72, color=BLACK2, stroke_width=2.4),
            Line(c+DOWN*0.25, c+RIGHT*0.23+DOWN*0.72, color=BLACK2, stroke_width=2.4),
        )
        return VGroup(head, body, arms, legs)

    # ---------- lesson ----------
    def construct(self):
        self.opening()
        self.scene1_definition()
        self.scene2_upward_throw()
        self.scene3_mass_independence()
        self.scene4_weight_vs_apparent()
        self.scene5_elevator()
        self.scene6_equations()
        self.scene7_worked_fall()
        self.scene8_graphs()
        self.scene9_air_and_orbit()
        self.scene10_qa()
        self.closing()

    def opening(self):
        course = self.t("FÍSICA 9° · MOVIMIENTO Y FUERZAS", 27, BOLD)
        title = self.t("CAÍDA LIBRE, PESO E INGRAVIDEZ", 50, BOLD)
        line = Line(LEFT*5.8, RIGHT*5.8, color=BLACK2, stroke_width=2)
        sub = self.t("La clave no es hacia dónde se mueve el objeto, sino qué fuerzas actúan.", 27)
        promise = self.t("Fenómeno → fuerzas → ecuaciones → gráficas → errores conceptuales", 24, BOLD)
        g = VGroup(course, title, line, sub, promise).arrange(DOWN, buff=0.28)
        self.fit(g, 14.0, 6.2)
        self.play(FadeIn(course, shift=UP*0.15))
        self.play(Write(title), run_time=1.2)
        self.play(Create(line), FadeIn(sub))
        self.wait(2.2)
        self.play(FadeIn(promise))
        self.wait(2.5)
        self.clear()

    def scene1_definition(self):
        self.header(1, "¿QUÉ ES CAÍDA LIBRE?",
                    "Después de liberar el objeto, la gravedad es la única fuerza relevante. La dirección de la velocidad no define la caída libre.")

        ground = Line(LEFT*5.8+DOWN*2.55, LEFT*0.6+DOWN*2.55, color=BLACK2, stroke_width=2)
        b = self.block(LEFT*3.3+UP*1.0, "m", 0.72)
        w = self.force_arrow(b.get_center()+RIGHT*0.52, DOWN*1.55, r"\vec W=m\vec g")
        grav = self.force_arrow(LEFT*1.2+UP*1.2, DOWN*1.55, r"\vec a=\vec g")
        visual = VGroup(ground, b, w, grav)

        note = self.panel("CONDICIÓN FÍSICA", [
            "No hay normal porque no existe soporte.",
            "No hay tensión si el objeto no está sujeto.",
            "En el modelo ideal ignoramos resistencia del aire.",
            "Por tanto: ΣF = W."
        ], 6.2).move_to(RIGHT*3.7+DOWN*0.30)

        self.play(Create(ground), FadeIn(b))
        self.play(GrowArrow(w[0]), FadeIn(w[1]))
        self.wait(1.4)
        self.play(GrowArrow(grav[0]), FadeIn(grav[1]), FadeIn(note))
        self.wait(3.0)

        eq = self.formula_box(r"\sum \vec F=m\vec a=m\vec g\;\Rightarrow\;\vec a=\vec g", 7.7, 38)
        eq.move_to(DOWN*2.45+RIGHT*2.5)
        self.play(FadeIn(eq))
        self.wait(2.6)
        self.clear()

    def scene2_upward_throw(self):
        self.header(2, "SUBIR TAMBIÉN PUEDE SER CAÍDA LIBRE",
                    "Una pelota lanzada hacia arriba sigue bajo la acción exclusiva de la gravedad después de abandonar la mano.")

        x = -3.7
        path = DashedLine(np.array([x,-2.3,0]), np.array([x,2.4,0]), color=LIGHT, dash_length=0.12)
        ball0 = Circle(radius=0.22, color=BLACK2, fill_color=WHITE, fill_opacity=1).move_to([x,-1.8,0])
        stages = VGroup(
            self.t("SUBE", 21, BOLD).move_to([x+1.05,-1.25,0]),
            self.t("PUNTO MÁS ALTO", 21, BOLD).move_to([x+1.55,1.80,0]),
            self.t("BAJA", 21, BOLD).move_to([x+1.0,0.35,0]),
        )
        self.play(Create(path), FadeIn(ball0), FadeIn(stages))

        up_v = self.force_arrow(ball0.get_center()+LEFT*0.45, UP*1.25, r"\vec v")
        a0 = self.force_arrow(ball0.get_center()+RIGHT*0.45, DOWN*1.05, r"\vec a=\vec g")
        self.play(GrowArrow(up_v[0]), FadeIn(up_v[1]), GrowArrow(a0[0]), FadeIn(a0[1]))
        self.wait(1.8)

        top_ball = ball0.copy().move_to([x,1.35,0])
        self.play(Transform(ball0, top_ball), FadeOut(up_v), Transform(a0, self.force_arrow(np.array([x+0.45,1.35,0]), DOWN*1.05, r"\vec a=\vec g")))
        vzero = self.m(r"v=0\quad\text{solo en ese instante}", 30).move_to(LEFT*2.7+UP*2.55)
        self.play(FadeIn(vzero))
        self.wait(2.2)

        down_v = self.force_arrow(np.array([x-0.45,0.55,0]), DOWN*1.25, r"\vec v")
        self.play(ball0.animate.move_to([x,0.55,0]), FadeIn(down_v), a0.animate.shift(DOWN*0.80))
        self.wait(1.8)

        key = self.panel("ERROR CLÁSICO", [
            "En el punto más alto: v = 0.",
            "Pero la aceleración NO es cero.",
            "Mientras la gravedad actúe: a = −g."
        ], 6.5).move_to(RIGHT*3.7+DOWN*0.20)
        self.play(FadeIn(key))
        self.wait(3.0)
        self.clear()

    def scene3_mass_independence(self):
        self.header(3, "¿CAE MÁS RÁPIDO EL OBJETO MÁS PESADO?",
                    "En vacío, no. El peso aumenta con la masa, pero la inercia también aumenta en la misma proporción.")

        leftx, rightx = -3.6, 0.0
        topy, boty = 1.7, -2.0
        guide1 = DashedLine([leftx,topy,0],[leftx,boty,0],color=LIGHT)
        guide2 = DashedLine([rightx,topy,0],[rightx,boty,0],color=LIGHT)
        b1 = self.block(np.array([leftx,topy,0]), "1 kg", 0.72)
        b2 = self.block(np.array([rightx,topy,0]), "5 kg", 0.88)
        w1 = self.force_arrow(b1.get_center()+RIGHT*0.58, DOWN*0.95, r"W_1=m_1g")
        w2 = self.force_arrow(b2.get_center()+RIGHT*0.68, DOWN*1.45, r"W_2=m_2g")
        self.play(Create(guide1), Create(guide2), FadeIn(b1), FadeIn(b2))
        self.play(FadeIn(w1), FadeIn(w2))
        self.wait(1.4)

        cancel = self.formula_box(r"a=\frac{F}{m}=\frac{mg}{m}=g", 5.8, 42).move_to(RIGHT*4.5+UP*1.2)
        note = self.panel("MISMA ACELERACIÓN", [
            "Más masa → más peso.",
            "Pero también → más resistencia a acelerar (inercia).",
            "La masa se cancela en F = ma."
        ], 5.8).move_to(RIGHT*4.5+DOWN*1.1)
        self.play(FadeIn(cancel), FadeIn(note))
        self.play(b1.animate.move_to([leftx,boty,0]), b2.animate.move_to([rightx,boty,0]), run_time=2.4)
        simultaneous = self.t("LLEGAN JUNTOS EN EL MODELO IDEAL", 23, BOLD).move_to(LEFT*1.8+DOWN*2.65)
        self.play(FadeIn(simultaneous))
        self.wait(2.8)
        self.clear()

    def scene4_weight_vs_apparent(self):
        self.header(4, "PESO REAL ≠ PESO APARENTE",
                    "El peso es la fuerza gravitatoria W = mg. La báscula mide la fuerza normal N que el soporte ejerce sobre ti.")

        p = self.person(LEFT*3.6+DOWN*0.25)
        floor = Line(LEFT*5.4+DOWN*1.25, LEFT*1.8+DOWN*1.25, color=BLACK2, stroke_width=3)
        w = self.force_arrow(LEFT*3.0+UP*0.25, DOWN*1.35, r"W=mg")
        n = self.force_arrow(LEFT*4.2+DOWN*0.85, UP*1.35, r"N")
        self.play(FadeIn(p), Create(floor))
        self.play(FadeIn(w), FadeIn(n))

        eqs = VGroup(
            self.formula_box(r"W=mg", 5.4, 42),
            self.formula_box(r"N=\text{peso aparente}", 5.4, 38),
            self.formula_box(r"\sum F_y=N-mg=ma_y", 5.4, 37),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT*3.9+DOWN*0.15)
        self.play(FadeIn(eqs[0]))
        self.wait(1.1)
        self.play(FadeIn(eqs[1]))
        self.wait(1.1)
        self.play(FadeIn(eqs[2]))
        self.wait(2.5)

        note = self.t("Si a = 0, entonces N = mg. Solo en ese caso la lectura coincide con el peso.", 22, BOLD)
        self.fit(note, 13.5, 0.6)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note))
        self.wait(2.5)
        self.clear()

    def elevator_card(self, x, title, ay, nval, nfrac):
        box = RoundedRectangle(width=4.35, height=4.75, corner_radius=0.12,
                               stroke_color=BLACK2, stroke_width=1.7, fill_color=WHITE, fill_opacity=1).move_to([x,-0.25,0])
        tt = self.t(title, 23, BOLD).next_to(box.get_top(), DOWN, buff=0.18)
        acc = self.m(ay, 27).next_to(tt, DOWN, buff=0.10)
        floor_y = box.get_bottom()[1] + 0.78
        p = self.person(np.array([x,floor_y+0.85,0]))
        scale = RoundedRectangle(width=1.25, height=0.24, corner_radius=0.04,
                                 stroke_color=BLACK2, stroke_width=1.6, fill_color=PALE, fill_opacity=1).move_to([x,floor_y,0])
        wg = self.force_arrow(np.array([x+0.53,floor_y+1.15,0]), DOWN*0.92, r"W")
        pieces = [box,tt,acc,p,scale,wg]
        if nfrac > 0:
            ng = self.force_arrow(np.array([x-0.53,floor_y+0.50,0]), UP*(0.92*nfrac), r"N", LEFT)
            pieces.append(ng)
        else:
            nz = self.m(r"N=0", 27).move_to([x-0.75,floor_y+0.85,0])
            pieces.append(nz)
        read = VGroup(self.t("Báscula", 19, BOLD), self.m(nval, 25)).arrange(DOWN,buff=0.05).next_to(scale,DOWN,buff=0.12)
        pieces.append(read)
        return VGroup(*pieces)

    def scene5_elevator(self):
        self.header(5, "INGRAVIDEZ: LA GRAVEDAD SIGUE ACTUANDO",
                    "La sensación de ingravidez aparece cuando desaparece la fuerza de apoyo. En caída libre W ≠ 0, pero N = 0.")

        c1 = self.elevator_card(-4.6, "ACELERA HACIA ARRIBA", r"a_y=+3.0\,\mathrm{m/s^2}", rf"N={N_UP:.1f}\,\mathrm{{N}}", 1.25)
        c2 = self.elevator_card(0.0, "ACELERA HACIA ABAJO", r"a_y=-3.0\,\mathrm{m/s^2}", rf"N={N_DOWN:.1f}\,\mathrm{{N}}", 0.70)
        c3 = self.elevator_card(4.6, "CAÍDA LIBRE", r"a_y=-g", r"N=0", 0.0)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3))
        self.wait(2.5)

        formulas = VGroup(
            self.m(r"N=m(g+a_y)", 30),
            self.m(r"N=m(g-3)", 30),
            self.m(r"N=m(g-g)=0", 30),
        )
        for f, c in zip(formulas, [c1,c2,c3]):
            f.next_to(c, DOWN, buff=0.16)
        self.play(FadeIn(formulas))
        self.wait(2.5)

        bottom = self.t("“Peso cero” en una báscula significa N = 0; NO significa que la gravedad haya desaparecido.", 22, BOLD)
        self.fit(bottom, 14.2, 0.58)
        bottom.to_edge(DOWN,buff=0.20)
        self.play(FadeIn(bottom))
        self.wait(3.2)
        self.clear()

    def scene6_equations(self):
        self.header(6, "DEDUCCIÓN CINEMÁTICA CON SIGNO",
                    "Tomemos +y hacia arriba. Entonces, cerca de la superficie terrestre, la aceleración es constante: a_y = −g.")

        sign_axis = Arrow(LEFT*5.7+DOWN*1.7, LEFT*5.7+UP*2.0, buff=0, color=BLACK2, stroke_width=3)
        plus = self.t("+y", 23, BOLD).next_to(sign_axis, UP, buff=0.07)
        garr = self.force_arrow(LEFT*4.7+UP*1.25, DOWN*1.55, r"\vec g")
        self.play(GrowArrow(sign_axis), FadeIn(plus), FadeIn(garr))

        stack = VGroup(
            self.formula_box(r"a_y=-g", 6.5, 42),
            self.formula_box(r"v(t)=v_0-gt", 6.5, 42),
            self.formula_box(r"y(t)=y_0+v_0t-\frac12gt^2", 6.5, 38),
            self.formula_box(r"v^2=v_0^2-2g(y-y_0)", 6.5, 38),
        ).arrange(DOWN,buff=0.18).move_to(RIGHT*2.2+DOWN*0.15)
        for item in stack:
            self.play(FadeIn(item), run_time=0.55)
            self.wait(0.9)
        note = self.panel("INTERPRETACIÓN", [
            "a constante → v cambia linealmente con t.",
            "v lineal → y es una parábola en t.",
            "El signo de v puede cambiar; el signo de a no."
        ], 5.6).move_to(LEFT*3.0+DOWN*0.10)
        self.play(FadeIn(note))
        self.wait(3.0)
        self.clear()

    def scene7_worked_fall(self):
        self.header(7, "EJEMPLO: SOLTAR DESDE 20 m",
                    "Objeto soltado desde reposo: y₀ = 20 m, v₀ = 0. Calculamos tiempo de impacto y rapidez final.")

        tower_x = -4.7
        ground_y = -2.35
        top_y = 2.05
        wall = Line([tower_x-0.8,ground_y,0],[tower_x-0.8,top_y+0.3,0],color=BLACK2,stroke_width=4)
        ground = Line([tower_x-1.5,ground_y,0],[tower_x+1.2,ground_y,0],color=BLACK2,stroke_width=3)
        marks = VGroup()
        for val in [0,5,10,15,20]:
            y = ground_y + (val/20)*(top_y-ground_y)
            tick = Line([tower_x-0.95,y,0],[tower_x-0.65,y,0],color=BLACK2,stroke_width=1.5)
            lab = self.t(f"{val} m",18).next_to(tick,LEFT,buff=0.08)
            marks.add(tick,lab)
        ball = Dot([tower_x,top_y,0],radius=0.16,color=BLACK2)
        self.play(Create(wall),Create(ground),FadeIn(marks),FadeIn(ball))

        eq = VGroup(
            self.m(r"0=20-\frac12gt^2", 35),
            self.m(r"t=\sqrt{\frac{2(20)}{9.81}}\approx "+f"{T_HIT:.2f}"+r"\,\mathrm{s}", 34),
            self.m(r"|v|=gt\approx "+f"{V_HIT:.2f}"+r"\,\mathrm{m/s}", 34)
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.32).move_to(RIGHT*2.4+UP*0.7)
        self.play(FadeIn(eq[0]))
        self.play(FadeIn(eq[1]))
        self.wait(1.2)

        clock = DecimalNumber(0, num_decimal_places=2, font_size=34, color=BLACK2)
        speed = DecimalNumber(0, num_decimal_places=2, font_size=34, color=BLACK2)
        read = VGroup(
            VGroup(self.t("t =",22,BOLD),clock,self.t("s",22)).arrange(RIGHT,buff=0.08),
            VGroup(self.t("|v| =",22,BOLD),speed,self.t("m/s",22)).arrange(RIGHT,buff=0.08),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.12).move_to(RIGHT*3.0+DOWN*1.15)
        tracker = ValueTracker(0)
        clock.add_updater(lambda d: d.set_value(tracker.get_value()))
        speed.add_updater(lambda d: d.set_value(G*tracker.get_value()))
        ball.add_updater(lambda q: q.move_to([tower_x, top_y-(top_y-ground_y)*(tracker.get_value()/T_HIT)**2, 0]))
        self.play(FadeIn(read))
        self.play(tracker.animate.set_value(T_HIT), run_time=3.2, rate_func=linear)
        ball.clear_updaters(); clock.clear_updaters(); speed.clear_updaters()
        self.play(FadeIn(eq[2]))
        self.wait(2.7)
        self.clear()

    def scene8_graphs(self):
        self.header(8, "UNA MISMA CAÍDA, TRES GRÁFICAS",
                    "Posición, velocidad y aceleración cuentan la misma historia física con representaciones diferentes.")

        tmax = T_HIT
        ax1 = Axes(x_range=[0,tmax,1], y_range=[0,20,5], x_length=4.4, y_length=2.35,
                   axis_config={"color":BLACK2,"stroke_width":1.7,"include_tip":False})
        ax2 = Axes(x_range=[0,tmax,1], y_range=[-20,0,5], x_length=4.4, y_length=2.35,
                   axis_config={"color":BLACK2,"stroke_width":1.7,"include_tip":False})
        ax3 = Axes(x_range=[0,tmax,1], y_range=[-12,0,3], x_length=4.4, y_length=2.35,
                   axis_config={"color":BLACK2,"stroke_width":1.7,"include_tip":False})

        ax1.move_to(LEFT*4.8+DOWN*0.25)
        ax2.move_to(DOWN*0.25)
        ax3.move_to(RIGHT*4.8+DOWN*0.25)

        c1 = ax1.plot(lambda t: H-0.5*G*t*t, x_range=[0,tmax], color=BLACK2, stroke_width=3)
        c2 = ax2.plot(lambda t: -G*t, x_range=[0,tmax], color=BLACK2, stroke_width=3)
        c3 = ax3.plot(lambda t: -G, x_range=[0,tmax], color=BLACK2, stroke_width=3)

        titles = VGroup(
            self.t("POSICIÓN y(t)",22,BOLD).next_to(ax1,UP,buff=0.14),
            self.t("VELOCIDAD v(t)",22,BOLD).next_to(ax2,UP,buff=0.14),
            self.t("ACELERACIÓN a(t)",22,BOLD).next_to(ax3,UP,buff=0.14),
        )
        forms = VGroup(
            self.m(r"y=20-\frac12gt^2",25).next_to(ax1,DOWN,buff=0.12),
            self.m(r"v=-gt",25).next_to(ax2,DOWN,buff=0.12),
            self.m(r"a=-g",25).next_to(ax3,DOWN,buff=0.12),
        )
        self.play(FadeIn(ax1),FadeIn(ax2),FadeIn(ax3),FadeIn(titles))
        self.play(Create(c1),run_time=1.5)
        self.play(Create(c2),run_time=1.2)
        self.play(Create(c3),run_time=1.0)
        self.play(FadeIn(forms))
        self.wait(2.5)

        logic = self.t("Curvatura en y(t) ↔ pendiente cambiante en v(t) ↔ aceleración constante.", 22, BOLD)
        self.fit(logic, 14.2, 0.55)
        logic.to_edge(DOWN,buff=0.18)
        self.play(FadeIn(logic))
        self.wait(2.8)
        self.clear()

    def scene9_air_and_orbit(self):
        self.header(9, "DOS CASOS QUE EVITAN CONFUSIONES",
                    "La caída real en aire y la ingravidez orbital no son idénticas al modelo elemental, pero se entienden desde las mismas fuerzas.")

        air = self.panel("AIRE: APARECE OTRA FUERZA", [
            "Al caer, el arrastre apunta hacia arriba.",
            "F_net = mg − D.",
            "Si D crece hasta igualar mg, entonces a → 0.",
            "La rapidez deja de aumentar: velocidad terminal."
        ], 6.7).move_to(LEFT*3.7+DOWN*0.05)

        orbit = self.panel("ÓRBITA: NO ES “SIN GRAVEDAD”", [
            "A 400 km la gravedad sigue siendo intensa.",
            f"g ≈ {G_ORBIT:.2f} m/s² ≈ {100*G_ORBIT/G:.1f}% de g superficial.",
            "Astronauta y nave caen juntos alrededor de la Tierra.",
            "Sin soporte: N ≈ 0 → ingravidez aparente."
        ], 6.7).move_to(RIGHT*3.7+DOWN*0.05)

        self.play(FadeIn(air),FadeIn(orbit))
        self.wait(2.8)

        left_eq = self.formula_box(r"mg-D=ma",5.4,38).next_to(air,DOWN,buff=0.20)
        right_eq = self.formula_box(r"g(h)=g_0\left(\frac{R}{R+h}\right)^2",5.4,32).next_to(orbit,DOWN,buff=0.20)
        self.play(FadeIn(left_eq),FadeIn(right_eq))
        self.wait(3.0)
        self.clear()

    def scene10_qa(self):
        self.header(10, "SENIOR QA · ERRORES QUE NO DEBEN SOBREVIVIR",
                    "Comprobación conceptual final: cada afirmación se decide con fuerzas, signos y definiciones.")

        cards = VGroup(
            self.panel("1 · “En la cima a = 0”", ["Incorrecto: v = 0 instantáneamente, pero a = −g."], 6.6, 1.25),
            self.panel("2 · “Ingravidez = no gravedad”", ["Incorrecto: en caída libre W = mg sigue actuando; N = 0."], 6.6, 1.25),
            self.panel("3 · “Más masa = más aceleración”", ["Incorrecto en vacío: a = mg/m = g."], 6.6, 1.25),
            self.panel("4 · “La báscula mide mg siempre”", ["Incorrecto: mide N, que depende de la aceleración del soporte."], 6.6, 1.25),
            self.panel("5 · “Toda caída es caída libre”", ["Incorrecto: con arrastre apreciable existe una fuerza adicional."], 6.6, 1.25),
            self.panel("6 · “Si v < 0 entonces a < 0 por definición”", ["Incorrecto: velocidad y aceleración son magnitudes independientes."], 6.6, 1.25),
        ).arrange_in_grid(rows=3,cols=2,buff=(0.35,0.26)).move_to(DOWN*0.25)
        self.fit(cards,14.3,5.9)

        for c in cards:
            self.play(FadeIn(c,shift=UP*0.08),run_time=0.35)
            self.wait(0.35)
        self.wait(3.4)
        self.clear()

    def closing(self):
        title = self.t("MAPA FINAL", 35, BOLD)
        steps = VGroup(
            self.panel("1", ["Identifica las fuerzas reales."], 2.45, 1.0),
            self.panel("2", ["Elige un eje y fija signos."], 2.45, 1.0),
            self.panel("3", ["Usa ΣF = ma para hallar a."], 2.45, 1.0),
            self.panel("4", ["Integra a → v → y."], 2.45, 1.0),
            self.panel("5", ["Interpreta gráficas y lectura N."], 2.45, 1.0),
        ).arrange(RIGHT,buff=0.22)
        final = self.t("Caída libre: la gravedad no desaparece. Lo que desaparece en ingravidez es el apoyo.", 29, BOLD)
        self.fit(final,13.8,0.85)
        g = VGroup(title,steps,final).arrange(DOWN,buff=0.50)
        self.fit(g,14.5,6.0)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(s,shift=UP*0.08) for s in steps],lag_ratio=0.18),run_time=1.8)
        self.wait(2.0)
        self.play(FadeIn(final))
        self.wait(4.0)
        self.clear()
