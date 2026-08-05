"""Week 1 — vectors, components, dot product and projection."""
from manim import *
import numpy as np
from mvc_manim_library import *


class W1_VectorBridge2D3D(ThreeDScene):
    """Connect a 2D vector decomposition with its 3D interpretation."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 1 · Escena 1", "De vectores 2D a vectores 3D", "Componentes, magnitud y representación espacial")
        foot = footer()
        fixed_overlay(self, title, foot)

        plane = clean_number_plane().shift(DOWN * 0.35)
        a2 = np.array([3.0, 2.0, 0.0])
        arrow = vector2d(plane, a2, BLUE)
        guides = component_guides(plane, a2, BLUE)
        label = MathTex(r"\vec a=\langle 3,2\rangle", color=BLUE).scale(0.82).next_to(arrow.get_end(), UR, buff=0.18)
        mag = equation_card(
            MathTex(r"\|\vec a\|=\sqrt{3^2+2^2}=\sqrt{13}", color=INK).scale(0.75),
            width=5.4,
        ).to_corner(DL, buff=0.45)
        fixed_overlay(self, mag)
        self.remove(mag)

        self.play(Create(plane), run_time=1.2)
        self.play(GrowArrow(arrow), Create(guides), FadeIn(label, shift=UP * 0.15), run_time=1.4)
        self.play(FadeIn(mag, shift=UP * 0.2), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(plane), FadeOut(arrow), FadeOut(guides), FadeOut(label), FadeOut(mag), run_time=0.8)

        self.set_camera_orientation(phi=68 * DEGREES, theta=-45 * DEGREES, zoom=1.05)
        axes = standard_3d_axes().shift(DOWN * 0.35)
        a3 = (3.0, 2.0, 1.5)
        vector = line3d_from_origin(axes, a3, BLUE)
        endpoint = Dot3D(axes.c2p(*a3), radius=0.085, color=BLUE)
        xline = DashedLine(axes.c2p(0, 0, 0), axes.c2p(3, 0, 0), color=RED)
        yline = DashedLine(axes.c2p(3, 0, 0), axes.c2p(3, 2, 0), color=GREEN)
        zline = DashedLine(axes.c2p(3, 2, 0), axes.c2p(3, 2, 1.5), color=PURPLE)
        formula = equation_card(
            MathTex(r"\vec a=\langle 3,2,1.5\rangle", color=BLUE).scale(0.76),
            MathTex(r"\|\vec a\|=\sqrt{3^2+2^2+1.5^2}", color=INK).scale(0.68),
            width=5.6,
        ).to_corner(DL, buff=0.45)
        fixed_overlay(self, formula)
        self.remove(formula)

        self.play(Create(axes), run_time=1.2)
        self.play(Create(xline), Create(yline), Create(zline), Create(vector), FadeIn(endpoint), run_time=1.6)
        self.play(FadeIn(formula, shift=UP * 0.2), run_time=0.8)
        self.move_camera(theta=25 * DEGREES, run_time=2.0)
        self.wait(1.0)


class W1_DotProductProjection(Scene):
    """Geometric meaning of the dot product as a projection."""

    def construct(self):
        prepare_scene(self)
        title = title_group("Semana 1 · Escena 2", "Producto punto y proyección", "Ángulo, componente paralela y ortogonalidad")
        foot = footer()
        self.add(title, foot)

        plane = clean_number_plane(x_range=(-1, 7, 1), y_range=(-1, 6, 1), size=0.78).shift(LEFT * 2.7 + DOWN * 0.4)
        u = np.array([5.0, 1.5, 0.0])
        v = np.array([2.0, 4.0, 0.0])
        au = vector2d(plane, u, BLUE)
        av = vector2d(plane, v, ORANGE)
        lu = MathTex(r"\vec u", color=BLUE).scale(0.78).next_to(au.get_end(), RIGHT, buff=0.12)
        lv = MathTex(r"\vec v", color=ORANGE).scale(0.78).next_to(av.get_end(), UP, buff=0.12)
        angle = Angle(Line(plane.c2p(0, 0), plane.c2p(*u[:2])), Line(plane.c2p(0, 0), plane.c2p(*v[:2])), radius=0.7, color=PURPLE)
        theta = MathTex(r"\theta", color=PURPLE).scale(0.65).move_to(angle.point_from_proportion(0.5) + 0.2 * UP)

        projection = (np.dot(v[:2], u[:2]) / np.dot(u[:2], u[:2])) * u[:2]
        p_dot = Dot(plane.c2p(*projection), color=GREEN, radius=0.07)
        proj_line = Arrow(plane.c2p(0, 0), plane.c2p(*projection), color=GREEN, buff=0, stroke_width=6)
        orth = DashedLine(plane.c2p(*v[:2]), plane.c2p(*projection), color=MUTED)

        calc = equation_card(
            MathTex(r"\vec u\cdot\vec v=\|\vec u\|\,\|\vec v\|\cos\theta", color=INK).scale(0.72),
            MathTex(r"\operatorname{proj}_{\vec u}(\vec v)=\frac{\vec u\cdot\vec v}{\vec u\cdot\vec u}\vec u", color=GREEN).scale(0.68),
            Text("La proyección mide cuánto de v apunta en la dirección de u.", font_size=21, color=MUTED),
            width=6.6,
        ).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.25)

        self.play(Create(plane), run_time=1.0)
        self.play(GrowArrow(au), GrowArrow(av), FadeIn(lu), FadeIn(lv), run_time=1.2)
        self.play(Create(angle), FadeIn(theta), run_time=0.7)
        self.play(GrowArrow(proj_line), FadeIn(p_dot), Create(orth), run_time=1.2)
        self.play(FadeIn(calc, shift=LEFT * 0.2), run_time=0.9)
        self.wait(2.0)
