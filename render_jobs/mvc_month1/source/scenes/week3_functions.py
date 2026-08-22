"""Week 3 — multivariable functions, level curves and limits."""
from manim import *
import numpy as np
from mvc_manim_library import *


class W3_SurfaceToContours(ThreeDScene):
    """Turn a graph z=f(x,y) into a family of level curves."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 3 · Escena 5", "Superficies y curvas de nivel", "Dos representaciones de la misma función")
        foot = footer()
        fixed_overlay(self, title, foot)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-45 * DEGREES, zoom=1.05)

        axes = standard_3d_axes().shift(DOWN * 0.35)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, 0.32 * (u**2 + v**2)),
            u_range=[-2.2, 2.2],
            v_range=[-2.2, 2.2],
            resolution=(12, 12),
            checkerboard_colors=[PURPLE, BLUE],
            fill_opacity=0.38,
            stroke_color=PURPLE,
            stroke_opacity=0.25,
        )
        levels = VGroup()
        for c, color in [(0.45, GREEN), (0.95, ORANGE), (1.55, RED)]:
            r = np.sqrt(c / 0.32)
            curve = ParametricFunction(
                lambda t, rr=r, cc=c: axes.c2p(rr * np.cos(t), rr * np.sin(t), cc),
                t_range=[0, TAU],
                color=color,
                stroke_width=4,
            )
            levels.add(curve)
        card = equation_card(
            MathTex(r"z=f(x,y)=0.32(x^2+y^2)", color=PURPLE).scale(0.72),
            MathTex(r"f(x,y)=c\quad\Longrightarrow\quad x^2+y^2=\frac{c}{0.32}", color=INK).scale(0.64),
            Text("Cada altura c produce una curva de nivel.", font_size=21, color=MUTED),
            width=6.2,
        ).to_corner(DL, buff=0.42)
        fixed_overlay(self, card)
        self.remove(card)

        self.play(Create(axes), FadeIn(surface), run_time=1.4)
        self.play(LaggedStart(*[Create(curve) for curve in levels], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.move_camera(phi=5 * DEGREES, theta=-90 * DEGREES, zoom=1.15, run_time=2.2)
        self.wait(1.3)


class W3_PathDependentLimit(Scene):
    """Show that two approach paths can produce different limiting values."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 3 · Escena 6", "Límites por caminos", "Una prueba visual de no existencia")
        foot = footer()
        self.add(title, foot)

        plane = clean_number_plane(x_range=(-4, 5, 1), y_range=(-4, 5, 1), size=0.78).shift(LEFT * 2.65 + DOWN * 0.35)
        path1 = plane.plot(lambda x: x, x_range=[-3.6, 3.6], color=BLUE, stroke_width=5)
        path2 = plane.plot(lambda x: -x, x_range=[-3.6, 3.6], color=ORANGE, stroke_width=5)
        origin = Dot(plane.c2p(0, 0), radius=0.09, color=RED)
        d1 = Dot(plane.c2p(3.2, 3.2), color=BLUE)
        d2 = Dot(plane.c2p(3.2, -3.2), color=ORANGE)
        l1 = MathTex(r"y=x", color=BLUE).scale(0.68).next_to(plane.c2p(2.5, 2.5), UL)
        l2 = MathTex(r"y=-x", color=ORANGE).scale(0.68).next_to(plane.c2p(2.5, -2.5), DL)

        card = equation_card(
            MathTex(r"f(x,y)=\frac{xy}{x^2+y^2}", color=INK).scale(0.78),
            MathTex(r"y=x\Rightarrow f(x,x)=\frac12", color=BLUE).scale(0.68),
            MathTex(r"y=-x\Rightarrow f(x,-x)=-\frac12", color=ORANGE).scale(0.68),
            MathTex(r"\therefore\;\lim_{(x,y)\to(0,0)}f(x,y)\;\text{no existe}", color=RED).scale(0.62),
            width=6.2,
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.22)

        self.play(Create(plane), run_time=1.0)
        self.play(Create(path1), Create(path2), FadeIn(l1), FadeIn(l2), FadeIn(d1), FadeIn(d2), run_time=1.2)
        self.play(d1.animate.move_to(origin), d2.animate.move_to(origin), run_time=2.2, rate_func=smooth)
        self.play(FadeIn(origin, scale=1.7), FadeIn(card, shift=LEFT * 0.2), run_time=0.9)
        self.wait(2.0)
