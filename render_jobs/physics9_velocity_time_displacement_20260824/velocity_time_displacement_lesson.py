#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9: velocity–time graphs and area as displacement.

Consolidates the audited Achilles/Zeno meeting model and the Position–Time
Graph QA V3 lesson into a new Week 2 presentation aligned to the Grade 9
third-period planning (24–28 August 2026).

Final render target:
    manim -pqh velocity_time_displacement_lesson.py \
        Physics9VelocityTimeDisplacement --format=mp4 --disable_caching
"""
from __future__ import annotations

from manim import *

from jp_classroom_style import (
    JPClassroomScene,
    BLACK_TEXT,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT_GRAY,
    PAPER_GRAY,
    RUN_QUICK,
    RUN_NORMAL,
    RUN_SLOW,
    PAUSE_SHORT,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_WORK,
    PAUSE_FINAL,
)


class Physics9VelocityTimeDisplacement(JPClassroomScene):
    """Complete Grade 9 graph lesson with numerical and layout validation."""

    V_A = 10.0
    V_T = 1.0
    LEAD = 10.0
    T_CATCH = 10.0 / 9.0
    X_CATCH = 100.0 / 9.0

    def validate_lesson_data(self) -> None:
        assert abs(self.T_CATCH - self.LEAD / (self.V_A - self.V_T)) < 1e-12
        assert abs(self.X_CATCH - self.V_A * self.T_CATCH) < 1e-12
        assert abs(self.X_CATCH - (self.LEAD + self.V_T * self.T_CATCH)) < 1e-12
        assert 4 * 2 + 2 * 3 == 14
        assert 2 * 3 + (-1) * 2 == 4
        assert 2 * 3 + abs(-1) * 2 == 8

    # ------------------------------------------------------------------
    # Reusable visual components
    # ------------------------------------------------------------------
    def card(self, title: str, body: str, width=4.35, height=2.10) -> VGroup:
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.13,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        title_mob = self.text(title, 27, BOLD)
        words = body.split()
        lines = []
        current = []
        for word in words:
            trial = " ".join(current + [word])
            if len(trial) > 30 and current:
                lines.append(" ".join(current))
                current = [word]
            else:
                current.append(word)
        if current:
            lines.append(" ".join(current))
        body_mob = VGroup(*[self.text(line, 22) for line in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06
        )
        content = VGroup(title_mob, body_mob).arrange(
            DOWN, aligned_edge=LEFT, buff=0.20
        )
        self.fit(content, width - 0.50, height - 0.42)
        content.move_to(box)
        return VGroup(box, content)

    def result_chip(self, expression: str, width=4.3, size=34) -> VGroup:
        box = RoundedRectangle(
            width=width, height=0.86, corner_radius=0.11,
            stroke_color=BLACK_LINE, stroke_width=2.0,
            fill_color=PAPER_GRAY, fill_opacity=1,
        )
        eq = self.math(expression, size)
        self.fit(eq, width - 0.35, 0.58)
        eq.move_to(box)
        return VGroup(box, eq)

    def x_t_axes(self, position=LEFT * 2.85 + DOWN * 0.55, scale=1.0) -> Axes:
        axes = Axes(
            x_range=[0, 1.25, 0.25],
            y_range=[0, 12.5, 2.5],
            x_length=7.0 * scale,
            y_length=4.65 * scale,
            tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2},
            x_axis_config={"numbers_to_include": [0, 0.5, 1.0], "font_size": 20},
            y_axis_config={"numbers_to_include": [0, 5, 10], "font_size": 20},
        ).move_to(position)
        return axes

    def v_t_axes(
        self,
        x_max=5,
        y_min=0,
        y_max=12,
        x_step=1,
        y_step=2,
        position=LEFT * 2.6 + DOWN * 0.55,
        x_length=7.6,
        y_length=4.65,
    ) -> Axes:
        return Axes(
            x_range=[0, x_max, x_step],
            y_range=[y_min, y_max, y_step],
            x_length=x_length,
            y_length=y_length,
            tips=False,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.2},
            x_axis_config={"include_numbers": True, "font_size": 20},
            y_axis_config={"include_numbers": True, "font_size": 20},
        ).move_to(position)

    def axis_labels(self, axes: Axes, y_symbol: str) -> VGroup:
        x_label = self.math(r"t\;(\mathrm{s})", 26).next_to(axes.x_axis, RIGHT, buff=0.12)
        y_label = self.math(y_symbol, 26).next_to(axes.y_axis, UP, buff=0.10)
        return VGroup(x_label, y_label)

    def graph_caption(self, text_value: str, position) -> VGroup:
        box = RoundedRectangle(
            width=5.15, height=0.66, corner_radius=0.09,
            stroke_color=MID_GRAY, stroke_width=1.3,
            fill_color=WHITE, fill_opacity=0.96,
        ).move_to(position)
        txt = self.text(text_value, 21, BOLD)
        self.fit(txt, 4.82, 0.42)
        txt.move_to(box)
        return VGroup(box, txt)

    # ------------------------------------------------------------------
    # Scene sequence
    # ------------------------------------------------------------------
    def opening(self) -> None:
        self.standard_opening(
            "PHYSICS 9 • THIRD PERIOD • WEEK 2",
            "FROM MEETING POINT TO DISPLACEMENT",
            "Position–time and velocity–time graphs",
            "We will connect slope, velocity and signed area step by step.",
        )

    def lesson_map(self) -> None:
        self.set_header(
            1, "TODAY'S MAP",
            "One physical event will be represented in two graphs and then used to calculate displacement.",
        )
        cards = VGroup(
            self.card("1  LOCATE", "Find the meeting on a position–time graph."),
            self.card("2  READ", "Use slope to identify each constant velocity."),
            self.card("3  CALCULATE", "Use signed area under a v–t graph."),
        ).arrange(RIGHT, buff=0.32).move_to(DOWN * 0.45)
        self.assert_content_safe(cards, "lesson-map cards")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.18), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        bridge = self.math(r"\text{motion}\;\longrightarrow\;x\!\! -\!\! t\;\longrightarrow\;v\!\! -\!\! t\;\longrightarrow\;\Delta x", 36)
        bridge.next_to(cards, DOWN, buff=0.45)
        self.play(Write(bridge), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.clear_stage()

    def consolidate_meeting(self) -> None:
        self.set_header(
            2, "CONSOLIDATE THE PHYSICAL MEETING",
            "Achilles moves at 10 m/s. The tortoise moves at 1 m/s and begins 10 m ahead.",
        )
        track = NumberLine(
            x_range=[0, 12, 2], length=12.1, include_numbers=True,
            font_size=21, color=BLACK_LINE, stroke_width=2.4,
        ).move_to(UP * 1.05)
        achilles = Dot(track.n2p(0) + UP * 0.38, radius=0.13, color=BLACK_LINE)
        tortoise = Dot(track.n2p(10) + DOWN * 0.30, radius=0.13, color=DARK_GRAY)
        a_label = self.text("ACHILLES", 21, BOLD).next_to(achilles, UP, buff=0.08)
        t_label = self.text("TORTOISE", 21, BOLD).next_to(tortoise, DOWN, buff=0.08)
        lead = DoubleArrow(track.n2p(0) + DOWN * 0.70, track.n2p(10) + DOWN * 0.70, buff=0.05, color=MID_GRAY)
        lead_label = self.math(r"\Delta x_0=10\,\mathrm{m}", 26).next_to(lead, DOWN, buff=0.10)
        eqs = VGroup(
            self.math(r"x_A(t)=10t", 34),
            self.math(r"x_T(t)=10+t", 34),
            self.math(r"10t=10+t", 36),
            self.math(r"9t=10\;\Rightarrow\;t^*=\frac{10}{9}\,\mathrm{s}", 36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT * 2.65 + DOWN * 2.03)
        results = VGroup(
            self.result_chip(r"t^*=\frac{10}{9}\,\mathrm{s}", 3.55, 32),
            self.result_chip(r"x^*=\frac{100}{9}\,\mathrm{m}", 3.95, 32),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.25 + DOWN * 2.05)
        self.play(Create(track), FadeIn(achilles), FadeIn(tortoise), Write(a_label), Write(t_label), run_time=RUN_NORMAL)
        self.play(GrowArrow(lead), Write(lead_label), run_time=RUN_NORMAL)
        for eq in eqs:
            self.play(Write(eq), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.45)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.12) for r in results], lag_ratio=0.18), run_time=RUN_SLOW)
        meet_x = track.n2p(self.X_CATCH)
        self.play(
            achilles.animate.move_to(meet_x + UP * 0.38),
            tortoise.animate.move_to(meet_x + DOWN * 0.30),
            run_time=3.6, rate_func=linear,
        )
        meet_line = DashedLine(meet_x + DOWN * 0.78, meet_x + UP * 0.85, color=MID_GRAY)
        self.play(Create(meet_line), run_time=RUN_QUICK)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def position_time_graph(self) -> None:
        self.set_header(
            3, "THE SAME MEETING ON AN x–t GRAPH",
            "A point on this graph pairs one time with one position. The intersection is the physical meeting.",
        )
        axes = self.x_t_axes(position=LEFT * 2.85 + DOWN * 0.56)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        a_graph = axes.plot(lambda t: 10 * t, x_range=[0, 1.22], color=BLACK_LINE, stroke_width=3.4)
        t_graph = axes.plot(lambda t: 10 + t, x_range=[0, 1.22], color=DARK_GRAY, stroke_width=3.4)
        a_tag = self.math(r"x_A=10t", 26).move_to(axes.c2p(0.68, 6.8) + RIGHT * 0.25)
        t_tag = self.math(r"x_T=10+t", 26).move_to(axes.c2p(0.50, 10.5) + UP * 0.28)
        meeting = axes.c2p(self.T_CATCH, self.X_CATCH)
        meet_dot = Dot(meeting, radius=0.10, color=BLACK_LINE)
        vline = DashedLine(axes.c2p(self.T_CATCH, 0), meeting, color=MID_GRAY, dash_length=0.08)
        hline = DashedLine(axes.c2p(0, self.X_CATCH), meeting, color=MID_GRAY, dash_length=0.08)
        callout = self.result_chip(r"\left(t^*,x^*\right)=\left(\frac{10}{9}\,\mathrm{s},\frac{100}{9}\,\mathrm{m}\right)", 5.2, 27)
        callout.move_to(RIGHT * 4.60 + UP * 1.18)
        interpretation = self.note_panel(
            "READ THE INTERSECTION",
            ["same horizontal coordinate → same time", "same vertical coordinate → same position", "therefore: the objects meet"],
            width=5.45, body_size=22,
        ).move_to(RIGHT * 4.55 + DOWN * 1.55)
        self.play(Create(axes), Write(labels), run_time=RUN_NORMAL)
        self.play(Create(a_graph), Write(a_tag), run_time=RUN_SLOW)
        self.play(Create(t_graph), Write(t_tag), run_time=RUN_SLOW)
        self.play(FadeIn(meet_dot), Create(vline), Create(hline), run_time=RUN_NORMAL)
        self.play(FadeIn(callout, shift=DOWN * 0.08), FadeIn(interpretation, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def slopes(self) -> None:
        self.set_header(
            4, "WHAT THE SLOPES SAY",
            "On a position–time graph, slope measures how much position changes during a time interval.",
        )
        axes = self.x_t_axes(position=LEFT * 3.35 + DOWN * 0.58)
        labels = self.axis_labels(axes, r"x\;(\mathrm{m})")
        a_graph = axes.plot(lambda t: 10 * t, x_range=[0, 1.20], color=BLACK_LINE, stroke_width=3.2)
        t_graph = axes.plot(lambda t: 10 + t, x_range=[0, 1.20], color=DARK_GRAY, stroke_width=3.2)
        tri_a = Polygon(axes.c2p(0, 0), axes.c2p(1, 0), axes.c2p(1, 10), color=BLACK_LINE, fill_opacity=0.05)
        tri_t = Polygon(axes.c2p(0, 10), axes.c2p(1, 10), axes.c2p(1, 11), color=MID_GRAY, fill_opacity=0.10)
        slope_formula = self.result_chip(r"\mathrm{slope}=\frac{\Delta x}{\Delta t}=v", 5.0, 35).move_to(RIGHT * 4.45 + UP * 1.20)
        calculations = VGroup(
            self.card("ACHILLES", "10 m in 1 s → 10 m/s", width=5.0, height=1.50),
            self.card("TORTOISE", "1 m in 1 s → 1 m/s", width=5.0, height=1.50),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 4.45 + DOWN * 1.35)
        self.play(Create(axes), Write(labels), Create(a_graph), Create(t_graph), run_time=RUN_SLOW)
        self.play(FadeIn(tri_a), FadeIn(tri_t), run_time=RUN_NORMAL)
        self.play(Write(slope_formula), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.10) for c in calculations], lag_ratio=0.22), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        key = self.graph_caption("steeper line → greater velocity", RIGHT * 4.45 + DOWN * 3.25)
        self.play(FadeIn(key), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.clear_stage()

    def velocity_time_height(self) -> None:
        self.set_header(
            5, "FROM x–t SLOPE TO v–t HEIGHT",
            "Constant velocity becomes a horizontal line because the velocity value does not change with time.",
        )
        axes = self.v_t_axes(x_max=1.25, y_max=12, x_step=0.25, y_step=2, position=LEFT * 2.85 + DOWN * 0.56)
        labels = self.axis_labels(axes, r"v\;(\mathrm{m/s})")
        a_line = Line(axes.c2p(0, 10), axes.c2p(1.20, 10), color=BLACK_LINE, stroke_width=3.4)
        t_line = Line(axes.c2p(0, 1), axes.c2p(1.20, 1), color=DARK_GRAY, stroke_width=3.4)
        catch = DashedLine(axes.c2p(self.T_CATCH, 0), axes.c2p(self.T_CATCH, 10.7), color=MID_GRAY)
        a_tag = self.math(r"v_A=10\,\mathrm{m/s}", 25).next_to(a_line, UP, buff=0.12).shift(LEFT * 0.60)
        t_tag = self.math(r"v_T=1\,\mathrm{m/s}", 25).next_to(t_line, UP, buff=0.10).shift(LEFT * 0.50)
        side = VGroup(
            self.card("GRAPH HEIGHT", "The vertical coordinate is velocity.", width=5.25, height=1.65),
            self.card("HORIZONTAL LINE", "Its height stays constant as time passes.", width=5.25, height=1.65),
            self.result_chip(r"t^*=\frac{10}{9}\,\mathrm{s}", 4.1, 31),
        ).arrange(DOWN, buff=0.23).move_to(RIGHT * 4.55 + DOWN * 0.52)
        self.play(Create(axes), Write(labels), run_time=RUN_NORMAL)
        self.play(Create(a_line), Write(a_tag), run_time=RUN_SLOW)
        self.play(Create(t_line), Write(t_tag), run_time=RUN_SLOW)
        self.play(Create(catch), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.10) for x in side], lag_ratio=0.16), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def area_is_displacement(self) -> None:
        self.set_header(
            6, "AREA UNDER v–t IS DISPLACEMENT",
            "For constant velocity, the shaded region is a rectangle: base is time and height is velocity.",
        )
        axes = self.v_t_axes(x_max=4, y_max=5, x_step=1, y_step=1, position=LEFT * 3.10 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"v\;(\mathrm{m/s})")
        top = Line(axes.c2p(0, 3), axes.c2p(4, 3), color=BLACK_LINE, stroke_width=3.3)
        area = Polygon(
            axes.c2p(0, 0), axes.c2p(4, 0), axes.c2p(4, 3), axes.c2p(0, 3),
            stroke_color=MID_GRAY, stroke_width=1.8, fill_color=LIGHT_GRAY, fill_opacity=0.48,
        )
        base_label = self.math(r"\Delta t=4\,\mathrm{s}", 25).next_to(axes.x_axis, DOWN, buff=0.42)
        height_label = self.math(r"v=3\,\mathrm{m/s}", 25).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.42)
        stack = VGroup(
            self.math(r"\Delta x=\mathrm{area}", 37),
            self.math(r"\Delta x=(\Delta t)(v)", 37),
            self.math(r"\Delta x=(4\,\mathrm{s})(3\,\mathrm{m/s})", 34),
            self.math(r"\Delta x=12\,\mathrm{m}", 40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.25 + DOWN * 0.48)
        unit_check = self.result_chip(r"(\mathrm{s})\left(\frac{\mathrm{m}}{\mathrm{s}}\right)=\mathrm{m}", 4.8, 32)
        unit_check.next_to(stack, DOWN, buff=0.40)
        self.play(Create(axes), Write(labels), Create(top), run_time=RUN_NORMAL)
        self.play(FadeIn(area), Write(base_label), Write(height_label), run_time=RUN_SLOW)
        for line in stack:
            self.play(Write(line), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.55)
        self.play(FadeIn(unit_check, shift=UP * 0.08), run_time=RUN_NORMAL)
        self.focus_on(VGroup(area, base_label, height_label, stack[-2:], unit_check), width=13.8, pause=PAUSE_EXPLAIN)
        distinction = self.graph_caption("height = velocity   •   area = displacement", RIGHT * 4.25 + DOWN * 3.48)
        self.play(FadeIn(distinction), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def reconcile_achilles(self) -> None:
        self.set_header(
            7, "RECONCILE THE ACHILLES MEETING",
            "The two v–t areas give each object's displacement during the same catch interval.",
        )
        axes = self.v_t_axes(x_max=1.25, y_max=12, x_step=0.25, y_step=2, position=LEFT * 3.10 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"v\;(\mathrm{m/s})")
        catch_x = self.T_CATCH
        area_a = Polygon(axes.c2p(0, 0), axes.c2p(catch_x, 0), axes.c2p(catch_x, 10), axes.c2p(0, 10),
            color=BLACK_LINE, fill_color=LIGHT_GRAY, fill_opacity=0.48, stroke_width=2.0)
        area_t = Polygon(axes.c2p(0, 0), axes.c2p(catch_x, 0), axes.c2p(catch_x, 1), axes.c2p(0, 1),
            color=DARK_GRAY, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.95, stroke_width=2.0)
        a_calc = VGroup(
            self.text("ACHILLES", 24, BOLD),
            self.math(r"\Delta x_A=10\left(\frac{10}{9}\right)=\frac{100}{9}\,\mathrm{m}", 31),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        t_calc = VGroup(
            self.text("TORTOISE", 24, BOLD),
            self.math(r"\Delta x_T=1\left(\frac{10}{9}\right)=\frac{10}{9}\,\mathrm{m}", 31),
            self.math(r"x_T=10+\frac{10}{9}=\frac{100}{9}\,\mathrm{m}", 31),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        calculation_panel = VGroup(a_calc, Line(LEFT * 2.5, RIGHT * 2.5, color=LIGHT_GRAY), t_calc).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        ).move_to(RIGHT * 4.30 + DOWN * 0.45)
        final = self.result_chip(r"x_A=x_T=\frac{100}{9}\,\mathrm{m}", 5.2, 34).next_to(calculation_panel, DOWN, buff=0.42)
        self.play(Create(axes), Write(labels), run_time=RUN_NORMAL)
        self.play(FadeIn(area_a), run_time=RUN_SLOW)
        self.play(Write(a_calc), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(area_t), run_time=RUN_SLOW)
        self.play(Write(t_calc), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(final, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def guided_piecewise(self) -> None:
        self.set_header(
            8, "GUIDED EXAMPLE: SPLIT THE REGION",
            "The object moves at 4 m/s for 2 s, then at 2 m/s for the next 3 s. Find its displacement.",
        )
        axes = self.v_t_axes(x_max=5, y_max=5, x_step=1, y_step=1, position=LEFT * 3.10 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"v\;(\mathrm{m/s})")
        seg1 = Line(axes.c2p(0, 4), axes.c2p(2, 4), color=BLACK_LINE, stroke_width=3.4)
        drop = DashedLine(axes.c2p(2, 4), axes.c2p(2, 2), color=MID_GRAY)
        seg2 = Line(axes.c2p(2, 2), axes.c2p(5, 2), color=BLACK_LINE, stroke_width=3.4)
        area1 = Polygon(axes.c2p(0, 0), axes.c2p(2, 0), axes.c2p(2, 4), axes.c2p(0, 4),
            color=BLACK_LINE, fill_color=LIGHT_GRAY, fill_opacity=0.48)
        area2 = Polygon(axes.c2p(2, 0), axes.c2p(5, 0), axes.c2p(5, 2), axes.c2p(2, 2),
            color=DARK_GRAY, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.92)
        prompt = self.card("PAUSE AND PLAN", "How many rectangles do you see?", width=5.2, height=1.40).move_to(RIGHT * 4.35 + UP * 1.42)
        eqs = VGroup(
            self.math(r"A_1=(2\,\mathrm{s})(4\,\mathrm{m/s})=8\,\mathrm{m}", 30),
            self.math(r"A_2=(3\,\mathrm{s})(2\,\mathrm{m/s})=6\,\mathrm{m}", 30),
            self.math(r"\Delta x=A_1+A_2=14\,\mathrm{m}", 36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(RIGHT * 4.40 + DOWN * 1.00)
        self.play(Create(axes), Write(labels), Create(seg1), Create(drop), Create(seg2), run_time=RUN_SLOW)
        self.play(FadeIn(prompt, shift=LEFT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(area1), run_time=RUN_NORMAL)
        self.play(Write(eqs[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(area2), run_time=RUN_NORMAL)
        self.play(Write(eqs[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        answer_box = SurroundingRectangle(eqs[2], buff=0.18, color=BLACK_LINE, stroke_width=2.2)
        self.play(Write(eqs[2]), Create(answer_box), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def signed_area(self) -> None:
        self.set_header(
            9, "AREA BELOW THE AXIS IS NEGATIVE",
            "Displacement keeps direction. Distance travelled counts every part as a positive length.",
        )
        axes = self.v_t_axes(x_max=5, y_min=-2, y_max=3, x_step=1, y_step=1, position=LEFT * 3.10 + DOWN * 0.60)
        labels = self.axis_labels(axes, r"v\;(\mathrm{m/s})")
        pos_seg = Line(axes.c2p(0, 2), axes.c2p(3, 2), color=BLACK_LINE, stroke_width=3.4)
        jump = DashedLine(axes.c2p(3, 2), axes.c2p(3, -1), color=MID_GRAY)
        neg_seg = Line(axes.c2p(3, -1), axes.c2p(5, -1), color=DARK_GRAY, stroke_width=3.4)
        pos_area = Polygon(axes.c2p(0, 0), axes.c2p(3, 0), axes.c2p(3, 2), axes.c2p(0, 2),
            color=BLACK_LINE, fill_color=LIGHT_GRAY, fill_opacity=0.52)
        neg_area = Polygon(axes.c2p(3, 0), axes.c2p(5, 0), axes.c2p(5, -1), axes.c2p(3, -1),
            color=DARK_GRAY, fill_color=VERY_LIGHT_GRAY, fill_opacity=0.98)
        plus = self.math(r"+6\,\mathrm{m}", 27).move_to(axes.c2p(1.5, 1.0))
        minus = self.math(r"-2\,\mathrm{m}", 27).move_to(axes.c2p(4.0, -0.55))
        displacement = self.result_chip(r"\Delta x=6-2=4\,\mathrm{m}", 5.2, 34)
        distance = self.result_chip(r"d=6+2=8\,\mathrm{m}", 5.2, 34)
        compare = VGroup(
            self.text("SIGNED AREA → DISPLACEMENT", 23, BOLD), displacement,
            self.text("ABSOLUTE AREAS → DISTANCE", 23, BOLD), distance,
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 4.35 + DOWN * 0.40)
        self.play(Create(axes), Write(labels), Create(pos_seg), Create(jump), Create(neg_seg), run_time=RUN_SLOW)
        self.play(FadeIn(pos_area), Write(plus), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(neg_area), Write(minus), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.08) for x in compare], lag_ratio=0.15), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def recipe_and_exit(self) -> None:
        self.set_header(
            10, "NOTEBOOK RECIPE",
            "Use these five steps every time you calculate displacement from a velocity–time graph.",
        )
        recipe = self.process_map(
            [("1", "Read axes and units"), ("2", "Split the region"),
             ("3", "Calculate each area"), ("4", "Apply the sign"),
             ("5", "Add and write metres")],
            card_width=4.15, card_height=1.18, columns=3,
        ).move_to(DOWN * 0.52)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in recipe], lag_ratio=0.12), run_time=RUN_SLOW)
        formula = self.result_chip(r"\boxed{\Delta x=\text{signed area under the }v\!\! -\!\! t\text{ graph}}", 9.8, 32)
        formula.next_to(recipe, DOWN, buff=0.45)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()

        self.set_header(
            11, "EXIT TICKET",
            "A horizontal line is at 3 m/s from 0 s to 4 s. Find the displacement and explain the unit.",
        )
        axes = self.v_t_axes(x_max=4, y_max=4, x_step=1, y_step=1, position=LEFT * 2.95 + DOWN * 0.55)
        labels = self.axis_labels(axes, r"v\;(\mathrm{m/s})")
        seg = Line(axes.c2p(0, 3), axes.c2p(4, 3), color=BLACK_LINE, stroke_width=3.4)
        area = Polygon(axes.c2p(0, 0), axes.c2p(4, 0), axes.c2p(4, 3), axes.c2p(0, 3),
            color=BLACK_LINE, fill_color=LIGHT_GRAY, fill_opacity=0.45)
        work = self.card("YOUR TURN", "Base? Height? Area? Unit?", width=5.1, height=1.75).move_to(RIGHT * 4.45 + UP * 0.65)
        answer = VGroup(
            self.math(r"\Delta x=(4\,\mathrm{s})(3\,\mathrm{m/s})", 32),
            self.result_chip(r"\Delta x=12\,\mathrm{m}", 4.4, 38),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT * 4.45 + DOWN * 1.45)
        self.play(Create(axes), Write(labels), Create(seg), FadeIn(area), FadeIn(work), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK * 1.45)
        self.play(Write(answer[0]), FadeIn(answer[1], shift=UP * 0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)

    def construct(self) -> None:
        self.opening()
        self.lesson_map()
        self.consolidate_meeting()
        self.position_time_graph()
        self.slopes()
        self.velocity_time_height()
        self.area_is_displacement()
        self.reconcile_achilles()
        self.guided_piecewise()
        self.signed_area()
        self.recipe_and_exit()
        self.standard_closing(
            "x–t slope gives velocity; v–t signed area gives displacement."
        )
