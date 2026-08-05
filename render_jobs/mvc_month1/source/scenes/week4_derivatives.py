"""Week 4 — partial derivatives, tangent planes and gradient."""
from manim import *
import numpy as np
from mvc_manim_library import *


class W4_PartialDerivativeSlices(ThreeDScene):
    """Partial derivatives as slopes of coordinate-direction slices."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 4 · Escena 7", "Derivadas parciales como cortes", "Pendiente en x y pendiente en y")
        foot = footer()
        fixed_overlay(self, title, foot)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-45 * DEGREES, zoom=1.05)

        axes = standard_3d_axes().shift(DOWN * 0.35)
        f = lambda x, y: 0.28 * x**2 + 0.18 * y**2
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-2.3, 2.3],
            v_range=[-2.3, 2.3],
            resolution=(12, 12),
            checkerboard_colors=[CYAN, BLUE],
            fill_opacity=0.34,
            stroke_opacity=0.22,
        )
        x0, y0 = 1.2, 1.0
        z0 = f(x0, y0)
        point = Dot3D(axes.c2p(x0, y0, z0), radius=0.09, color=RED)
        x_slice = ParametricFunction(lambda t: axes.c2p(t, y0, f(t, y0)), t_range=[-2.2, 2.2], color=ORANGE, stroke_width=5)
        y_slice = ParametricFunction(lambda t: axes.c2p(x0, t, f(x0, t)), t_range=[-2.2, 2.2], color=GREEN, stroke_width=5)
        fx = 0.56 * x0
        fy = 0.36 * y0
        tx = ParametricFunction(lambda s: axes.c2p(x0 + s, y0, z0 + fx * s), t_range=[-1.0, 1.0], color=ORANGE, stroke_width=7)
        ty = ParametricFunction(lambda s: axes.c2p(x0, y0 + s, z0 + fy * s), t_range=[-1.0, 1.0], color=GREEN, stroke_width=7)
        card = equation_card(
            MathTex(r"f(x,y)=0.28x^2+0.18y^2", color=INK).scale(0.70),
            MathTex(fr"f_x({x0:g},{y0:g})={fx:.2f}", color=ORANGE).scale(0.70),
            MathTex(fr"f_y({x0:g},{y0:g})={fy:.2f}", color=GREEN).scale(0.70),
            width=5.2,
        ).to_corner(DL, buff=0.42)
        fixed_overlay(self, card)
        self.remove(card)

        self.play(Create(axes), FadeIn(surface), run_time=1.4)
        self.play(Create(x_slice), Create(y_slice), FadeIn(point), run_time=1.3)
        self.play(Create(tx), Create(ty), FadeIn(card, shift=UP * 0.2), run_time=1.1)
        self.move_camera(theta=10 * DEGREES, run_time=2.0)
        self.wait(1.3)


class W4_GradientAndTangentPlane(ThreeDScene):
    """Unify partial derivatives, the gradient and the tangent plane."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 4 · Escena 8", "Gradiente y plano tangente", "Máximo crecimiento y aproximación lineal")
        foot = footer("Cálculo de varias variables · Cierre del mes 1")
        fixed_overlay(self, title, foot)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-42 * DEGREES, zoom=1.04)

        axes = standard_3d_axes().shift(DOWN * 0.35)
        f = lambda x, y: 0.23 * x**2 + 0.16 * y**2
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-2.3, 2.3],
            v_range=[-2.3, 2.3],
            resolution=(12, 12),
            checkerboard_colors=[PURPLE, BLUE],
            fill_opacity=0.30,
            stroke_opacity=0.18,
        )
        x0, y0 = 1.1, 1.0
        z0 = f(x0, y0)
        gx, gy = 0.46 * x0, 0.32 * y0
        tangent = Surface(
            lambda u, v: axes.c2p(u, v, z0 + gx * (u - x0) + gy * (v - y0)),
            u_range=[-0.8, 2.8],
            v_range=[-0.8, 2.8],
            resolution=(2, 2),
            checkerboard_colors=[GREEN, GREEN],
            fill_opacity=0.28,
            stroke_color=GREEN,
            stroke_opacity=0.55,
        )
        point = Dot3D(axes.c2p(x0, y0, z0), radius=0.09, color=RED)
        gradient = Line3D(
            axes.c2p(x0, y0, z0),
            axes.c2p(x0 + gx * 2.0, y0 + gy * 2.0, z0),
            color=ORANGE,
            thickness=0.045,
        )
        card = equation_card(
            MathTex(r"\nabla f=\langle f_x,f_y\rangle", color=ORANGE).scale(0.76),
            MathTex(r"L(x,y)=f(a,b)+f_x(a,b)(x-a)+f_y(a,b)(y-b)", color=GREEN).scale(0.57),
            Text("El gradiente vive en el dominio; el plano tangente aproxima la superficie.", font_size=20, color=MUTED),
            width=7.2,
        ).to_corner(DL, buff=0.42)
        fixed_overlay(self, card)
        self.remove(card)

        self.play(Create(axes), FadeIn(surface), run_time=1.4)
        self.play(FadeIn(point), FadeIn(gradient), run_time=1.0)
        self.play(FadeIn(tangent), FadeIn(card, shift=UP * 0.2), run_time=1.1)
        self.move_camera(theta=22 * DEGREES, phi=74 * DEGREES, run_time=2.0)
        self.wait(1.5)
