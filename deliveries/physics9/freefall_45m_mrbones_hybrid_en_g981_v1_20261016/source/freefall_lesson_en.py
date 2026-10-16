"""Physics 9 · Free fall from 45 m with Mr. Bones — ManimCE lesson (engine A of the hybrid video), ENGLISH, g = 9.81 m/s².

Protocolo HYBRID-SCIANIM-v1: 1920x1080, 30 fps, fondo blanco, Noto Serif, colores semánticos
(C_POS posición, C_VEL velocidad/incrementos, C_ACC aceleración/gravedad, C_GAL conclusión
verificada). Cada sección es una escena que empieza y termina en un fotograma blanco; el video final
intercala estas escenas con los clips del motor cartoon (Mr. Bones).

TODOS los números salen de ../shared/derived.json, escrito por verify_caida_libre.py (con asserts),
que usa las mismas constantes que el motor cartoon (../shared/constants.json).

Render:  manim -qh --fps 30 caida_libre_leccion.py A1Pregunta A2NumerosPrimero ...
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np
from manim import *

HERE = Path(__file__).resolve().parent
D = json.loads((HERE.parent / "shared" / "derived.json").read_text())
CST = D["constants"]
H, G = CST["H"], CST["g"]
CASES = D["cases"]

config.pixel_width, config.pixel_height = 1920, 1080
config.frame_width, config.frame_height = 16, 9
config.frame_rate = 30
config.background_color = "#FFFFFF"

# ---------------------------------------------------------------- design tokens (shared)
BG, INK, MUTED, RULE, FILL, STROKE = "#FFFFFF", "#151515", "#6E6E6E", "#D6D6D6", "#F3F3F3", "#3C3C3C"
C_ACC, C_VEL, C_POS, C_GAL = "#B03A2E", "#B7791F", "#2C6E9B", "#2F7D5B"
SERIF = "Noto Serif"
TXT_SCALE = 1.15
TS = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
P_BEAT, P_SHORT, P_MED, P_LONG, P_READ = 0.8, 1.5, 2.5, 4.0, 6.0


def fmt(x, d=1):
    s = f"{x:.{d}f}"
    if s in ("-0.0", "-0.00", "-0"):
        s = s[1:]
    return s  # English: decimal point


def T(s, size=30, color=INK, weight=NORMAL, slant=NORMAL):
    """Text built at 2x then scaled 0.5 (crisper glyph outlines)."""
    return Text(s, font=SERIF, font_size=size * 2 * TXT_SCALE, color=color, weight=weight, slant=slant).scale(0.5)


def M(tex, size=40, color=INK, **kw):
    return MathTex(tex, font_size=size * TXT_SCALE, color=color, **kw)


def fit(m, w, h=None):
    if m.width > w:
        m.scale_to_fit_width(w)
    if h is not None and m.height > h:
        m.scale_to_fit_height(h)
    return m


class Lesson(MovingCameraScene):
    NUM, TITLE, SUB = "00", "", ""

    # ------------------------------------------------------------ helpers (protocol components)
    def wait_s(self, s):
        self.wait(s * TS)

    def read_time(self, text):
        return max(2.0, 0.35 * len(text.split()))

    def header(self):
        box = Square(0.78, color=INK, fill_color=INK, fill_opacity=1, stroke_width=0)
        num = T(self.NUM, 30, BG, BOLD).move_to(box)
        title = T(self.TITLE.upper(), 34, INK, BOLD)
        sub = T(self.SUB, 22, MUTED)
        txt = VGroup(title, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        g = VGroup(VGroup(box, num), txt).arrange(RIGHT, buff=0.28, aligned_edge=UP)
        g.to_corner(UL, buff=0.5)
        rule = Line(LEFT * 7.5, RIGHT * 7.5, color=RULE, stroke_width=1.5).next_to(g, DOWN, buff=0.18)
        rule.set_x(0)
        self.hdr = VGroup(g, rule)
        return self.hdr

    def card(self, content, pad=0.3, stroke=RULE, fill=BG, width=None):
        w = max(content.width + 2 * pad, width or 0)
        r = RoundedRectangle(corner_radius=0.08, width=w, height=content.height + 2 * pad, stroke_color=stroke, stroke_width=2, fill_color=fill, fill_opacity=1)
        r.move_to(content)
        return VGroup(r, content)

    def info_box(self, title, lines, maxw=6.2, stroke=RULE, title_color=INK):
        t = T(title, 24, title_color, BOLD)
        body = VGroup(*[l if isinstance(l, Mobject) else T(l, 24, INK) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        g = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fit(g, maxw - 0.6)
        return self.card(g, stroke=stroke, width=maxw)

    def predict_box(self, lines):
        t = T("PAUSE · PREDICT", 26, C_ACC, BOLD)
        body = VGroup(*[T(l, 26) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        return self.card(VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3), stroke=C_ACC)

    def note(self, s):
        n = T(s, 18, MUTED, slant=ITALIC)
        n.to_corner(DL, buff=0.35)
        return n

    def begin(self):
        self.wait(1 / 30)  # first frame: pure white
        h = self.header()
        self.play(FadeIn(h, shift=RIGHT * 0.2), run_time=0.9 * TS)

    def end(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9 * TS)
        self.wait(0.2)  # last frames: pure white

    def construct(self):
        self.begin()
        self.body()
        self.end()

    def body(self):
        pass

    # building + axis schematic (not to scale horizontally), height mapped 45 m -> hgt units
    def building(self, x=-4.6, y0=-3.6, hgt=6.0, w=1.6):
        b = Rectangle(width=w, height=hgt, stroke_color=STROKE, stroke_width=2.5, fill_color=FILL, fill_opacity=1).move_to([x, y0 + hgt / 2, 0])
        floors = VGroup(*[Line([x - w / 2, y0 + k * hgt / 15, 0], [x + w / 2, y0 + k * hgt / 15, 0], color=RULE, stroke_width=1.2) for k in range(1, 15)])
        ground = Line([x - 2.2, y0, 0], [x + 3.4, y0, 0], color=INK, stroke_width=3)
        return VGroup(b, floors, ground)


HG = 0.5 * G  # 4.905 m/s^2 (half g), the coefficient of t^2


def num(x, d):
    return fmt(x, d)


# ==================================================================== A1 · question + convention
class A1Pregunta(Lesson):
    NUM, TITLE, SUB = "01", "The question", "One head, a 45 m building and three ways to let it go"

    def body(self):
        hgt, y0, x = 5.3, -3.75, -5.6
        bld = self.building(x, y0, hgt)
        ax = Arrow([x + 1.5, y0, 0], [x + 1.5, y0 + hgt + 0.9, 0], buff=0, color=C_POS, stroke_width=4, max_tip_length_to_length_ratio=0.06)
        ylab = M(r"+y", 36, C_POS).next_to(ax.get_end(), RIGHT, buff=0.1)
        o = Dot([x + 1.5, y0, 0], color=C_POS)
        olab = M(r"y=0", 30, C_POS).next_to(o, RIGHT, buff=0.12).shift(UP * 0.25)
        top = DashedLine([x - 0.8, y0 + hgt, 0], [x + 2.2, y0 + hgt, 0], color=C_POS, stroke_width=2)
        tlab = M(r"y_0=45\ \mathrm{m}", 32, C_POS).next_to(top, UP, buff=0.08).shift(LEFT * 0.4)
        skull = Circle(0.16, color=INK, fill_color=BG, fill_opacity=1, stroke_width=3).move_to([x + 0.95, y0 + hgt, 0])
        g_arrow = Arrow(skull.get_center() + DOWN * 0.3, skull.get_center() + DOWN * 1.4, buff=0, color=C_ACC, stroke_width=5)
        g_lab = M(r"\vec a=-g\,\hat{y}", 32, C_ACC).next_to(g_arrow, LEFT, buff=0.1)
        self.play(Create(bld), run_time=1.4 * TS)
        self.play(GrowArrow(ax), FadeIn(ylab), FadeIn(o), FadeIn(olab), run_time=1.2 * TS)
        self.play(Create(top), FadeIn(tlab), FadeIn(skull), run_time=1.0 * TS)
        self.play(GrowArrow(g_arrow), FadeIn(g_lab), run_time=1.0 * TS)
        conv = self.info_box("SIGN CONVENTION (fixed before any calculation)", [
            T("+y axis points up; the origin y = 0 is at the ground.", 24),
            T("Moving up means v > 0; moving down means v < 0.", 24),
            VGroup(T("Gravity points down:", 24), M(rf"a=-g=-{num(G,2)}\ \mathrm{{m/s^2}}", 34, C_ACC)).arrange(RIGHT, buff=0.2),
            T("No air: the head is a particle (its centre of mass).", 22, MUTED),
        ], maxw=9.6).move_to([2.6, 1.15, 0])
        self.play(FadeIn(conv, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        q = self.info_box("THE QUESTION", [
            T("From 45 m: how long does the head take to reach the ground,", 26),
            T("and how fast is it going when it lands, if...", 26),
            VGroup(T("1) it is released", 26, INK), M(r"(v_0=0)", 32, C_VEL)).arrange(RIGHT, buff=0.15),
            VGroup(T("2) it is thrown downward", 26), M(r"(v_0=-10\ \mathrm{m/s})", 32, C_VEL)).arrange(RIGHT, buff=0.15),
            VGroup(T("3) it is thrown upward", 26), M(r"(v_0=+10\ \mathrm{m/s})", 32, C_VEL)).arrange(RIGHT, buff=0.15),
        ], maxw=9.6).move_to([2.6, -2.15, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        self.play(FadeOut(conv), FadeOut(q), run_time=0.7 * TS)
        pb = self.predict_box([
            "Which one reaches the ground first?",
            "Which one lands the fastest?",
            "Do cases 2 and 3 land equally fast?",
        ]).move_to([2.6, 0, 0])
        self.play(FadeIn(pb, scale=0.96), run_time=0.8 * TS)
        for k in range(5, 0, -1):
            c = T(str(k), 40, C_ACC, BOLD).next_to(pb, DOWN, buff=0.3)
            self.add(c)
            self.wait_s(1.0)
            self.remove(c)
        self.add(self.note("First we watch the phenomenon (case 1); the numbers come after."))
        self.wait_s(P_SHORT)


# ==================================================================== A2 · numbers first
class A2NumerosPrimero(Lesson):
    NUM, TITLE, SUB = "02", "Numbers first", "What the stroboscope recorded in case 1, second by second"

    def body(self):
        nf = D["numbers_first"]
        rows = [("t (s)", [str(t) for t in nf["t"]], INK),
                ("y (m)", [num(H - d, 1) for d in nf["drop"]], C_POS),
                ("drop (m)", [num(d, 1) for d in nf["drop"]], C_POS),
                ("v (m/s)", [num(-v, 1) for v in nf["v"]], C_VEL)]
        cw, rh = 1.4, 1.05
        x0, y0 = -7.3, 2.1
        grid = VGroup()
        cells = {}
        for r, (lab, vals, col) in enumerate(rows):
            y = y0 - r * rh
            grid.add(T(lab, 26, col, BOLD).move_to([x0 + 1.0, y, 0]))
            for c, v in enumerate(vals):
                m = T(v, 28, col).move_to([x0 + 2.6 + c * cw, y, 0])
                cells[(r, c)] = m
                grid.add(m)
        lines = VGroup(*[Line([x0, y0 - (r + 0.5) * rh, 0], [x0 + 2.6 + 3.5 * cw, y0 - (r + 0.5) * rh, 0], color=RULE, stroke_width=1.5) for r in range(4)])
        self.play(FadeIn(lines), *[FadeIn(grid[k]) for k in range(len(grid)) if k % 5 == 0], run_time=0.8 * TS)
        for c in range(4):
            self.play(*[FadeIn(cells[(r, c)], shift=DOWN * 0.1) for r in range(4)], run_time=0.55 * TS)
        self.wait_s(P_MED)
        incr = nf["increments"]
        braces = VGroup()
        for i, d in enumerate(incr):
            a, b = cells[(2, i)], cells[(2, i + 1)]
            br = ArcBetweenPoints(a.get_bottom() + DOWN * 0.15, b.get_bottom() + DOWN * 0.15, angle=PI / 2.4, color=C_VEL, stroke_width=3)
            lab = M(rf"+{num(d, 1)}", 24, C_VEL).next_to(br, UP, buff=0.02).shift(DOWN * 0.42)
            braces.add(VGroup(br, lab))
        self.play(LaggedStart(*[Create(b) for b in braces], lag_ratio=0.4), run_time=1.6 * TS)
        ratio = self.info_box("IT FALLS MORE EVERY SECOND", [M(rf"{num(incr[0],3)} : {num(incr[1],3)} : {num(incr[2],3)} \;=\; 1 : 3 : 5", 36, C_VEL), T("odd numbers: the speed grows evenly", 24)], maxw=6.6).move_to([3.95, 2.05, 0])
        self.play(FadeIn(ratio), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        dv = VGroup()
        for i in range(3):
            a, b = cells[(3, i)], cells[(3, i + 1)]
            arc = ArcBetweenPoints(a.get_bottom() + DOWN * 0.15, b.get_bottom() + DOWN * 0.15, angle=PI / 2.4, color=C_ACC, stroke_width=3)
            dv.add(VGroup(arc, M(rf"-{num(G,2)}", 24, C_ACC).next_to(arc, DOWN, buff=0.05)))
        self.play(LaggedStart(*[Create(b) for b in dv], lag_ratio=0.4), run_time=1.4 * TS)
        acc = self.info_box("THE VELOCITY CHANGES BY THE SAME AMOUNT EVERY SECOND", [M(rf"a=\frac{{\Delta v}}{{\Delta t}}=\frac{{-{num(G,2)}\ \mathrm{{m/s}}}}{{1\ \mathrm{{s}}}}=-{num(G,2)}\ \mathrm{{m/s^2}}", 38, C_ACC)], maxw=6.6).move_to([3.95, -0.3, 0])
        self.play(FadeIn(acc), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        avg = nf["avg_speed"]
        txt = self.info_box("AVERAGE SPEED IN EACH SECOND", [
            M(rf"\frac{{{num(incr[0],3)}\ \mathrm{{m}}}}{{1\ \mathrm{{s}}}},\ \frac{{{num(incr[1],3)}}}{{1}},\ \frac{{{num(incr[2],3)}}}{{1}}\ \mathrm{{m/s}}", 30, C_VEL),
            T("= the speed at the middle of each second (0.5 s, 1.5 s, 2.5 s)", 22, MUTED),
            M(r"\text{drop}=\bar v\,t=\frac{0+g t}{2}\,t=\tfrac12 g t^2", 36, C_POS),
        ], maxw=7.6).move_to([3.95, -2.75, 0])
        self.play(FadeOut(ratio), acc.animate.move_to([3.95, 2.05, 0]), run_time=0.8 * TS)
        self.play(FadeIn(txt, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        res = self.card(M(rf"y=45-{num(HG,3)}\,t^2", 50, C_POS), stroke=C_GAL).move_to([-4.4, -3.2, 0])
        self.play(FadeIn(res, scale=0.95), run_time=0.9 * TS)
        c1 = CASES["1"]
        self.add(self.note(f"At t = 3 s it is still {num(H - 0.5 * G * 9, 1)} m up: y(t) = 0 at t = {num(c1['T'], 2)} s."))
        self.wait_s(P_LONG)


# ==================================================================== A3 · the equation term by term
class A3Ecuacion(Lesson):
    NUM, TITLE, SUB = "03", "The equation, term by term", "One model for all three cases"

    def body(self):
        eq = MathTex(r"y", r"=", r"y_0", r"+", r"v_0\,t", r"-", r"\tfrac12\,g\,t^2", font_size=88 * TXT_SCALE, color=INK).move_to([0, 2.0, 0])
        self.play(Write(eq), run_time=1.6 * TS)
        self.wait_s(P_SHORT)
        expl = [
            (0, C_POS, "y: position at time t (metres, measured from the ground)"),
            (2, C_POS, "y₀ = 45 m: the height it starts from (positive: it is above the ground)"),
            (4, C_VEL, "v₀·t: how far it would move with no gravity (sign of v₀: + up, − down)"),
            (6, C_ACC, "−½ g t²: how far gravity pulls it down; always downward (−)"),
        ]
        box = None
        for idx, col, s in expl:
            frame = SurroundingRectangle(eq[idx], color=col, buff=0.12, stroke_width=4)
            nb = self.card(T(s, 28, col), stroke=col).move_to([0, -0.3, 0])
            fit(nb, 14.5)
            anims = [Create(frame), eq[idx].animate.set_color(col)]
            if box is not None:
                anims += [FadeOut(box[0]), FadeOut(box[1])]
            self.play(*anims, FadeIn(nb, shift=UP * 0.15), run_time=0.9 * TS)
            self.wait_s(self.read_time(s))
            box = (frame, nb)
        self.play(FadeOut(box[0]), FadeOut(box[1]), run_time=0.6 * TS)
        v = MathTex(r"v", r"=", r"v_0", r"-", r"g\,t", font_size=72 * TXT_SCALE, color=INK).move_to([0, 0.4, 0])
        v[0].set_color(C_VEL); v[2].set_color(C_VEL); v[4].set_color(C_ACC)
        self.play(Write(v), run_time=1.2 * TS)
        vb = self.card(T(f"The velocity loses {num(G,2)} m/s every second (or gains {num(G,2)} m/s downward).", 26, INK), stroke=RULE).move_to([0, -0.85, 0])
        fit(vb, 14.5)
        self.play(FadeIn(vb), run_time=0.7 * TS)
        self.wait_s(P_LONG)
        u = self.info_box("UNITS CHECK", [
            M(r"[y]=\mathrm{m}\qquad [v_0\,t]=\frac{\mathrm{m}}{\mathrm{s}}\cdot\mathrm{s}=\mathrm{m}\qquad [g\,t^2]=\frac{\mathrm{m}}{\mathrm{s}^2}\cdot\mathrm{s}^2=\mathrm{m}", 36, INK),
            T("Every term is in metres: the equation is consistent.", 24, C_GAL),
        ], maxw=13.5, stroke=C_GAL).move_to([0, -2.45, 0])
        self.play(FadeIn(u, shift=UP * 0.2), run_time=0.9 * TS)
        self.add(self.note(f"With g = {num(G,2)} m/s²: y = 45 + v₀t − {num(HG,3)}t² and v = v₀ − {num(G,2)}t."))
        self.wait_s(P_READ)


# ==================================================================== A4 · the sling
class A4Honda(Lesson):
    NUM, TITLE, SUB = "04", "Mr. Bones' sling", "Circular motion that ends in a vertical launch"

    def body(self):
        sl = D["sling"]
        R, w = sl["R"], sl["omega"]
        sc = 3.4
        C = np.array([-3.3, -0.3, 0])
        circ = DashedVMobject(Circle(R * sc, color=C_POS, stroke_width=3), num_dashes=48).move_to(C)
        cdot = Dot(C, color=C_POS, radius=0.08)
        clab = T("C (right hand, fixed)", 22, C_POS).next_to(cdot, LEFT, buff=0.15).shift(UP * 0.25)
        th = ValueTracker(-PI / 2)
        arm = always_redraw(lambda: Line(C, C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0]), color=STROKE, stroke_width=9))
        skull = always_redraw(lambda: Circle(0.22, color=INK, fill_color=BG, fill_opacity=1, stroke_width=3).move_to(C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0])))
        vel = always_redraw(lambda: Arrow(C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0]),
                                         C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0]) + 1.25 * np.array([-math.sin(th.get_value()), math.cos(th.get_value()), 0]),
                                         buff=0.22, color=C_VEL, stroke_width=6))
        rlab = M(rf"R={num(R,3)}\ \mathrm{{m}}", 30, C_POS).move_to(C + np.array([R * sc * 0.5 - 0.3, -0.38, 0]))
        self.play(Create(circ), FadeIn(cdot), FadeIn(clab), run_time=1.2 * TS)
        self.add(arm, skull)
        self.play(FadeIn(rlab), run_time=0.5 * TS)
        self.add(vel)
        info = self.info_box("THE VELOCITY IS TANGENT TO THE CIRCLE", [
            M(r"v=\omega\,R", 44, C_VEL),
            T("ω: angular speed (rad/s); R: radius (m)", 22, MUTED),
        ], maxw=6.6).move_to([3.9, 2.0, 0])
        self.play(FadeIn(info), run_time=0.8 * TS)
        self.play(th.animate.set_value(-PI / 2 + 2 * PI), run_time=2.6 * TS, rate_func=rate_functions.ease_in_quad)
        self.play(th.animate.set_value(-PI / 2 + 4 * PI), run_time=1.3 * TS, rate_func=linear)
        self.play(th.animate.set_value(4 * PI), run_time=0.45 * TS, rate_func=linear)
        mark = Line(C, C + RIGHT * R * sc, color=C_GAL, stroke_width=6)
        ml = VGroup(T("horizontal radius", 24, C_GAL), T("→ vertical velocity", 24, C_GAL)).arrange(DOWN, buff=0.12).next_to(circ, DOWN, buff=0.25)
        self.play(Create(mark), FadeIn(ml), run_time=0.8 * TS)
        self.wait_s(P_MED)
        need = self.info_box("TO LEAVE AT 10 m/s", [
            M(rf"\omega=\frac{{v_0}}{{R}}=\frac{{10\ \mathrm{{m/s}}}}{{{num(R,3)}\ \mathrm{{m}}}}\approx {num(w,1)}\ \mathrm{{rad/s}}", 38, INK),
            M(rf"\approx {num(sl['rev_per_s'],2)}\ \text{{turns/s}}", 34, MUTED),
            M(rf"a_c=\omega^2R\approx {num(sl['centripetal_acc'],0)}\ \mathrm{{m/s^2}}\approx {num(sl['centripetal_in_g'],1)}\,g", 36, C_ACC),
        ], maxw=6.6).move_to([3.9, -0.65, 0])
        self.play(FadeIn(need, shift=UP * 0.15), run_time=0.9 * TS)
        self.wait_s(P_READ)
        up = Arrow(C + RIGHT * R * sc, C + RIGHT * R * sc + UP * 1.7, buff=0.22, color=C_VEL, stroke_width=8)
        dn = Arrow(C + RIGHT * R * sc, C + RIGHT * R * sc + DOWN * 1.7, buff=0.22, color=C_VEL, stroke_width=8)
        self.remove(vel)
        self.play(GrowArrow(up), run_time=0.6 * TS)
        lab = VGroup(T("counter-clockwise: it leaves upward (case 3)", 24, C_VEL), T("clockwise: it leaves downward (case 2)", 24, C_VEL)).arrange(DOWN, aligned_edge=LEFT)
        lab.move_to([0, -3.05, 0]).align_to(need, RIGHT)
        self.play(FadeIn(lab[0]), run_time=0.5 * TS)
        self.play(GrowArrow(dn), FadeIn(lab[1]), run_time=0.6 * TS)
        self.add(self.note("Once released the sling no longer pushes: only gravity acts. From there on it is free fall."))
        self.wait_s(P_READ)


# ==================================================================== A5 · three cases, one equation
class A5TresCasos(Lesson):
    NUM, TITLE, SUB = "05", "Three cases, one equation", "Same clock, same gravity: only v₀ changes"

    def body(self):
        hgt, y0 = 4.9, -3.75
        s = hgt / 52.0
        xs = [-6.3, -4.6, -2.9]
        t = ValueTracker(0.0)
        ground = Line([-7.3, y0, 0], [-1.9, y0, 0], color=INK, stroke_width=3)
        top = DashedLine([-7.3, y0 + 45 * s, 0], [-1.9, y0 + 45 * s, 0], color=C_POS, stroke_width=2)
        tl = M(r"45\ \mathrm{m}", 26, C_POS).next_to(top, LEFT, buff=0.08).shift(RIGHT * 0.9 + UP * 0.2)
        yap = CASES["3"]["y_apex"]
        apex = DashedLine([-3.4, y0 + yap * s, 0], [-2.4, y0 + yap * s, 0], color=C_POS, stroke_width=2)
        self.play(Create(ground), Create(top), FadeIn(tl), run_time=0.8 * TS)
        heads = VGroup()
        for i, k in enumerate(["1", "2", "3"]):
            c = CASES[k]
            col_lab = T(f"case {k}", 24, INK, BOLD).move_to([xs[i], y0 + 52 * s + 0.35, 0])

            def ypos(c=c):
                tt = min(t.get_value(), c["T"])
                return y0 + s * (H + c["v0"] * tt - 0.5 * G * tt * tt)

            dot = always_redraw(lambda x=xs[i], ypos=ypos: Circle(0.15, color=INK, fill_color=BG, fill_opacity=1, stroke_width=3).move_to([x, ypos(), 0]))
            heads.add(col_lab)
            self.add(dot)
        self.play(FadeIn(heads), Create(apex), run_time=0.6 * TS)
        state = always_redraw(lambda: self.card(M(rf"t={num(t.get_value(),2)}\ \mathrm{{s}}", 40, INK), width=3.2).move_to([-4.6, 2.2, 0]))
        self.add(state)
        self.play(t.animate.set_value(CASES["3"]["T"]), run_time=CASES["3"]["T"] * 1.0 * TS, rate_func=linear)
        self.wait_s(P_SHORT)
        a = HG
        rows = []
        for k in ["1", "2", "3"]:
            c = CASES[k]
            v0 = c["v0"]
            if k == "1":
                l1 = rf"0=45+0\cdot t-{num(a,3)}\,t^2"
                l2 = rf"t^2=\frac{{45}}{{{num(a,3)}}}={num(45/a,3)}\;\Rightarrow\;t=\sqrt{{{num(45/a,3)}}}"
            elif k == "2":
                l1 = rf"0=45-10t-{num(a,3)}\,t^2"
                l2 = rf"{num(a,3)}\,t^2+10t-45=0\;\Rightarrow\;t=\frac{{-10+\sqrt{{100+4({num(a,3)})(45)}}}}{{2({num(a,3)})}}"
            else:
                l1 = rf"0=45+10t-{num(a,3)}\,t^2"
                l2 = rf"{num(a,3)}\,t^2-10t-45=0\;\Rightarrow\;t=\frac{{10+\sqrt{{100+4({num(a,3)})(45)}}}}{{2({num(a,3)})}}"
            res = rf"t\approx{num(c['T'],2)}\ \mathrm{{s}},\quad v={num(v0,0)}-{num(G,2)}\,({num(c['T'],2)})\approx{num(c['v_impact'],1)}\ \mathrm{{m/s}}"
            rows.append((k, l1, l2, res))
        panel = VGroup()
        for i, (k, l1, l2, res) in enumerate(rows):
            g = VGroup(T(f"Case {k}", 26, INK, BOLD), M(l1, 34, C_POS), M(l2, 32, INK), M(res, 32, C_VEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            panel.add(g)
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(panel, 8.4, 5.9)
        panel.move_to([3.2, -1.0, 0])
        for g in panel:
            self.play(FadeIn(g[0]), Write(g[1]), run_time=0.9 * TS)
            self.wait_s(P_SHORT)
            self.play(Write(g[2]), run_time=0.9 * TS)
            self.wait_s(P_SHORT)
            self.play(FadeIn(g[3], shift=RIGHT * 0.1), run_time=0.7 * TS)
            self.wait_s(P_MED)
        quad = self.card(M(r"t=\frac{-b+\sqrt{b^2-4ac}}{2a}\quad(\text{positive root})", 30, MUTED)).move_to([4.6, 2.5, 0])
        self.play(FadeIn(quad), run_time=0.6 * TS)
        self.wait_s(P_LONG)


# ==================================================================== A6 · top point, symmetry, time-free
class A6PuntoAlto(Lesson):
    NUM, TITLE, SUB = "06", "The highest point and the symmetry", "Case 3: v = 0 for an instant, but gravity does not switch off"

    def body(self):
        c3, c2 = CASES["3"], CASES["2"]
        ax = Axes(x_range=[0, 4.5, 1], y_range=[-35, 12, 10], x_length=7.2, y_length=5.2, tips=False,
                  axis_config={"color": INK, "stroke_width": 2, "include_numbers": True, "font_size": 26, "decimal_number_config": {"num_decimal_places": 0, "color": INK}}).move_to([-3.4, -0.6, 0])
        xl = M(r"t\ (\mathrm{s})", 28).next_to(ax.x_axis, RIGHT, buff=0.1).shift(UP * 0.35)
        yl = M(r"v\ (\mathrm{m/s})", 28, C_VEL).next_to(ax.y_axis, UP, buff=0.1)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.2 * TS)
        line = ax.plot(lambda t: c3["v0"] - G * t, x_range=[0, c3["T"]], color=C_VEL, stroke_width=5)
        self.play(Create(line), run_time=2.0 * TS)
        apex = Dot(ax.c2p(c3["t_apex"], 0), color=C_ACC, radius=0.1)
        al = self.card(M(rf"t={num(c3['t_apex'],2)}\ \mathrm{{s}}:\ v=0", 30, C_ACC), stroke=C_ACC).next_to(apex, UR, buff=0.2)
        self.play(FadeIn(apex), FadeIn(al), run_time=0.7 * TS)
        mis = self.info_box("COMMON MISTAKE", [T("“At the top v = 0, so a = 0”: FALSE.", 26, C_ACC),
                                                M(rf"a=\frac{{\Delta v}}{{\Delta t}}=-{num(G,2)}\ \mathrm{{m/s^2}}\ \text{{always (constant slope)}}", 32, C_ACC),
                                                T("If a were 0 at the top, it would stay floating there.", 22, MUTED)], maxw=7.2, stroke=C_ACC).move_to([4.1, 1.7, 0])
        self.play(FadeIn(mis), run_time=0.9 * TS)
        self.wait_s(P_READ)
        ym = self.info_box("MAXIMUM HEIGHT", [M(rf"y_{{max}}=45+\frac{{v_0^2}}{{2g}}=45+\frac{{100}}{{{num(2*G,2)}}}\approx{num(c3['y_apex'],2)}\ \mathrm{{m}}", 34, C_POS)], maxw=7.2).move_to([4.1, -0.25, 0])
        self.play(FadeIn(ym), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        sym = Dot(ax.c2p(c3["t_back"], c3["v_back"]), color=C_VEL, radius=0.1)
        syl = self.card(M(rf"t={num(c3['t_back'],2)}\ \mathrm{{s}}:\ y=45\ \mathrm{{m}},\ v={num(c3['v_back'],0)}\ \mathrm{{m/s}}", 28, C_VEL)).next_to(sym, DOWN, buff=0.25).shift(RIGHT * 0.9)
        self.play(FadeIn(sym), FadeIn(syl), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        tf = self.info_box("TIME-FREE RELATION", [
            M(r"v^2=v_0^2+2gh", 40, INK),
            M(rf"(\pm10)^2+2({num(G,2)})(45)={num(c2['disc'],1)}", 32, C_VEL),
            M(rf"|v|=\sqrt{{{num(c2['disc'],1)}}}\approx{num(c2['speed_impact'],1)}\ \mathrm{{m/s}}", 32, C_VEL),
            T("Cases 2 and 3: same v₀², same landing speed; different times.", 24, C_GAL),
        ], maxw=7.6, stroke=C_GAL).move_to([4.0, -1.2, 0])
        self.play(FadeOut(mis), ym.animate.move_to([4.1, 2.3, 0]), run_time=0.7 * TS)
        self.play(FadeIn(tf, shift=UP * 0.2), run_time=0.9 * TS)
        self.wait_s(P_READ)


# ==================================================================== A7 · real-world exceptions
class A7Excepciones(Lesson):
    NUM, TITLE, SUB = "07", "Real-world exceptions", "What changes if g is rounded to 10 m/s², and with air"

    def body(self):
        rnd_, drag = D["rounded_g"], D["drag"]
        hdr = ["", "case 1", "case 2", "case 3"]
        data = [
            (f"g = {num(G,2)} (ideal)", [CASES[k]["T"] for k in "123"], [CASES[k]["speed_impact"] for k in "123"], INK),
            ("g = 10 (rounded)", [rnd_[k]["T"] for k in "123"], [rnd_[k]["speed_impact"] for k in "123"], C_POS),
            (f"g = {num(G,2)} + air*", [drag["cases"][k]["T"] for k in "123"], [-drag["cases"][k]["v_impact"] for k in "123"], C_ACC),
        ]
        x0, y0, cw, rh = -7.4, 2.35, 3.45, 0.82
        tab = VGroup()
        for c, h in enumerate(hdr):
            tab.add(T(h, 26, INK, BOLD).move_to([x0 + 1.3 + c * cw, y0, 0]))
        for r, (lab, Ts, Vs, col) in enumerate(data):
            y = y0 - (r + 1) * rh
            tab.add(T(lab, 24, col, BOLD).move_to([x0 + 1.45, y, 0]))
            for c in range(3):
                tab.add(M(rf"{num(Ts[c],2)}\ \mathrm{{s}}\ \cdot\ {num(Vs[c],1)}\ \mathrm{{m/s}}", 28, col).move_to([x0 + 1.3 + (c + 1) * cw, y, 0]))
        lines = VGroup(*[Line([x0, y0 - (r + 0.5) * rh, 0], [x0 + 1.3 + 3.5 * cw, y0 - (r + 0.5) * rh, 0], color=RULE, stroke_width=1.5) for r in range(4)])
        self.play(FadeIn(lines), FadeIn(tab[:4]), run_time=0.8 * TS)
        for r in range(3):
            self.play(FadeIn(tab[4 + r * 4: 8 + r * 4], shift=RIGHT * 0.1), run_time=0.8 * TS)
            self.wait_s(P_MED)
        a = CST["air"]
        model = self.info_box("*AIR MODEL (estimate for a real skull)", [
            M(r"F_d=\tfrac12\,\rho\,C_d\,A\,v^2", 36, C_ACC),
            M(rf"\rho={num(a['rho'],1)}\ \mathrm{{kg/m^3}},\ C_d={num(a['Cd'],1)},\ m={num(a['mass_kg'],1)}\ \mathrm{{kg}},\ d={num(a['diameter_m'],2)}\ \mathrm{{m}}", 28, INK),
            M(rf"v_{{\text{{terminal}}}}=\sqrt{{\frac{{2mg}}{{\rho C_d A}}}}\approx{num(drag['v_terminal'],1)}\ \mathrm{{m/s}}", 32, C_ACC),
            T("Numerical RK4 integration (dt = 10 µs); case 1 matches the exact solution.", 22, MUTED),
        ], maxw=9.4, stroke=C_ACC).move_to([-2.6, -2.3, 0])
        self.play(FadeIn(model, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        concl = self.info_box("WHAT WE CONCLUDE", [
            T("Rounding g to 10 shortens the times by ~1%.", 24),
            T("With air it lands later and slower,", 24),
            T("and cases 2 and 3 no longer land equally fast.", 24, C_ACC),
            T("The ideal model is the base; air is the correction.", 24, C_GAL),
        ], maxw=5.6, stroke=C_GAL).move_to([5.05, -2.6, 0])
        self.play(FadeIn(concl, shift=UP * 0.2), run_time=0.9 * TS)
        self.add(self.note("Mr. Bones has a cartoon skull (bigger): air drag was estimated for a real human skull."))
        self.wait_s(P_READ)


# ==================================================================== A8 · synthesis
class A8Sintesis(Lesson):
    NUM, TITLE, SUB = "08", "Summary", "Fix the axis, identify v₀, keep the signs"

    def body(self):
        cards = [
            ("1 · AXIS", r"+y\ \text{up},\ y=0\ \text{at the ground}", C_POS),
            ("2 · DATA", r"y_0=45\ \mathrm{m},\ v_0\in\{0,-10,+10\}", C_VEL),
            ("3 · MODEL", r"y=y_0+v_0t-\tfrac12gt^2", C_POS),
            ("4 · GROUND", r"y=0\Rightarrow t\ (\text{positive root})", INK),
            ("5 · SPEED", r"v=v_0-gt,\ \ v^2=v_0^2+2gh", C_VEL),
        ]
        g = VGroup()
        for title, tex, col in cards:
            g.add(self.card(VGroup(T(title, 24, col, BOLD), M(tex, 30, INK)).arrange(DOWN, buff=0.15), stroke=col, width=5.6))
        g.arrange_in_grid(rows=2, cols=3, buff=(0.4, 0.4)).move_to([0, 0.75, 0])
        fit(g, 15)
        arrows = VGroup(*[Arrow(g[i].get_right(), g[i + 1].get_left(), buff=0.08, color=MUTED, stroke_width=3) for i in (0, 1, 3)])
        for i, c in enumerate(g):
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.6 * TS)
            if i in (0, 1, 3):
                self.play(GrowArrow(arrows[(0, 1, 3).index(i)]), run_time=0.3 * TS)
            self.wait_s(P_BEAT)
        res = self.card(VGroup(
            T(f"RESULTS (g = {num(G,2)} m/s², no air)", 24, C_GAL, BOLD),
            M(rf"t_1\approx{num(CASES['1']['T'],2)}\ \mathrm{{s}},\ |v_1|\approx{num(CASES['1']['speed_impact'],1)}\qquad t_2\approx{num(CASES['2']['T'],2)}\ \mathrm{{s}},\ |v_2|\approx{num(CASES['2']['speed_impact'],1)}\qquad t_3\approx{num(CASES['3']['T'],2)}\ \mathrm{{s}},\ |v_3|\approx{num(CASES['3']['speed_impact'],1)}\ \mathrm{{m/s}}", 30, INK),
        ).arrange(DOWN, buff=0.15), stroke=C_GAL).move_to([0, -2.35, 0])
        fit(res, 15)
        self.play(FadeIn(res), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        chk = self.card(VGroup(T("LAB CHECKLIST", 22, INK, BOLD), T("☐ axis and signs written   ☐ units in every term   ☐ positive root   ☐ any air? estimate v_terminal", 22, INK)).arrange(DOWN, buff=0.12))
        fit(chk, 15).move_to([0, -3.65, 0])
        self.play(FadeIn(chk), run_time=0.6 * TS)
        self.wait_s(P_LONG)
        close = T("Same gravity, same equation: the sign of v₀ decides the story.", 34, INK, BOLD)
        fit(close, 14.5)
        self.play(*[FadeOut(m) for m in [g, arrows, res, chk]], run_time=0.7 * TS)
        self.play(FadeIn(close, scale=0.96), run_time=0.9 * TS)
        self.wait_s(P_LONG)


SECTIONS = ["A1Pregunta", "A2NumerosPrimero", "A3Ecuacion", "A4Honda", "A5TresCasos", "A6PuntoAlto", "A7Excepciones", "A8Sintesis"]
