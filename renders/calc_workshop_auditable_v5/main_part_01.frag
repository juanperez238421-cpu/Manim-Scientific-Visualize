            current = target
            self.wait(pause)
        return current

    def result_panel(self, expression: str, *, width: float = 6.2, font_size: int = 39) -> VGroup:
        panel = self.formula_panel(expression, width=width, height=1.08, font_size=font_size)
        panel[0].set_stroke(width=2.6)
        return panel

    # ------------------------------------------------------------------
    # Number-line visuals
    # ------------------------------------------------------------------
    def domain_lane(
        self,
        intervals: Sequence[tuple[float | None, float | None, bool, bool]],
        *,
        x_min: float = -7,
        x_max: float = 7,
        length: float = 5.7,
        label: str = "D",
        endpoint_labels: Sequence[float] = (),
    ) -> VGroup:
        line = NumberLine(
            x_range=[x_min, x_max, 1],
            length=length,
            include_numbers=False,
            include_tip=False,
            color=MID_GRAY,
            stroke_width=1.7,
        )
        lane_label = self.math(label, 27).next_to(line, LEFT, buff=0.18)
        marks = VGroup()
        for value in endpoint_labels:
            marks.add(self.math(str(int(value)) if float(value).is_integer() else str(value), 20)
                      .next_to(line.n2p(value), DOWN, buff=0.13))

        allowed = VGroup()
        endpoint_mobs = VGroup()
        for a, b, closed_a, closed_b in intervals:
            aa = x_min if a is None else a
            bb = x_max if b is None else b
            segment = Line(line.n2p(aa), line.n2p(bb), color=BLACK_LINE, stroke_width=6.0)
            allowed.add(segment)
            if a is not None:
                endpoint_mobs.add(
                    Dot(line.n2p(a), radius=0.075, color=BLACK_LINE)
                    if closed_a
                    else Circle(radius=0.075, color=BLACK_LINE, stroke_width=2.2,
                                fill_color=WHITE, fill_opacity=1).move_to(line.n2p(a))
                )
            if b is not None:
                endpoint_mobs.add(
                    Dot(line.n2p(b), radius=0.075, color=BLACK_LINE)
                    if closed_b
                    else Circle(radius=0.075, color=BLACK_LINE, stroke_width=2.2,
                                fill_color=WHITE, fill_opacity=1).move_to(line.n2p(b))
                )
        return VGroup(line, allowed, endpoint_mobs, marks, lane_label)

    def animate_domain_lane(self, lane: VGroup, *, pause: float = 1.0) -> None:
        line, allowed, endpoints, marks, label = lane
        self.play(Create(line), FadeIn(label), run_time=0.95, rate_func=smootherstep)
        if len(marks):
            self.play(FadeIn(marks), run_time=0.55)
        if len(allowed):
            self.play(LaggedStart(*[Create(seg) for seg in allowed], lag_ratio=0.12),
                      run_time=1.15, rate_func=smootherstep)
        if len(endpoints):
            self.play(LaggedStart(*[FadeIn(p, scale=0.55) for p in endpoints], lag_ratio=0.12),
                      run_time=0.70)
        self.wait(pause)

    # ------------------------------------------------------------------
    # Limit mini-graphs
    # ------------------------------------------------------------------
    def mini_limit_graphs(
        self,
        funcs: Sequence[Callable[[float], float]],
        *,
        t0: float,
        x_range: tuple[float, float],
        y_ranges: Sequence[tuple[float, float]],
        labels: Sequence[str] = ("i", "j", "k"),
    ) -> tuple[VGroup, list[Axes], ValueTracker, VGroup]:
        axes_list: list[Axes] = []
        plot_groups = VGroup()
        for func, yr, label in zip(funcs, y_ranges, labels):
            ax = Axes(
                x_range=[x_range[0], x_range[1], (x_range[1]-x_range[0])/4],
                y_range=[yr[0], yr[1], (yr[1]-yr[0])/4],
                x_length=2.05,
                y_length=2.15,
                tips=False,
                axis_config={"color": MID_GRAY, "stroke_width": 1.5, "include_ticks": False},
            )
            curve = ax.plot(func, x_range=[x_range[0], x_range[1]], color=BLACK_LINE, stroke_width=2.4)
            tag = self.math(r"\mathbf " + label, 25).next_to(ax, UP, buff=0.05)
            plot_groups.add(VGroup(ax, curve, tag))
            axes_list.append(ax)
        plot_groups.arrange(RIGHT, buff=0.38)

        eps = ValueTracker(min(0.85, (x_range[1] - x_range[0]) * 0.23))
        moving = VGroup()
        for ax, func in zip(axes_list, funcs):
            left_dot = always_redraw(
                lambda ax=ax, func=func: Dot(
                    ax.c2p(t0 - eps.get_value(), func(t0 - eps.get_value())),
                    radius=0.060,
                    color=BLACK_LINE,
                )
            )
            right_dot = always_redraw(
                lambda ax=ax, func=func: Circle(
                    radius=0.060,
                    color=BLACK_LINE,
                    stroke_width=2.0,
                    fill_color=WHITE,
                    fill_opacity=1,
                ).move_to(ax.c2p(t0 + eps.get_value(), func(t0 + eps.get_value())))
            )
            moving.add(left_dot, right_dot)
        return plot_groups, axes_list, eps, moving

    # ------------------------------------------------------------------
    # Tangent projection visual
    # ------------------------------------------------------------------
    def tangent_projection(
        self,
        *,
        xy: Callable[[float], tuple[float, float]],
        t0: float,
        t_range: tuple[float, float],
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        direction_2d: tuple[float, float],
        approach_from: float,
        arrow_scale: float,
        tangent_span: float,
        x_label: str,
        y_label: str,
    ) -> tuple[VGroup, Axes, ValueTracker, Mobject, Mobject, Mobject]:
        ax = Axes(
            x_range=[x_range[0], x_range[1], (x_range[1]-x_range[0])/4],
            y_range=[y_range[0], y_range[1], (y_range[1]-y_range[0])/4],
            x_length=5.5,
            y_length=3.65,
            tips=False,
            axis_config={"color": MID_GRAY, "stroke_width": 1.55, "include_ticks": False},
        )
        curve = ParametricFunction(
            lambda u: ax.c2p(*xy(u)),
            t_range=[t_range[0], t_range[1], 0.015],
            color=BLACK_LINE,
            stroke_width=2.8,
        )
        labels = VGroup(
            self.math(x_label, 23).next_to(ax.x_axis.get_end(), DOWN, buff=0.06),
            self.math(y_label, 23).next_to(ax.y_axis.get_end(), LEFT, buff=0.06),
        )
        base = VGroup(ax, curve, labels)

        tracker = ValueTracker(approach_from)
        moving_dot = always_redraw(
            lambda: Dot(ax.c2p(*xy(tracker.get_value())), radius=0.075, color=BLACK_LINE)
        )
        x0, y0 = xy(t0)
        dx, dy = direction_2d
        tangent = ParametricFunction(
            lambda s: ax.c2p(x0 + s * dx, y0 + s * dy),
            t_range=[-tangent_span, tangent_span, 0.02],
