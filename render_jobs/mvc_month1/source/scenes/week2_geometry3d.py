"""Week 2 — cross product, lines and planes in three dimensions."""
from manim import *
import numpy as np
from mvc_manim_library import *


class W2_CrossProductArea(ThreeDScene):
    """Cross product as oriented area and plane normal."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 2 · Escena 3", "Producto cruz", "Área orientada y vector normal")
        foot = footer()
        fixed_overlay(self, title, foot)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-45 * DEGREES, zoom=1.05)

        axes = standard_3d_axes().shift(DOWN * 0.4)
        u = np.array([2.5, 0.8, 0.0])
        v = np.array([0.7, 2.4, 0.0])
        w = np.cross(u, v)
        au = line3d_from_origin(axes, tuple(u), BLUE)
        av = line3d_from_origin(axes, tuple(v), ORANGE)
        aw = line3d_from_origin(axes, (0, 0, float(w[2]) / 2.0), PURPLE)
        poly = Polygon(
            axes.c2p(0, 0, 0),
            axes.c2p(*u),
            axes.c2p(*(u + v)),
            axes.c2p(*v),
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.32,
            stroke_width=2.2,
        )
        card = equation_card(
            MathTex(r"\vec u\times\vec v=\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\2.5&0.8&0\\0.7&2.4&0\end{vmatrix}", color=INK).scale(0.58),
            MathTex(fr"\|\vec u\times\vec v\|={abs(w[2]):.2f}", color=GREEN).scale(0.76),
            Text("La magnitud es el área del paralelogramo.", font_size=21, color=MUTED),
            width=6.2,
        ).to_corner(DL, buff=0.42)
        fixed_overlay(self, card)
        self.remove(card)

        self.play(Create(axes), run_time=1.0)
        self.play(Create(au), Create(av), run_time=1.1)
        self.play(FadeIn(poly), run_time=0.8)
        self.play(Create(aw), FadeIn(card, shift=UP * 0.18), run_time=1.2)
        self.move_camera(theta=20 * DEGREES, run_time=2.0)
        self.wait(1.2)


class W2_LinesPlanesIntersection(ThreeDScene):
    """Parametric line intersecting an affine plane."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 2 · Escena 4", "Rectas y planos en el espacio", "Ecuaciones paramétricas, normal e intersección")
        foot = footer()
        fixed_overlay(self, title, foot)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-38 * DEGREES, zoom=1.03)

        axes = standard_3d_axes().shift(DOWN * 0.35)
        plane = Surface(
            lambda u, v: axes.c2p(u, v, 1.5 - 0.35 * u - 0.25 * v),
            u_range=[-2.4, 2.4],
            v_range=[-2.4, 2.4],
            resolution=(10, 10),
            checkerboard_colors=[BLUE, CYAN],
            fill_opacity=0.34,
            stroke_color=BLUE,
            stroke_opacity=0.35,
        )
        p0 = np.array([-2.2, -1.6, -0.8])
        d = np.array([1.0, 0.8, 0.95])
        p1 = p0 + 4.7 * d
        line = Line3D(axes.c2p(*p0), axes.c2p(*p1), color=ORANGE, thickness=0.035)

        numerator = 1.5 - 0.35 * p0[0] - 0.25 * p0[1] - p0[2]
        denominator = d[2] + 0.35 * d[0] + 0.25 * d[1]
        t_star = numerator / denominator
        point = p0 + t_star * d
        hit = Dot3D(axes.c2p(*point), radius=0.095, color=RED)
        normal = line3d_from_origin(axes, (0.7, 0.5, 2.0), PURPLE)

        card = equation_card(
            MathTex(r"\Pi:\;0.35x+0.25y+z=1.5", color=BLUE).scale(0.72),
            MathTex(r"\ell(t)=\vec p_0+t\vec d", color=ORANGE).scale(0.72),
            MathTex(fr"t^*={t_star:.2f}\quad\Rightarrow\quad \ell(t^*)\in\Pi", color=RED).scale(0.68),
            width=5.8,
        ).to_corner(DL, buff=0.42)
        fixed_overlay(self, card)
        self.remove(card)

        self.play(Create(axes), run_time=1.0)
        self.play(FadeIn(plane), run_time=1.1)
        self.play(Create(line), Create(normal), run_time=1.1)
        self.play(FadeIn(hit, scale=1.8), FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.move_camera(theta=15 * DEGREES, run_time=2.0)
        self.wait(1.1)
