#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physics 9 — Movimiento vertical y caída libre
V2 MOTION-FIRST / CINEMATIC THEORY
ManimCE 0.20.x | 1920x1080 | 30 fps

Design goal
-----------
Replace slide-like panels with continuous physics-driven animation:
- moving objects remain synchronized with equations and graphs;
- vector arrows update continuously;
- camera motion is used to direct attention;
- derivations are built by transformation, not by replacing static slides;
- equal-time stroboscopic positions make d ∝ t² visible before the formula appears;
- the laboratory prediction is generated from motion, then linearized as d vs t².

Physics convention
------------------
+y upward, near Earth's surface, g = 9.81 m/s² downward.
Ideal free fall means gravity is the only relevant force after release.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass

import numpy as np
from manim import *


# =============================================================================
# RENDER
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#07111F"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))


# =============================================================================
# PHYSICS
# =============================================================================
G = 9.81

# Upward throw
V0 = 14.0
T_APEX = V0 / G
H_APEX = V0**2 / (2 * G)
T_RETURN = 2 * T_APEX

# Drop
H_DROP = 20.0
T_DROP = math.sqrt(2 * H_DROP / G)
V_IMPACT = G * T_DROP

# Lab prediction samples
LAB_TIMES = np.array([0.20, 0.40, 0.60, 0.80], dtype=float)
LAB_D = 0.5 * G * LAB_TIMES**2


def verify_physics() -> None:
    assert abs(V0 - G * T_APEX) < 1e-12
    assert abs(H_APEX - (V0 * T_APEX - 0.5 * G * T_APEX**2)) < 1e-12
    assert abs(T_RETURN - 2 * T_APEX) < 1e-12
    assert abs(0.5 * G * T_DROP**2 - H_DROP) < 1e-12
    assert abs(V_IMPACT - math.sqrt(2 * G * H_DROP)) < 1e-12
    ratios = LAB_D / LAB_D[0]
    assert np.allclose(ratios, [1, 4, 9, 16])


# =============================================================================
# VISUAL LANGUAGE
# =============================================================================
BG = "#07111F"
PANEL = "#0E1C2F"
PANEL_2 = "#13253A"
WHITE2 = "#F7FAFC"
MUTED = "#A8B3C7"
GRID = "#1C2E43"
CYAN = "#35D0FF"
YELLOW = "#FFD166"
RED = "#FF5D73"
GREEN = "#52E0A0"
PURPLE = "#B892FF"
ORANGE = "#FF9E5E"

SAFE_LEFT = -7.35
SAFE_RIGHT = 7.35
SAFE_TOP = 4.0
SAFE_BOTTOM = -4.0


@dataclass
class State:
    t: float
    y: float
    v: float
    a: float


class Physics9VerticalFreeFallTheoryV2(MovingCameraScene):
    """Motion-first full theory lesson for the vertical-motion/free-fall lab."""

    def setup(self):
        verify_physics()
        self.camera.background_color = BG

    # ------------------------------------------------------------------
    # timing
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1.0) * TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # text / boxes
    # ------------------------------------------------------------------
    def tx(self, text, size=30, color=WHITE2, weight=NORMAL):
        return Text(text, font_size=size, color=color, weight=weight)

    def mt(self, tex, size=40, color=WHITE2):
        return MathTex(tex, font_size=size, color=color)

    def fit(self, mob, w=14.3, h=7.3):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def safe(self, mob, label="object"):
        if (
            mob.get_left()[0] < SAFE_LEFT
            or mob.get_right()[0] > SAFE_RIGHT
            or mob.get_top()[1] > SAFE_TOP
            or mob.get_bottom()[1] < SAFE_BOTTOM
        ):
            raise ValueError(f"{label} outside safe frame")
        return mob

    def header(self, n, title, subtitle=None):
        badge = Circle(0.25, stroke_color=CYAN, stroke_width=2.2)
        badge.set_fill(PANEL, 1)
        num = self.tx(str(n), 20, CYAN, BOLD).move_to(badge)
        title_m = self.tx(title, 31, WHITE2, BOLD)
        row = VGroup(badge, num, title_m).arrange(RIGHT, buff=0.16)
        row.to_edge(UP, buff=0.22).to_edge(LEFT, buff=0.42)
        self.add(row)
        if subtitle:
            sub = self.tx(subtitle, 19, MUTED)
            self.fit(sub, 13.9, 0.45)
            sub.next_to(row, DOWN, aligned_edge=LEFT, buff=0.10)
            rule = Line([-7.25, sub.get_bottom()[1]-0.12, 0],
                        [7.25, sub.get_bottom()[1]-0.12, 0],
                        stroke_color=GRID, stroke_width=1.4)
            self.add(sub, rule)
            return VGroup(row, sub, rule)
        return row

    def pill(self, text, color=CYAN, size=23):
        t = self.tx(text, size, color, BOLD)
        box = RoundedRectangle(
            width=t.width + 0.48,
            height=t.height + 0.25,
            corner_radius=0.16,
            stroke_color=color,
            stroke_width=1.6,
            fill_color=PANEL,
            fill_opacity=1,
        )
        t.move_to(box)
        return VGroup(box, t)

    def glass_panel(self, w, h, stroke=GRID, fill=PANEL, opacity=0.94):
        return RoundedRectangle(
            width=w,
            height=h,
            corner_radius=0.18,
            stroke_color=stroke,
            stroke_width=1.5,
            fill_color=fill,
            fill_opacity=opacity,
        )

    def clear_stage(self, rt=0.45):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=rt)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    # ------------------------------------------------------------------
    # primitive physics graphics
    # ------------------------------------------------------------------
    def ball(self, p, r=0.19, color=CYAN):
        glow = Circle(r*1.9, stroke_width=0, fill_color=color, fill_opacity=0.10).move_to(p)
        core = Circle(r, stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.24).move_to(p)
        dot = Dot(p, radius=r*0.36, color=WHITE2)
        return VGroup(glow, core, dot)

    def vector(self, start, vec, label, color, side=RIGHT, size=24):
        a = Arrow(start, start + vec, buff=0, color=color, stroke_width=4.0,
                  max_tip_length_to_length_ratio=0.18)
        lab = self.mt(label, size, color).next_to(a, side, buff=0.08)
        return VGroup(a, lab)

    def vertical_ruler(self, x=-5.4, y0=-2.7, y1=2.5, meters=20):
        line = Line([x,y0,0], [x,y1,0], color=MUTED, stroke_width=2)
        marks = VGroup()
        for m in range(0, meters+1, 5):
            yy = y0 + (m/meters)*(y1-y0)
            tick = Line([x-0.12,yy,0],[x+0.12,yy,0], color=MUTED, stroke_width=1.5)
            lab = self.tx(f"{m} m", 17, MUTED).next_to(tick, LEFT, buff=0.08)
            marks.add(tick,lab)
        return VGroup(line,marks)

    def ground(self, y=-2.7, x0=-6.4, x1=6.4):
        base = Line([x0,y,0],[x1,y,0], color=MUTED, stroke_width=2.4)
        dashes = VGroup(*[
            Line([x,y-0.08,0],[x+0.28,y-0.28,0], color=GRID, stroke_width=1.4)
            for x in np.arange(x0, x1, 0.55)
        ])
        return VGroup(base,dashes)

    def live_readout(self, tracker, state_fn, title="LIVE STATE", x=4.75, y=0.4):
        def build():
            s = state_fn(tracker.get_value())
            p = self.glass_panel(4.0, 3.0, stroke=CYAN, fill=PANEL_2, opacity=0.97)
            ttl = self.tx(title, 21, CYAN, BOLD)
            vals = VGroup(
                self.tx(f"t = {s.t:0.2f} s", 26, WHITE2, BOLD),
                self.tx(f"y = {s.y:0.2f} m", 26, WHITE2),
                self.tx(f"v = {s.v:+0.2f} m/s", 26, YELLOW),
                self.tx(f"a = {s.a:+0.2f} m/s²", 26, RED),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            content = VGroup(ttl, vals).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            content.move_to(p).align_to(p, LEFT).shift(RIGHT*0.25)
            return VGroup(p, content).move_to([x,y,0])
        return always_redraw(build)

    # =========================================================================
    # MASTER
    # =========================================================================
    def construct(self):
        self.opening()
        self.s1_trajectory_vs_force_condition()
        self.s2_sign_convention_live()
        self.s3_newton_to_g()
        self.s4_integrate_to_kinematics()
        self.s5_three_vertical_cases()
        self.s6_apex_live_motion()
        self.s7_mass_independence()
        self.s8_synchronized_motion_and_graphs()
        self.s9_drop_20m_live()
        self.s10_strobe_square_law()
        self.s11_lab_linearization()
        self.s12_experimental_bridge()
        self.closing()

    # =========================================================================
    # OPENING — motion before text
    # =========================================================================
    def opening(self):
        title = self.tx("MOVIMIENTO VERTICAL", 54, WHITE2, BOLD).move_to([0,2.4,0])
        subtitle = self.tx("y CAÍDA LIBRE", 47, CYAN, BOLD).next_to(title, DOWN, buff=0.10)
        rule = Line([-5.6,1.28,0],[5.6,1.28,0], color=GRID, stroke_width=2)

        t = ValueTracker(0.0)
        y0 = -1.95
        h = 3.2
        moving = always_redraw(lambda:
            self.ball([0, y0 + h*(4*t.get_value()*(1-t.get_value())), 0], 0.20, CYAN)
        )
        velocity = always_redraw(lambda:
            self.vector(
                np.array([0.55, y0 + h*(4*t.get_value()*(1-t.get_value())), 0]),
                UP * (1.2*(1-2*t.get_value())),
                r"\vec v",
                YELLOW,
                RIGHT,
                23
            ) if abs(1-2*t.get_value()) > 0.08 else
            VGroup(self.mt(r"v=0", 25, YELLOW).move_to([0.95, y0+h, 0]))
        )
        gravity = always_redraw(lambda:
            self.vector(
                np.array([-0.55, y0 + h*(4*t.get_value()*(1-t.get_value())), 0]),
                DOWN*0.95,
                r"\vec g",
                RED,
                LEFT,
                23
            )
        )

        tagline = self.tx("ONE FORCE. THREE GRAPHS. ONE TESTABLE PREDICTION.", 22, MUTED, BOLD).move_to([0,-3.15,0])

        self.play(Write(title), FadeIn(subtitle), Create(rule), run_time=1.0)
        self.play(FadeIn(moving), FadeIn(velocity), FadeIn(gravity), run_time=0.45)
        self.play(t.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        self.play(FadeIn(tagline), run_time=0.4)
        self.wait(1.5)
        self.clear_stage()

    # =========================================================================
    # 1 — vertical trajectory != free-fall condition
    # =========================================================================
    def s1_trajectory_vs_force_condition(self):
        self.header(
            1,
            "TRAYECTORIA VERTICAL ≠ CONDICIÓN DE CAÍDA LIBRE",
            "La trayectoria dice dónde se mueve. La caída libre dice qué fuerzas actúan."
        )

        split = Line([0,-2.8,0],[0,2.25,0], color=GRID, stroke_width=1.4)

        # left: vertical elevator-like supported motion
        rail_l = Line([-4.2,-2.3,0],[-4.2,2.0,0], color=GRID, stroke_width=2)
        block_l = Square(0.68, stroke_color=WHITE2, fill_color=PANEL_2, fill_opacity=1).move_to([-4.2,-1.5,0])
        normal = self.vector(np.array([-4.65,-1.35,0]), UP*1.0, r"\vec N", GREEN, LEFT)
        weight_l = self.vector(np.array([-3.75,-1.15,0]), DOWN*1.0, r"m\vec g", RED, RIGHT)
        lab_l = self.pill("VERTICAL MOTION", PURPLE).move_to([-4.2,2.55,0])

        # right: true free fall
        rail_r = DashedLine([4.2,-2.3,0],[4.2,2.0,0], color=GRID, dash_length=0.10)
        block_r = self.ball([4.2,1.55,0],0.20,CYAN)
        weight_r = self.vector(np.array([4.75,1.45,0]), DOWN*1.15, r"m\vec g", RED, RIGHT)
        lab_r = self.pill("IDEAL FREE FALL", CYAN).move_to([4.2,2.55,0])

        self.play(Create(split), FadeIn(lab_l), FadeIn(lab_r), run_time=0.5)
        self.play(Create(rail_l), FadeIn(block_l), FadeIn(normal), FadeIn(weight_l), run_time=0.7)
        self.play(block_l.animate.shift(UP*2.3), run_time=1.5, rate_func=there_and_back)
        self.wait(0.5)

        self.play(Create(rail_r), FadeIn(block_r), FadeIn(weight_r), run_time=0.6)
        self.play(block_r.animate.move_to([4.2,-2.0,0]), weight_r.animate.shift(DOWN*3.55),
                  run_time=1.8, rate_func=rate_functions.ease_in_quad)
        self.wait(0.7)

        verdict = self.mt(
            r"\text{caída libre ideal}\Longleftrightarrow \sum \vec F=m\vec g",
            38,
            CYAN,
        ).to_edge(DOWN, buff=0.42)
        self.play(Write(verdict))
        self.wait(2.2)
        self.clear_stage()

    # =========================================================================
    # 2 — sign convention, with moving object
    # =========================================================================
    def s2_sign_convention_live(self):
        self.header(
            2,
            "EL SIGNO SE DEFINE ANTES DE CALCULAR",
            "Tomamos +y hacia arriba. Entonces la gravedad es siempre negativa: a_y = −g."
        )

        axis = Arrow([-5.2,-2.5,0],[-5.2,2.4,0],buff=0,color=WHITE2,stroke_width=3)
        zero = Dot([-5.2,-0.15,0], radius=0.065, color=CYAN)
        labels = VGroup(
            self.tx("+y",23,CYAN,BOLD).next_to(axis,UP,buff=0.05),
            self.tx("−y",23,RED,BOLD).next_to(axis,DOWN,buff=0.05),
            self.tx("0",19,MUTED).next_to(zero,LEFT,buff=0.10)
        )

        t = ValueTracker(0.0)
        y0=-1.8
        ypeak=1.75

        ball = always_redraw(lambda:
            self.ball([-1.6, y0 + (ypeak-y0)*(4*t.get_value()*(1-t.get_value())),0],0.19,CYAN)
        )

        def vel_vec():
            q=1-2*t.get_value()
            yy=y0+(ypeak-y0)*(4*t.get_value()*(1-t.get_value()))
            if abs(q)<0.06:
                return self.mt(r"v_y=0",26,YELLOW).move_to([-0.55,yy,0])
            return self.vector(np.array([-1.0,yy,0]), UP*(1.25*q), r"v_y", YELLOW, RIGHT)

        vel = always_redraw(vel_vec)
        acc = always_redraw(lambda:
            self.vector(
                np.array([-2.2, y0+(ypeak-y0)*(4*t.get_value()*(1-t.get_value())),0]),
                DOWN*1.0, r"a_y=-g", RED, LEFT
            )
        )

        state = always_redraw(lambda:
            self.pill(
                "UP: v>0" if t.get_value()<0.47 else
                "APEX: v=0" if t.get_value()<0.53 else
                "DOWN: v<0",
                YELLOW if abs(t.get_value()-0.5)>0.03 else CYAN,
                22
            ).move_to([4.0,1.55,0])
        )

        key = VGroup(
            self.mt(r"v_y>0",33,YELLOW),
            self.mt(r"v_y=0",33,YELLOW),
            self.mt(r"v_y<0",33,YELLOW),
        ).arrange(DOWN,buff=0.28).move_to([4.0,-0.10,0])

        constant = self.mt(r"a_y=-9.81\;\mathrm{m/s^2}\quad\text{en los tres casos}", 31, RED).move_to([3.4,-2.30,0])

        self.play(GrowArrow(axis), FadeIn(zero), FadeIn(labels), run_time=0.7)
        self.play(FadeIn(ball), FadeIn(vel), FadeIn(acc), FadeIn(state), run_time=0.5)
        self.play(t.animate.set_value(0.5), run_time=1.8, rate_func=linear)
        self.play(FadeIn(key[1]), FadeIn(constant), run_time=0.5)
        self.wait(1.0)
        self.play(t.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        self.play(FadeIn(key[0]), FadeIn(key[2]), run_time=0.5)
        self.wait(2.0)
        self.clear_stage()

    # =========================================================================
    # 3 — force diagram morphs into a=-g
    # =========================================================================
    def s3_newton_to_g(self):
        self.header(
            3,
            "DE LAS FUERZAS A LA ACELERACIÓN",
            "No empezamos con una fórmula de cinemática: empezamos con el diagrama de cuerpo libre."
        )

        b = self.ball([-4.4,0.55,0],0.28,CYAN)
        w = self.vector(np.array([-3.8,0.6,0]),DOWN*1.75,r"\vec W=m\vec g",RED,RIGHT,28)
        fbd = self.tx("FREE-BODY DIAGRAM",22,MUTED,BOLD).move_to([-4.15,2.25,0])

        self.play(FadeIn(fbd), FadeIn(b), run_time=0.4)
        self.play(GrowArrow(w[0]), FadeIn(w[1]), run_time=0.8)
        self.wait(0.8)

        e1 = self.mt(r"\sum F_y=ma_y",46,WHITE2).move_to([2.1,1.8,0])
        e2 = self.mt(r"-mg=ma_y",46,WHITE2).move_to([2.1,0.60,0])
        e3 = self.mt(r"a_y=\frac{-mg}{m}",46,WHITE2).move_to([2.1,-0.60,0])
        e4 = self.mt(r"a_y=-g",54,RED).move_to([2.1,-1.85,0])

        self.play(Write(e1))
        self.play(TransformMatchingTex(e1.copy(), e2), run_time=0.7)
        self.play(TransformMatchingTex(e2.copy(), e3), run_time=0.7)
        self.play(TransformMatchingTex(e3.copy(), e4), run_time=0.8)
        self.wait(1.2)

        mass_cancel = self.tx("mass cancels → same ideal acceleration",22,GREEN,BOLD).next_to(e4,DOWN,buff=0.30)
        self.play(FadeIn(mass_cancel))
        self.wait(2.2)
        self.clear_stage()

    # =========================================================================
    # 4 — integration as animated chain
    # =========================================================================
    def s4_integrate_to_kinematics(self):
        self.header(
            4,
            "UNA CADENA: ACELERACIÓN → VELOCIDAD → POSICIÓN",
            "Con a_y constante, integramos una vez para v(t) y otra vez para y(t)."
        )

        a = self.mt(r"a_y=-g",50,RED).move_to([-4.6,0.4,0])
        arrow1 = Arrow([-3.3,0.4,0],[-1.6,0.4,0],buff=0,color=MUTED,stroke_width=3)
        v = self.mt(r"v_y(t)=v_0-gt",48,YELLOW).move_to([0,0.4,0])
        arrow2 = Arrow([1.85,0.4,0],[3.35,0.4,0],buff=0,color=MUTED,stroke_width=3)
        y = self.mt(r"y(t)=y_0+v_0t-\frac12gt^2",42,CYAN).move_to([5.25,0.4,0])

        under_a = self.tx("constant",20,RED,BOLD).next_to(a,DOWN,buff=0.22)
        under_v = self.tx("linear in t",20,YELLOW,BOLD).next_to(v,DOWN,buff=0.22)
        under_y = self.tx("quadratic in t",20,CYAN,BOLD).next_to(y,DOWN,buff=0.22)

        self.play(Write(a), FadeIn(under_a))
        self.play(GrowArrow(arrow1), run_time=0.5)
        self.play(Write(v), FadeIn(under_v))
        self.play(GrowArrow(arrow2), run_time=0.5)
        self.play(Write(y), FadeIn(under_y))
        self.wait(1.6)

        deriv = VGroup(
            self.mt(r"\frac{dv_y}{dt}=-g",34,WHITE2),
            self.mt(r"dv_y=-g\,dt",34,WHITE2),
            self.mt(r"v_y-v_0=-gt",34,WHITE2),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).move_to([-3.5,-1.75,0])

        deriv2 = VGroup(
            self.mt(r"\frac{dy}{dt}=v_0-gt",34,WHITE2),
            self.mt(r"dy=(v_0-gt)\,dt",34,WHITE2),
            self.mt(r"y-y_0=v_0t-\frac12gt^2",34,WHITE2),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).move_to([3.25,-1.75,0])

        self.play(LaggedStart(*[FadeIn(m,shift=UP*0.06) for m in deriv],lag_ratio=0.25),run_time=1.1)
        self.play(LaggedStart(*[FadeIn(m,shift=UP*0.06) for m in deriv2],lag_ratio=0.25),run_time=1.1)
        self.wait(2.0)
        self.clear_stage()

    # =========================================================================
    # 5 — three initial conditions, all animated simultaneously
    # =========================================================================
    def s5_three_vertical_cases(self):
        self.header(
            5,
            "TRES CONDICIONES INICIALES, UNA MISMA GRAVEDAD",
            "Soltar, lanzar hacia arriba o lanzar hacia abajo solo cambia v₀."
        )

        xs=[-4.8,0,4.8]
        labels=["DROP","UPWARD LAUNCH","DOWNWARD LAUNCH"]
        colors=[GREEN,CYAN,ORANGE]
        t=ValueTracker(0.0)

        cards=VGroup()
        movers=VGroup()
        gravs=VGroup()
        equations=VGroup()

        for x,label,c in zip(xs,labels,colors):
            box=self.glass_panel(4.15,4.75,stroke=c,fill=PANEL,opacity=0.95).move_to([x,-0.25,0])
            ttl=self.tx(label,21,c,BOLD).next_to(box.get_top(),DOWN,buff=0.18)
            guide=DashedLine([x,-1.95,0],[x,1.55,0],dash_length=0.09,color=GRID)
            cards.add(VGroup(box,ttl,guide))

        drop=always_redraw(lambda:self.ball([-4.8,1.35-3.0*(t.get_value()**2),0],0.17,GREEN))
        up=always_redraw(lambda:self.ball([0,-1.15+3.5*(4*t.get_value()*(1-t.get_value())),0],0.17,CYAN))
        down=always_redraw(lambda:self.ball([4.8,1.35-3.0*(0.25*t.get_value()+0.75*t.get_value()**2),0],0.17,ORANGE))
        movers.add(drop,up,down)

        for x in xs:
            gravs.add(self.vector(np.array([x+0.58,0.75,0]),DOWN*0.90,r"\vec g",RED,RIGHT,20))

        eqs=[
            r"v_0=0",
            r"v_0>0",
            r"v_0<0",
        ]
        for x,e,c in zip(xs,eqs,colors):
            equations.add(
                VGroup(
                    self.mt(e,29,c),
                    self.mt(r"a_y=-g",27,RED),
                ).arrange(DOWN,buff=0.12).move_to([x,-2.10,0])
            )

        self.play(FadeIn(cards),FadeIn(movers),FadeIn(gravs),FadeIn(equations),run_time=0.8)
        self.play(t.animate.set_value(1.0),run_time=3.2,rate_func=linear)
        self.wait(1.2)

        same=self.mt(r"y=y_0+v_0t-\frac12gt^2",40,WHITE2).to_edge(DOWN,buff=0.18)
        self.play(Write(same))
        self.wait(2.1)
        self.clear_stage()

    # =========================================================================
    # 6 — actual upward throw state + camera focus at apex
    # =========================================================================
    def s6_apex_live_motion(self):
        self.header(
            6,
            "EL PUNTO MÁS ALTO NO APAGA LA GRAVEDAD",
            "La velocidad pasa por cero; la aceleración permanece −g."
        )

        ruler=self.vertical_ruler(x=-5.8,y0=-2.65,y1=2.35,meters=12)
        ground=self.ground(y=-2.65,x0=-6.4,x1=1.3)
        t=ValueTracker(0.0)

        def state(tt):
            return State(tt, V0*tt-0.5*G*tt**2, V0-G*tt, -G)

        def scene_y(tt):
            return -2.45 + 4.65*(state(tt).y/H_APEX)

        b=always_redraw(lambda:self.ball([-2.7,scene_y(t.get_value()),0],0.19,CYAN))
        vv=always_redraw(lambda:
            self.vector(
                np.array([-2.05,scene_y(t.get_value()),0]),
                UP*np.clip(state(t.get_value()).v/11.0,-1.35,1.35),
                r"\vec v",
                YELLOW,
                RIGHT,
                21
            ) if abs(state(t.get_value()).v)>0.6 else
            self.mt(r"v=0",26,YELLOW).move_to([-1.65,scene_y(t.get_value()),0])
        )
        aa=always_redraw(lambda:
            self.vector(np.array([-3.35,scene_y(t.get_value()),0]),DOWN*0.95,r"\vec a=-\vec g",RED,LEFT,21)
        )
        hud=self.live_readout(t,state,title="UPWARD THROW",x=4.45,y=0.45)

        self.play(FadeIn(ruler),FadeIn(ground),FadeIn(b),FadeIn(vv),FadeIn(aa),FadeIn(hud),run_time=0.7)

        self.play(t.animate.set_value(T_APEX),run_time=2.4,rate_func=linear)
        self.play(self.camera.frame.animate.set(width=11.8).move_to([-0.9,0.8,0]),run_time=0.7)
        apex_tag=self.pill("APEX: v = 0, a = −g",RED,24).move_to([0.55,2.70,0])
        self.play(FadeIn(apex_tag))
        self.wait(1.8)
        self.play(self.camera.frame.animate.set(width=16).move_to(ORIGIN),run_time=0.7)
        self.play(t.animate.set_value(T_RETURN),run_time=2.4,rate_func=linear)

        stats=VGroup(
            self.mt(r"t_{\max}=v_0/g\approx "+f"{T_APEX:.2f}"+r"\,s",29,CYAN),
            self.mt(r"\Delta y_{\max}=v_0^2/(2g)\approx "+f"{H_APEX:.2f}"+r"\,m",29,CYAN),
        ).arrange(DOWN,buff=0.14).move_to([3.9,-2.15,0])
        self.play(FadeIn(stats))
        self.wait(2.0)
        self.clear_stage()

    # =========================================================================
    # 7 — mass independence as synchronized drop
    # =========================================================================
    def s7_mass_independence(self):
        self.header(
            7,
            "¿EL MÁS PESADO CAE MÁS RÁPIDO?",
            "En el modelo ideal, no: la fuerza aumenta con m, pero a = F/m."
        )

        xs=[-3.0,3.0]
        masses=[1,5]
        t=ValueTracker(0.0)
        guides=VGroup(
            DashedLine([-3,-2.3,0],[-3,2.0,0],color=GRID,dash_length=0.08),
            DashedLine([3,-2.3,0],[3,2.0,0],color=GRID,dash_length=0.08)
        )
        b1=always_redraw(lambda:self.ball([-3,1.75-3.8*t.get_value()**2,0],0.18,GREEN))
        b2=always_redraw(lambda:self.ball([3,1.75-3.8*t.get_value()**2,0],0.23,ORANGE))

        w1=self.vector(np.array([-2.4,1.2,0]),DOWN*0.8,r"m_1g",RED,RIGHT,21)
        w2=self.vector(np.array([3.65,1.2,0]),DOWN*1.35,r"m_2g",RED,RIGHT,21)
        m1=self.pill("1 kg",GREEN,22).move_to([-3,2.45,0])
        m2=self.pill("5 kg",ORANGE,22).move_to([3,2.45,0])

        self.play(FadeIn(guides),FadeIn(b1),FadeIn(b2),FadeIn(w1),FadeIn(w2),FadeIn(m1),FadeIn(m2))
        self.play(t.animate.set_value(1.0),run_time=2.4,rate_func=rate_functions.ease_in_quad)

        cancel=self.mt(r"a=\frac{mg}{m}=g",48,CYAN).move_to([0,-2.75,0])
        together=self.tx("same acceleration → same fall time (vacuum model)",22,WHITE2,BOLD).next_to(cancel,UP,buff=0.22)
        self.play(Write(cancel),FadeIn(together))
        self.wait(2.3)
        self.clear_stage()

    # =========================================================================
    # 8 — moving ball + y/v/a graphs synchronized
    # =========================================================================
    def s8_synchronized_motion_and_graphs(self):
        self.header(
            8,
            "EL MOVIMIENTO Y LAS GRÁFICAS SON EL MISMO EVENTO",
            "Un único reloj mueve la pelota y recorre y(t), v(t) y a(t) simultáneamente."
        )

        t=ValueTracker(0.0)

        # Physical trajectory left
        traj=Line([-6.15,-2.30,0],[-6.15,2.10,0],color=GRID,stroke_width=2)
        b=always_redraw(lambda:
            self.ball([-6.15,-2.30+4.4*((V0*t.get_value()-0.5*G*t.get_value()**2)/H_APEX),0],0.14,CYAN)
        )

        # Three graph axes
        ax_y=Axes(
            x_range=[0,T_RETURN,0.7],y_range=[0,11,2],
            x_length=4.65,y_length=1.75,
            axis_config={"color":MUTED,"stroke_width":1.3,"include_tip":False},
        ).move_to([-1.2,1.55,0])
        ax_v=Axes(
            x_range=[0,T_RETURN,0.7],y_range=[-15,15,5],
            x_length=4.65,y_length=1.75,
            axis_config={"color":MUTED,"stroke_width":1.3,"include_tip":False},
        ).move_to([-1.2,-0.55,0])
        ax_a=Axes(
            x_range=[0,T_RETURN,0.7],y_range=[-12,2,4],
            x_length=4.65,y_length=1.65,
            axis_config={"color":MUTED,"stroke_width":1.3,"include_tip":False},
        ).move_to([-1.2,-2.50,0])

        cy=ax_y.plot(lambda tt:V0*tt-0.5*G*tt**2,x_range=[0,T_RETURN],color=CYAN,stroke_width=3)
        cv=ax_v.plot(lambda tt:V0-G*tt,x_range=[0,T_RETURN],color=YELLOW,stroke_width=3)
        ca=ax_a.plot(lambda tt:-G,x_range=[0,T_RETURN],color=RED,stroke_width=3)

        dy=always_redraw(lambda:Dot(ax_y.c2p(t.get_value(),V0*t.get_value()-0.5*G*t.get_value()**2),radius=0.07,color=CYAN))
        dv=always_redraw(lambda:Dot(ax_v.c2p(t.get_value(),V0-G*t.get_value()),radius=0.07,color=YELLOW))
        da=always_redraw(lambda:Dot(ax_a.c2p(t.get_value(),-G),radius=0.07,color=RED))

        labels=VGroup(
            self.tx("y(t)",20,CYAN,BOLD).next_to(ax_y,LEFT,buff=0.18),
            self.tx("v(t)",20,YELLOW,BOLD).next_to(ax_v,LEFT,buff=0.18),
            self.tx("a(t)",20,RED,BOLD).next_to(ax_a,LEFT,buff=0.18),
        )

        hud=self.live_readout(
            t,
            lambda tt:State(tt,V0*tt-0.5*G*tt**2,V0-G*tt,-G),
            "SAME INSTANT",
            x=5.15,
            y=-0.10,
        )

        self.play(FadeIn(traj),FadeIn(b),FadeIn(ax_y),FadeIn(ax_v),FadeIn(ax_a),FadeIn(labels))
        self.play(Create(cy),Create(cv),Create(ca),run_time=1.2)
        self.play(FadeIn(dy),FadeIn(dv),FadeIn(da),FadeIn(hud),run_time=0.5)
        self.play(t.animate.set_value(T_RETURN),run_time=5.0,rate_func=linear)

        insight=VGroup(
            self.mt(r"\text{slope of }y(t)=v(t)",28,CYAN),
            self.mt(r"\text{slope of }v(t)=a(t)",28,YELLOW),
        ).arrange(DOWN,buff=0.12).move_to([5.05,-2.35,0])
        self.play(FadeIn(insight))
        self.wait(2.4)
        self.clear_stage()

    # =========================================================================
    # 9 — 20 m drop with true quadratic motion and live impact state
    # =========================================================================
    def s9_drop_20m_live(self):
        self.header(
            9,
            "CAÍDA DESDE 20 m: EL TIEMPO Y LA RAPIDEZ NACEN DEL MODELO",
            "Soltamos: v₀ = 0. El suelo está en y = 0."
        )

        ruler=self.vertical_ruler(x=-5.7,y0=-2.65,y1=2.45,meters=20)
        ground=self.ground(y=-2.65,x0=-6.4,x1=0.9)
        t=ValueTracker(0.0)

        def state(tt):
            y=H_DROP-0.5*G*tt**2
            return State(tt,y,-G*tt,-G)

        def sy(tt):
            return -2.65+5.10*(state(tt).y/H_DROP)

        ball=always_redraw(lambda:self.ball([-3.25,sy(t.get_value()),0],0.19,CYAN))
        vel=always_redraw(lambda:
            self.vector(np.array([-2.62,sy(t.get_value()),0]),
                        DOWN*min(1.55,max(0.15,abs(state(t.get_value()).v)/14)),
                        r"\vec v",YELLOW,RIGHT,21)
        )
        acc=always_redraw(lambda:
            self.vector(np.array([-3.90,sy(t.get_value()),0]),DOWN*0.90,r"\vec a=-\vec g",RED,LEFT,21)
        )
        hud=self.live_readout(t,state,"20 m DROP",x=4.45,y=0.55)

        eq0=self.mt(r"0=20-\frac12gt^2",36,WHITE2).move_to([3.9,-1.60,0])
        eq1=self.mt(r"t=\sqrt{\frac{40}{9.81}}\approx "+f"{T_DROP:.2f}"+r"\,s",34,CYAN).move_to([3.9,-2.25,0])

        self.play(FadeIn(ruler),FadeIn(ground),FadeIn(ball),FadeIn(vel),FadeIn(acc),FadeIn(hud))
        self.play(Write(eq0))
        self.play(Write(eq1))
        self.play(t.animate.set_value(T_DROP),run_time=3.2,rate_func=linear)

        impact=self.pill(f"IMPACT: |v| ≈ {V_IMPACT:.2f} m/s",YELLOW,24).move_to([3.8,-3.05,0])
        self.play(FadeIn(impact))
        self.wait(2.4)
        self.clear_stage()

    # =========================================================================
    # 10 — equal-time strobe positions BEFORE formula
    # =========================================================================
    def s10_strobe_square_law(self):
        self.header(
            10,
            "MIRA LOS ESPACIOS ENTRE FOTOGRAMAS",
            "Tomamos fotos a intervalos iguales. Si la aceleración es constante, la separación crece."
        )

        top_y=2.25
        x=-2.7
        dt=0.20
        times=[0,dt,2*dt,3*dt,4*dt]
        dists=[0.5*G*t*t for t in times]
        scale=1.34

        guide=Line([x,-2.65,0],[x,top_y,0],color=GRID,stroke_width=2)
        clock=self.tx("Δt = 0.20 s between frames",22,MUTED,BOLD).move_to([3.6,2.25,0])
        self.play(Create(guide),FadeIn(clock))

        balls=VGroup()
        labels=VGroup()
        for i,(tt,dd) in enumerate(zip(times,dists)):
            y=top_y-scale*dd
            b=self.ball([x,y,0],0.13,CYAN)
            lab=self.tx(f"t={tt:.1f}s",18,WHITE2).next_to(b,LEFT,buff=0.15)
            balls.add(b); labels.add(lab)
            self.play(FadeIn(b,scale=0.7),FadeIn(lab),run_time=0.33)
            self.wait(0.18)

        # successive interval distances, proportional to odd numbers
        segments=VGroup()
        oddlabs=VGroup()
        for i in range(1,len(times)):
            y0=top_y-scale*dists[i-1]
            y1=top_y-scale*dists[i]
            seg=DoubleArrow([x+0.65,y0,0],[x+0.65,y1,0],buff=0.03,color=YELLOW,stroke_width=2,tip_length=0.11)
            lab=self.tx(str(2*i-1),22,YELLOW,BOLD).next_to(seg,RIGHT,buff=0.10)
            segments.add(seg); oddlabs.add(lab)

        self.play(LaggedStart(*[GrowArrow(s) for s in segments],lag_ratio=0.18),run_time=1.3)
        self.play(FadeIn(oddlabs))

        cumulative=self.tx("cumulative distance at equal times → 1 : 4 : 9 : 16",27,WHITE2,BOLD).move_to([3.6,0.55,0])
        square=self.mt(r"d\propto t^2",54,CYAN).move_to([3.6,-0.45,0])
        formula=self.mt(r"d=\frac12gt^2",48,CYAN).move_to([3.6,-1.55,0])

        self.play(FadeIn(cumulative))
        self.play(Write(square))
        self.wait(0.8)
        self.play(TransformMatchingTex(square.copy(),formula))
        self.wait(2.7)
        self.clear_stage()

    # =========================================================================
    # 11 — linearization d vs t², built point by point
    # =========================================================================
    def s11_lab_linearization(self):
        self.header(
            11,
            "CONVERTIMOS UNA PARÁBOLA EN UNA RECTA",
            "Graficar d contra t² permite probar el modelo y estimar g desde la pendiente."
        )

        left_axes=Axes(
            x_range=[0,0.85,0.2],y_range=[0,3.4,0.5],
            x_length=5.4,y_length=4.0,
            axis_config={"color":MUTED,"stroke_width":1.5,"include_tip":False},
        ).move_to([-3.75,-0.15,0])
        right_axes=Axes(
            x_range=[0,0.70,0.1],y_range=[0,3.4,0.5],
            x_length=5.4,y_length=4.0,
            axis_config={"color":MUTED,"stroke_width":1.5,"include_tip":False},
        ).move_to([3.75,-0.15,0])

        lt=self.tx("d vs t",22,WHITE2,BOLD).next_to(left_axes,UP,buff=0.15)
        rt=self.tx("d vs t²",22,CYAN,BOLD).next_to(right_axes,UP,buff=0.15)
        lx=self.mt(r"t\;(s)",22,MUTED).next_to(left_axes,DOWN,buff=0.12)
        rx=self.mt(r"t^2\;(s^2)",22,MUTED).next_to(right_axes,DOWN,buff=0.12)
        ly=self.mt(r"d\;(m)",22,MUTED).next_to(left_axes,LEFT,buff=0.12)
        ry=self.mt(r"d\;(m)",22,MUTED).next_to(right_axes,LEFT,buff=0.12)

        self.play(FadeIn(left_axes),FadeIn(right_axes),FadeIn(lt),FadeIn(rt),FadeIn(lx),FadeIn(rx),FadeIn(ly),FadeIn(ry))

        lp=VGroup()
        rp=VGroup()
        for tt,dd in zip(LAB_TIMES,LAB_D):
            p1=Dot(left_axes.c2p(tt,dd),radius=0.075,color=YELLOW)
            p2=Dot(right_axes.c2p(tt*tt,dd),radius=0.075,color=CYAN)
            lp.add(p1); rp.add(p2)
            self.play(FadeIn(p1,scale=0.5),run_time=0.20)
            self.play(TransformFromCopy(p1,p2),run_time=0.35)

        parabola=left_axes.plot(lambda tt:0.5*G*tt**2,x_range=[0,0.82],color=YELLOW,stroke_width=3)
        line=right_axes.plot(lambda t2:0.5*G*t2,x_range=[0,0.66],color=CYAN,stroke_width=3)
        self.play(Create(parabola),run_time=0.8)
        self.play(Create(line),run_time=0.8)

        slope=self.mt(r"m=\frac{\Delta d}{\Delta(t^2)}=\frac g2",34,CYAN).to_edge(DOWN,buff=0.28)
        gcalc=self.mt(r"g=2m",38,GREEN).next_to(slope,RIGHT,buff=0.55)
        self.play(Write(slope),FadeIn(gcalc))
        self.wait(2.8)
        self.clear_stage()

    # =========================================================================
    # 12 — experiment architecture
    # =========================================================================
    def s12_experimental_bridge(self):
        self.header(
            12,
            "DEL MODELO A LOS DATOS",
            "El laboratorio debe medir, repetir, graficar y decidir si los datos apoyan d ∝ t²."
        )

        nodes=[
            ("1","RELEASE","same point\nno push",CYAN),
            ("2","TIME","video or\nphotogate",YELLOW),
            ("3","DISTANCE","calibrated\nscale",GREEN),
            ("4","REPEAT","several\ntrials",PURPLE),
            ("5","PLOT","d vs t²",ORANGE),
            ("6","ESTIMATE","g = 2m",RED),
        ]

        groups=VGroup()
        arrows=VGroup()
        x_positions=np.linspace(-6.0,6.0,6)

        for i,(num,title,body,c) in enumerate(nodes):
            box=self.glass_panel(2.05,2.25,stroke=c,fill=PANEL,opacity=0.96).move_to([x_positions[i],0,0])
            badge=Circle(0.22,stroke_color=c,stroke_width=2,fill_color=PANEL_2,fill_opacity=1).move_to([x_positions[i],0.72,0])
            n=self.tx(num,18,c,BOLD).move_to(badge)
            tt=self.tx(title,20,c,BOLD).move_to([x_positions[i],0.15,0])
            bb=self.tx(body,18,WHITE2).move_to([x_positions[i],-0.50,0])
            groups.add(VGroup(box,badge,n,tt,bb))
            if i<5:
                arrows.add(Arrow([x_positions[i]+1.08,0,0],[x_positions[i+1]-1.08,0,0],buff=0,color=MUTED,stroke_width=2.2))

        self.play(FadeIn(groups[0],shift=RIGHT*0.1))
        for i in range(5):
            self.play(GrowArrow(arrows[i]),FadeIn(groups[i+1],shift=RIGHT*0.1),run_time=0.45)
            self.wait(0.25)

        final=self.tx(
            "A good experiment does not force the data to match the equation — it tests whether the pattern survives measurement uncertainty.",
            21,
            WHITE2,
            BOLD,
        )
        self.fit(final,13.8,0.7)
        final.move_to([0,-2.40,0])
        self.play(FadeIn(final))
        self.wait(3.0)
        self.clear_stage()

    # =========================================================================
    # CLOSING
    # =========================================================================
    def closing(self):
        title=self.tx("THEORY COMPLETE",42,WHITE2,BOLD).move_to([0,2.35,0])
        sub=self.tx("Now the laboratory has a measurable prediction.",27,CYAN,BOLD).move_to([0,1.65,0])

        chain=VGroup(
            self.pill("FORCES",RED,22),
            self.pill("a = −g",RED,22),
            self.pill("v(t)",YELLOW,22),
            self.pill("y(t)",CYAN,22),
            self.pill("d ∝ t²",GREEN,22),
            self.pill("d vs t²",PURPLE,22),
            self.pill("g = 2m",ORANGE,22),
        ).arrange(RIGHT,buff=0.20).move_to([0,0.15,0])

        arrows=VGroup(*[
            Arrow(chain[i].get_right()+RIGHT*0.05,chain[i+1].get_left()+LEFT*0.05,
                  buff=0,color=MUTED,stroke_width=2)
            for i in range(len(chain)-1)
        ])

        next_lab=self.tx(
            "NEXT: apparatus → measurement protocol → repeated trials → regression → experimental g → uncertainty",
            23,
            WHITE2,
            BOLD,
        ).move_to([0,-2.10,0])
        self.fit(next_lab,13.8,0.7)

        self.play(Write(title),FadeIn(sub))
        self.play(LaggedStart(*[FadeIn(x,shift=UP*0.05) for x in chain],lag_ratio=0.10),run_time=1.3)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=0.12),run_time=1.0)
        self.wait(1.3)
        self.play(FadeIn(next_lab))
        self.wait(4.0)
        self.clear_stage()
