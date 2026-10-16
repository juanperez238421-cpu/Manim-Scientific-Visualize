"""Física 9 · Caída libre desde 45 m con Mr. Bones — lección ManimCE (motor A del video híbrido).

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
    return s.replace(".", ",")


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
        t = T("PAUSA · PREDICE", 26, C_ACC, BOLD)
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


# ==================================================================== A1 · question + convention
class A1Pregunta(Lesson):
    NUM, TITLE, SUB = "01", "La pregunta", "Una cabeza, un edificio de 45 m y tres maneras de soltarla"

    def body(self):
        hgt, y0, x = 5.3, -3.75, -5.6
        bld = self.building(x, y0, hgt)
        s = hgt / H
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
        conv = self.info_box("CONVENCIÓN DE SIGNOS (la fijamos antes de calcular)", [
            T("Eje +y hacia arriba; el origen y = 0 está en el suelo.", 24),
            T("Lo que sube tiene v > 0; lo que baja, v < 0.", 24),
            VGroup(T("La gravedad apunta hacia abajo:", 24), M(r"a=-g=-10\ \mathrm{m/s^2}", 34, C_ACC)).arrange(RIGHT, buff=0.2),
            T("Sin aire: la cabeza es una partícula (su centro de masa).", 22, MUTED),
        ], maxw=9.6).move_to([2.6, 1.15, 0])
        self.play(FadeIn(conv, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        q = self.info_box("LA PREGUNTA", [
            T("Desde 45 m: ¿cuánto tarda la cabeza en llegar al suelo", 26),
            T("y con qué rapidez llega, si...", 26),
            VGroup(T("1) se suelta", 26, INK), M(r"(v_0=0)", 32, C_VEL)).arrange(RIGHT, buff=0.15),
            VGroup(T("2) se lanza hacia abajo", 26), M(r"(v_0=-10\ \mathrm{m/s})", 32, C_VEL)).arrange(RIGHT, buff=0.15),
            VGroup(T("3) se lanza hacia arriba", 26), M(r"(v_0=+10\ \mathrm{m/s})", 32, C_VEL)).arrange(RIGHT, buff=0.15),
        ], maxw=9.6).move_to([2.6, -2.15, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        self.play(FadeOut(conv), FadeOut(q), run_time=0.7 * TS)
        pb = self.predict_box([
            "¿Cuál llega primero al suelo?",
            "¿Cuál llega con más rapidez?",
            "¿La 2 y la 3 llegan igual de rápido?",
        ]).move_to([2.6, 0, 0])
        self.play(FadeIn(pb, scale=0.96), run_time=0.8 * TS)
        # 5-second countdown
        for k in range(5, 0, -1):
            c = T(str(k), 40, C_ACC, BOLD).next_to(pb, DOWN, buff=0.3)
            self.add(c)
            self.wait_s(1.0)
            self.remove(c)
        self.add(self.note("Primero miramos el fenómeno (caso 1); los números vienen después."))
        self.wait_s(P_SHORT)


# ==================================================================== A2 · numbers first
class A2NumerosPrimero(Lesson):
    NUM, TITLE, SUB = "02", "Números primero", "Lo que midió el estroboscopio del caso 1, segundo a segundo"

    def body(self):
        nf = D["numbers_first"]
        rows = [("t (s)", [str(t) for t in nf["t"]], INK),
                ("y (m)", [fmt(H - d, 0) for d in nf["drop"]], C_POS),
                ("caída (m)", [fmt(d, 0) for d in nf["drop"]], C_POS),
                ("v (m/s)", [fmt(-v, 0) for v in nf["v"]], C_VEL)]
        cw, rh = 1.4, 1.05
        x0, y0 = -7.3, 2.1
        grid = VGroup()
        cells = {}
        for r, (lab, vals, col) in enumerate(rows):
            y = y0 - r * rh
            grid.add(T(lab, 26, col, BOLD).move_to([x0 + 1.0, y, 0]))
            for c, v in enumerate(vals):
                m = T(v, 30, col).move_to([x0 + 2.6 + c * cw, y, 0])
                cells[(r, c)] = m
                grid.add(m)
        lines = VGroup(*[Line([x0, y0 - (r + 0.5) * rh, 0], [x0 + 2.6 + 3.5 * cw, y0 - (r + 0.5) * rh, 0], color=RULE, stroke_width=1.5) for r in range(4)])
        self.play(FadeIn(lines), *[FadeIn(grid[k]) for k in range(len(grid)) if k % 5 == 0], run_time=0.8 * TS)
        for c in range(4):
            self.play(*[FadeIn(cells[(r, c)], shift=DOWN * 0.1) for r in range(4)], run_time=0.55 * TS)
        self.wait_s(P_MED)
        # increments of the drop: 5, 15, 25 -> 1 : 3 : 5
        incr = nf["increments"]
        braces = VGroup()
        for i, d in enumerate(incr):
            a, b = cells[(2, i)], cells[(2, i + 1)]
            br = ArcBetweenPoints(a.get_bottom() + DOWN * 0.15, b.get_bottom() + DOWN * 0.15, angle=PI / 2.4, color=C_VEL, stroke_width=3)
            lab = M(rf"+{fmt(d, 0)}", 30, C_VEL).next_to(br, DOWN, buff=0.05)
            braces.add(VGroup(br, lab))
        self.play(LaggedStart(*[Create(b) for b in braces], lag_ratio=0.4), run_time=1.6 * TS)
        ratio = self.info_box("CADA SEGUNDO CAE MÁS", [M(r"5 : 15 : 25 \;=\; 1 : 3 : 5", 40, C_VEL), T("números impares: la rapidez crece de forma pareja", 24)], maxw=6.6).move_to([3.95, 2.05, 0])
        self.play(FadeIn(ratio), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        # velocity: changes by the same amount each second -> acceleration
        dv = VGroup()
        for i in range(3):
            a, b = cells[(3, i)], cells[(3, i + 1)]
            arc = ArcBetweenPoints(a.get_bottom() + DOWN * 0.15, b.get_bottom() + DOWN * 0.15, angle=PI / 2.4, color=C_ACC, stroke_width=3)
            dv.add(VGroup(arc, M(r"-10", 28, C_ACC).next_to(arc, DOWN, buff=0.05)))
        self.play(LaggedStart(*[Create(b) for b in dv], lag_ratio=0.4), run_time=1.4 * TS)
        acc = self.info_box("LA VELOCIDAD CAMBIA LO MISMO CADA SEGUNDO", [M(r"a=\frac{\Delta v}{\Delta t}=\frac{-10\ \mathrm{m/s}}{1\ \mathrm{s}}=-10\ \mathrm{m/s^2}", 38, C_ACC)], maxw=6.4).move_to([3.9, -0.3, 0])
        self.play(FadeIn(acc), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        # average speed -> the drop law
        avg = nf["avg_speed"]
        txt = self.info_box("RAPIDEZ MEDIA EN CADA SEGUNDO", [
            M(rf"\frac{{5\ \mathrm{{m}}}}{{1\ \mathrm{{s}}}}={fmt(avg[0],0)},\quad \frac{{15}}{{1}}={fmt(avg[1],0)},\quad \frac{{25}}{{1}}={fmt(avg[2],0)}\ \mathrm{{m/s}}", 32, C_VEL),
            T("= la rapidez a mitad de cada segundo (0,5 s; 1,5 s; 2,5 s)", 22, MUTED),
            M(r"\text{caída}=\bar v\,t=\frac{0+g t}{2}\,t=\tfrac12 g t^2", 36, C_POS),
        ], maxw=8.4).move_to([3.4, -2.55, 0])
        self.play(FadeOut(ratio), acc.animate.move_to([3.9, 2.0, 0]), run_time=0.8 * TS)
        self.play(FadeIn(txt, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        res = self.card(M(r"y=45-5t^2", 54, C_POS), stroke=C_GAL).move_to([-4.4, -3.2, 0])
        self.play(FadeIn(res, scale=0.95), run_time=0.9 * TS)
        self.add(self.note("Comprobación: y(3) = 45 − 5·9 = 0 → la cabeza llega al suelo a los 3 s."))
        self.wait_s(P_LONG)


# ==================================================================== A3 · the equation term by term
class A3Ecuacion(Lesson):
    NUM, TITLE, SUB = "03", "La ecuación, término a término", "Un solo modelo para los tres casos"

    def body(self):
        eq = MathTex(r"y", r"=", r"y_0", r"+", r"v_0\,t", r"-", r"\tfrac12\,g\,t^2", font_size=88 * TXT_SCALE, color=INK).move_to([0, 2.0, 0])
        self.play(Write(eq), run_time=1.6 * TS)
        self.wait_s(P_SHORT)
        expl = [
            (0, C_POS, "y: posición en el instante t (metros, medida desde el suelo)"),
            (2, C_POS, "y₀ = 45 m: la altura de donde sale (positiva: está arriba)"),
            (4, C_VEL, "v₀·t: lo que avanzaría si no hubiera gravedad (signo de v₀: + sube, − baja)"),
            (6, C_ACC, "−½ g t²: lo que la gravedad la hace caer; siempre hacia abajo (−)"),
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
        vb = self.card(T("La velocidad pierde 10 m/s cada segundo (o gana 10 m/s hacia abajo).", 26, INK), stroke=RULE).move_to([0, -0.85, 0])
        self.play(FadeIn(vb), run_time=0.7 * TS)
        self.wait_s(P_LONG)
        # units check
        u = self.info_box("COMPROBACIÓN DE UNIDADES", [
            M(r"[y]=\mathrm{m}\qquad [v_0\,t]=\frac{\mathrm{m}}{\mathrm{s}}\cdot\mathrm{s}=\mathrm{m}\qquad [g\,t^2]=\frac{\mathrm{m}}{\mathrm{s}^2}\cdot\mathrm{s}^2=\mathrm{m}", 36, INK),
            T("Todos los términos son metros: la ecuación es coherente.", 24, C_GAL),
        ], maxw=13.5, stroke=C_GAL).move_to([0, -2.45, 0])
        self.play(FadeIn(u, shift=UP * 0.2), run_time=0.9 * TS)
        self.add(self.note("Con g = 10 m/s²: y = 45 + v₀t − 5t² y v = v₀ − 10t."))
        self.wait_s(P_READ)


# ==================================================================== A4 · the sling
class A4Honda(Lesson):
    NUM, TITLE, SUB = "04", "La honda de Mr. Bones", "Movimiento circular que termina en un lanzamiento vertical"

    def body(self):
        sl = D["sling"]
        R, w = sl["R"], sl["omega"]
        sc = 3.4  # scene units per metre (schematic of the sling)
        C = np.array([-3.3, -0.3, 0])
        circ = DashedVMobject(Circle(R * sc, color=C_POS, stroke_width=3), num_dashes=48).move_to(C)
        cdot = Dot(C, color=C_POS, radius=0.08)
        clab = T("C (mano derecha, fija)", 22, C_POS).next_to(cdot, LEFT, buff=0.15).shift(UP * 0.25)
        th = ValueTracker(-PI / 2)
        arm = always_redraw(lambda: Line(C, C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0]), color=STROKE, stroke_width=9))
        skull = always_redraw(lambda: Circle(0.22, color=INK, fill_color=BG, fill_opacity=1, stroke_width=3).move_to(C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0])))
        vel = always_redraw(lambda: Arrow(C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0]),
                                         C + R * sc * np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0]) + 1.25 * np.array([-math.sin(th.get_value()), math.cos(th.get_value()), 0]),
                                         buff=0.22, color=C_VEL, stroke_width=6))
        rlab = M(rf"R={fmt(R,3)}\ \mathrm{{m}}", 32, C_POS).move_to(C + np.array([R * sc * 0.5, 0.3, 0]))
        self.play(Create(circ), FadeIn(cdot), FadeIn(clab), run_time=1.2 * TS)
        self.add(arm, skull)
        self.play(FadeIn(rlab), run_time=0.5 * TS)
        self.add(vel)
        info = self.info_box("LA VELOCIDAD ES TANGENTE AL CÍRCULO", [
            M(r"v=\omega\,R", 44, C_VEL),
            T("ω: rapidez angular (rad/s); R: radio (m)", 22, MUTED),
        ], maxw=6.6).move_to([3.9, 2.0, 0])
        self.play(FadeIn(info), run_time=0.8 * TS)
        self.play(th.animate.set_value(-PI / 2 + 2 * PI), run_time=2.6 * TS, rate_func=rate_functions.ease_in_quad)
        self.play(th.animate.set_value(-PI / 2 + 4 * PI), run_time=1.3 * TS, rate_func=linear)
        # where the radius is horizontal, the velocity is vertical
        self.play(th.animate.set_value(4 * PI), run_time=0.45 * TS, rate_func=linear)
        mark = Line(C, C + RIGHT * R * sc, color=C_GAL, stroke_width=6)
        ml = T("radio horizontal → velocidad vertical", 24, C_GAL).next_to(circ, DOWN, buff=0.3)
        self.play(Create(mark), FadeIn(ml), run_time=0.8 * TS)
        self.wait_s(P_MED)
        need = self.info_box("PARA SALIR A 10 m/s", [
            M(rf"\omega=\frac{{v_0}}{{R}}=\frac{{10\ \mathrm{{m/s}}}}{{{fmt(R,3)}\ \mathrm{{m}}}}\approx {fmt(w,1)}\ \mathrm{{rad/s}}", 38, INK),
            M(rf"\approx {fmt(sl['rev_per_s'],2)}\ \text{{vueltas/s}}", 34, MUTED),
            M(rf"a_c=\omega^2R\approx {fmt(sl['centripetal_acc'],0)}\ \mathrm{{m/s^2}}\approx {fmt(sl['centripetal_in_g'],1)}\,g", 36, C_ACC),
        ], maxw=6.6).move_to([3.9, -0.65, 0])
        self.play(FadeIn(need, shift=UP * 0.15), run_time=0.9 * TS)
        self.wait_s(P_READ)
        # release: from now on only gravity (free fall); counter-clockwise -> up, clockwise -> down
        up = Arrow(C + RIGHT * R * sc, C + RIGHT * R * sc + UP * 1.7, buff=0.22, color=C_VEL, stroke_width=8)
        dn = Arrow(C + RIGHT * R * sc, C + RIGHT * R * sc + DOWN * 1.7, buff=0.22, color=C_VEL, stroke_width=8)
        self.remove(vel)
        self.play(GrowArrow(up), run_time=0.6 * TS)
        lab = VGroup(T("antihorario: sale hacia arriba (caso 3)", 24, C_VEL), T("horario: sale hacia abajo (caso 2)", 24, C_VEL)).arrange(DOWN, aligned_edge=LEFT).move_to([3.9, -3.0, 0])
        self.play(FadeIn(lab[0]), run_time=0.5 * TS)
        self.play(GrowArrow(dn), FadeIn(lab[1]), run_time=0.6 * TS)
        self.add(self.note("Al soltarla ya no hay fuerza de la honda: sólo la gravedad. Desde ahí es caída libre."))
        self.wait_s(P_READ)


# ==================================================================== A5 · three cases, one equation
class A5TresCasos(Lesson):
    NUM, TITLE, SUB = "05", "Tres casos, una ecuación", "Mismo reloj, misma gravedad: sólo cambia v₀"

    def body(self):
        hgt, y0 = 4.9, -3.75
        s = hgt / 52.0
        xs = [-6.3, -4.6, -2.9]
        t = ValueTracker(0.0)
        ground = Line([-7.3, y0, 0], [-1.9, y0, 0], color=INK, stroke_width=3)
        top = DashedLine([-7.3, y0 + 45 * s, 0], [-1.9, y0 + 45 * s, 0], color=C_POS, stroke_width=2)
        tl = M(r"45\ \mathrm{m}", 26, C_POS).next_to(top, LEFT, buff=0.08).shift(RIGHT * 0.9 + UP * 0.2)
        apex = DashedLine([-3.4, y0 + 50 * s, 0], [-2.4, y0 + 50 * s, 0], color=C_POS, stroke_width=2)
        self.play(Create(ground), Create(top), FadeIn(tl), run_time=0.8 * TS)
        heads = VGroup()
        for i, k in enumerate(["1", "2", "3"]):
            c = CASES[k]
            col_lab = T(f"caso {k}", 24, INK, BOLD).move_to([xs[i], y0 + 52 * s + 0.35, 0])

            def ypos(c=c):
                tt = min(t.get_value(), c["T"])
                return y0 + s * (H + c["v0"] * tt - 0.5 * G * tt * tt)

            dot = always_redraw(lambda x=xs[i], ypos=ypos: Circle(0.15, color=INK, fill_color=BG, fill_opacity=1, stroke_width=3).move_to([x, ypos(), 0]))
            heads.add(col_lab)
            self.add(dot)
        self.play(FadeIn(heads), Create(apex), run_time=0.6 * TS)
        state = always_redraw(lambda: self.card(M(rf"t={fmt(t.get_value(),2)}\ \mathrm{{s}}", 40, INK), width=3.2).move_to([-4.6, 2.2, 0]))
        self.add(state)
        self.play(t.animate.set_value(CASES["3"]["T"]), run_time=CASES["3"]["T"] * 1.0 * TS, rate_func=linear)
        self.wait_s(P_SHORT)
        # substitution, variable by variable, each case
        rows = []
        for k in ["1", "2", "3"]:
            c = CASES[k]
            v0 = c["v0"]
            sign = "+" if v0 > 0 else "-"
            if k == "1":
                l1 = r"0=45+0\cdot t-5t^2"
                l2 = r"t^2=9\;\Rightarrow\;t=3\ \mathrm{s}"
            elif k == "2":
                l1 = r"0=45-10t-5t^2"
                l2 = r"t^2+2t-9=0\;\Rightarrow\;t=-1+\sqrt{10}"
            else:
                l1 = r"0=45+10t-5t^2"
                l2 = r"t^2-2t-9=0\;\Rightarrow\;t=1+\sqrt{10}"
            res = rf"t\approx{fmt(c['T'],2)}\ \mathrm{{s}},\quad v={fmt(v0,0)}-10\,({fmt(c['T'],2)})\approx{fmt(c['v_impact'],1)}\ \mathrm{{m/s}}"
            rows.append((k, l1, l2, res))
        panel = VGroup()
        for i, (k, l1, l2, res) in enumerate(rows):
            g = VGroup(T(f"Caso {k}", 26, INK, BOLD), M(l1, 34, C_POS), M(l2, 34, INK), M(res, 32, C_VEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            panel.add(g)
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(panel, 8.2, 5.7)
        panel.move_to([3.2, -0.75, 0])
        for g in panel:
            self.play(FadeIn(g[0]), Write(g[1]), run_time=0.9 * TS)
            self.wait_s(P_SHORT)
            self.play(Write(g[2]), run_time=0.9 * TS)
            self.wait_s(P_SHORT)
            self.play(FadeIn(g[3], shift=RIGHT * 0.1), run_time=0.7 * TS)
            self.wait_s(P_MED)
        quad = self.card(M(r"t=\frac{-b+\sqrt{b^2-4ac}}{2a}\quad(\text{raíz positiva})", 30, MUTED)).move_to([4.6, 2.35, 0])
        self.play(FadeIn(quad), run_time=0.6 * TS)
        self.wait_s(P_LONG)


# ==================================================================== A6 · top point, symmetry, time-free
class A6PuntoAlto(Lesson):
    NUM, TITLE, SUB = "06", "El punto más alto y la simetría", "Caso 3: v = 0 por un instante, pero la gravedad no se apaga"

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
        al = self.card(M(rf"t={fmt(c3['t_apex'],0)}\ \mathrm{{s}}:\ v=0", 30, C_ACC), stroke=C_ACC).next_to(apex, UR, buff=0.2)
        self.play(FadeIn(apex), FadeIn(al), run_time=0.7 * TS)
        mis = self.info_box("ERROR FRECUENTE", [T("“Arriba v = 0, entonces a = 0”: FALSO.", 26, C_ACC),
                                                 M(r"a=\frac{\Delta v}{\Delta t}=-10\ \mathrm{m/s^2}\ \text{siempre (pendiente constante)}", 32, C_ACC),
                                                 T("Si a fuera 0 en la cima, se quedaría flotando.", 22, MUTED)], maxw=7.2, stroke=C_ACC).move_to([4.1, 1.7, 0])
        self.play(FadeIn(mis), run_time=0.9 * TS)
        self.wait_s(P_READ)
        ym = self.info_box("ALTURA MÁXIMA", [M(rf"y_{{max}}=45+\frac{{v_0^2}}{{2g}}=45+\frac{{100}}{{20}}={fmt(c3['y_apex'],0)}\ \mathrm{{m}}", 34, C_POS)], maxw=7.2).move_to([4.1, -0.25, 0])
        self.play(FadeIn(ym), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        sym = Dot(ax.c2p(c3["t_back"], c3["v_back"]), color=C_VEL, radius=0.1)
        syl = self.card(M(rf"t={fmt(c3['t_back'],0)}\ \mathrm{{s}}:\ y=45\ \mathrm{{m}},\ v={fmt(c3['v_back'],0)}\ \mathrm{{m/s}}", 28, C_VEL)).next_to(sym, DL, buff=0.2)
        self.play(FadeIn(sym), FadeIn(syl), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        tf = self.info_box("RELACIÓN SIN TIEMPO", [
            M(r"v^2=v_0^2+2gh", 40, INK),
            M(r"(\pm10)^2+2(10)(45)=1000", 32, C_VEL),
            M(rf"|v|=\sqrt{{1000}}\approx{fmt(c2['speed_impact'],1)}\ \mathrm{{m/s}}", 32, C_VEL),
            T("Casos 2 y 3: mismo v₀², misma rapidez al llegar; tiempos distintos.", 24, C_GAL),
        ], maxw=7.6, stroke=C_GAL).move_to([4.0, -1.2, 0])
        self.play(FadeOut(mis), ym.animate.move_to([4.1, 2.3, 0]), run_time=0.7 * TS)
        self.play(FadeIn(tf, shift=UP * 0.2), run_time=0.9 * TS)
        self.wait_s(P_READ)


# ==================================================================== A7 · real-world exceptions
class A7Excepciones(Lesson):
    NUM, TITLE, SUB = "07", "Excepciones del mundo real", "Lo que cambia con g = 9,81 m/s² y con aire"

    def body(self):
        real, drag = D["real_g"], D["drag"]
        hdr = ["", "caso 1", "caso 2", "caso 3"]
        data = [
            ("g = 10 (ideal)", [CASES[k]["T"] for k in "123"], [CASES[k]["speed_impact"] for k in "123"], INK),
            ("g = 9,81 (ideal)", [real[k]["T"] for k in "123"], [real[k]["speed_impact"] for k in "123"], C_POS),
            ("g = 9,81 + aire*", [drag["cases"][k]["T"] for k in "123"], [-drag["cases"][k]["v_impact"] for k in "123"], C_ACC),
        ]
        x0, y0, cw, rh = -7.4, 2.15, 3.45, 0.95
        tab = VGroup()
        for c, h in enumerate(hdr):
            tab.add(T(h, 26, INK, BOLD).move_to([x0 + 1.3 + c * cw, y0, 0]))
        for r, (lab, Ts, Vs, col) in enumerate(data):
            y = y0 - (r + 1) * rh
            tab.add(T(lab, 24, col, BOLD).move_to([x0 + 1.3, y, 0]))
            for c in range(3):
                tab.add(M(rf"{fmt(Ts[c],2)}\ \mathrm{{s}}\ \cdot\ {fmt(Vs[c],1)}\ \mathrm{{m/s}}", 28, col).move_to([x0 + 1.3 + (c + 1) * cw, y, 0]))
        lines = VGroup(*[Line([x0, y0 - (r + 0.5) * rh, 0], [x0 + 1.3 + 3.5 * cw, y0 - (r + 0.5) * rh, 0], color=RULE, stroke_width=1.5) for r in range(4)])
        self.play(FadeIn(lines), FadeIn(tab[:4]), run_time=0.8 * TS)
        for r in range(3):
            self.play(FadeIn(tab[4 + r * 4: 8 + r * 4], shift=RIGHT * 0.1), run_time=0.8 * TS)
            self.wait_s(P_MED)
        a = CST["air"]
        model = self.info_box("*MODELO DE AIRE (estimación para un cráneo real)", [
            M(r"F_d=\tfrac12\,\rho\,C_d\,A\,v^2", 36, C_ACC),
            M(rf"\rho={fmt(a['rho'],1)}\ \mathrm{{kg/m^3}},\ C_d={fmt(a['Cd'],1)},\ m={fmt(a['mass_kg'],1)}\ \mathrm{{kg}},\ d={fmt(a['diameter_m'],2)}\ \mathrm{{m}}", 28, INK),
            M(rf"v_{{\text{{terminal}}}}=\sqrt{{\frac{{2mg}}{{\rho C_d A}}}}\approx{fmt(drag['v_terminal'],1)}\ \mathrm{{m/s}}", 32, C_ACC),
            T("Integración numérica RK4 (dt = 10 µs); el caso 1 coincide con la solución exacta.", 22, MUTED),
        ], maxw=9.4, stroke=C_ACC).move_to([-2.6, -2.6, 0])
        self.play(FadeIn(model, shift=UP * 0.2), run_time=1.0 * TS)
        self.wait_s(P_READ)
        concl = self.info_box("QUÉ SE CONCLUYE", [
            T("Con g = 9,81 los tiempos crecen ~1%.", 24),
            T("Con aire llega más tarde y más lento,", 24),
            T("y los casos 2 y 3 ya no llegan igual de rápido.", 24, C_ACC),
            T("El modelo ideal es la base; el aire es la corrección.", 24, C_GAL),
        ], maxw=5.6, stroke=C_GAL).move_to([5.05, -2.6, 0])
        self.play(FadeIn(concl, shift=UP * 0.2), run_time=0.9 * TS)
        self.add(self.note("Mr. Bones tiene un cráneo de caricatura (más grande): el aire se estimó para un cráneo humano real."))
        self.wait_s(P_READ)


# ==================================================================== A8 · synthesis
class A8Sintesis(Lesson):
    NUM, TITLE, SUB = "08", "Síntesis", "Fija el eje, identifica v₀, conserva los signos"

    def body(self):
        cards = [
            ("1 · EJE", r"+y\ \text{arriba},\ y=0\ \text{en el suelo}", C_POS),
            ("2 · DATOS", r"y_0=45\ \mathrm{m},\ v_0\in\{0,-10,+10\}", C_VEL),
            ("3 · MODELO", r"y=y_0+v_0t-\tfrac12gt^2", C_POS),
            ("4 · SUELO", r"y=0\Rightarrow t\ (\text{raíz positiva})", INK),
            ("5 · RAPIDEZ", r"v=v_0-gt,\ \ v^2=v_0^2+2gh", C_VEL),
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
            T("RESULTADOS (g = 10 m/s², sin aire)", 24, C_GAL, BOLD),
            M(rf"t_1=3{{,}}00\ \mathrm{{s}},\ |v_1|=30{{,}}0\qquad t_2\approx{fmt(CASES['2']['T'],2)}\ \mathrm{{s}},\ |v_2|\approx{fmt(CASES['2']['speed_impact'],1)}\qquad t_3\approx{fmt(CASES['3']['T'],2)}\ \mathrm{{s}},\ |v_3|\approx{fmt(CASES['3']['speed_impact'],1)}\ \mathrm{{m/s}}", 30, INK),
        ).arrange(DOWN, buff=0.15), stroke=C_GAL).move_to([0, -2.35, 0])
        fit(res, 15)
        self.play(FadeIn(res), run_time=0.8 * TS)
        self.wait_s(P_LONG)
        chk = self.card(VGroup(T("CHECKLIST DE LABORATORIO", 22, INK, BOLD), T("☐ eje y signos escritos   ☐ unidades en cada término   ☐ raíz positiva   ☐ ¿hay aire? estima v_terminal", 22, INK)).arrange(DOWN, buff=0.12))
        fit(chk, 15).move_to([0, -3.65, 0])
        self.play(FadeIn(chk), run_time=0.6 * TS)
        self.wait_s(P_LONG)
        close = T("Misma gravedad, misma ecuación: el signo de v₀ decide la historia.", 34, INK, BOLD)
        fit(close, 14.5)
        self.play(*[FadeOut(m) for m in [g, arrows, res, chk]], run_time=0.7 * TS)
        self.play(FadeIn(close, scale=0.96), run_time=0.9 * TS)
        self.wait_s(P_LONG)


SECTIONS = ["A1Pregunta", "A2NumerosPrimero", "A3Ecuacion", "A4Honda", "A5TresCasos", "A6PuntoAlto", "A7Excepciones", "A8Sintesis"]
