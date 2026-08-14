
# =============================================================================
# SENIOR QA PATCH V5.1 — tangent geometry anchored after panel placement
# =============================================================================
def _fixed_tangent_problem(
    self,
    *,
    header_number: int,
    audit_id: str,
    title: str,
    subtitle: str,
    top_expr: str,
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
    point_eq: str,
    derivative_chain: Sequence[str],
    vector_eq: str,
    line_eq: str,
) -> None:
    """QA-fixed tangent scene.

    The original geometry objects were instantiated before the figure panel was
    repositioned. This patch creates the moving point, tangent and direction
    arrow *after* the panel reaches its final location, so every object remains
    spatially bound to the projected axes. The tangent span is also clipped to
    the visible axis ranges, eliminating cross-panel overlap.
    """
    self.audit(audit_id + "-QA51", title + " · anchored tangent geometry")
    self.set_header(header_number, title, subtitle)

    top = self.formula_panel(top_expr, width=11.6, height=1.05, font_size=31)
    top.move_to(UP * 1.55)
    self.play(FadeIn(top[0]), Write(top[1]), run_time=1.35, rate_func=smootherstep)
    self.wait(2.0)

    # Build only the curve/axes now. Dynamic geometry is rebuilt after layout.
    base, ax, tracker, _old_dot, _old_tangent, _old_point_arrow = self.tangent_projection(
        xy=xy,
        t0=t0,
        t_range=t_range,
        x_range=x_range,
        y_range=y_range,
        direction_2d=direction_2d,
        approach_from=approach_from,
        arrow_scale=arrow_scale,
        tangent_span=tangent_span,
        x_label=x_label,
        y_label=y_label,
    )
    panel = self.figure_panel(
        base,
        width=6.55,
        height=4.55,
        title="PROYECCION DE LA CURVA",
        caption="La proyeccion muestra el punto y la direccion sin perder el vector 3D.",
    )
    panel.group.move_to(LEFT * 3.55 + DOWN * 1.25)

    # Panel is now at its final coordinates: derive all geometry from moved axes.
    x0, y0 = xy(t0)
    dx, dy = direction_2d

    def _two_sided_bound() -> float:
        bounds: list[float] = []
        if abs(dx) > 1e-12:
            bounds.extend([
                abs((x_range[1] - x0) / dx),
                abs((x0 - x_range[0]) / dx),
            ])
        if abs(dy) > 1e-12:
            bounds.extend([
                abs((y_range[1] - y0) / dy),
                abs((y0 - y_range[0]) / dy),
            ])
        return min(bounds) if bounds else tangent_span

    def _forward_bound() -> float:
        bounds: list[float] = []
        if dx > 1e-12:
            bounds.append((x_range[1] - x0) / dx)
        elif dx < -1e-12:
            bounds.append((x_range[0] - x0) / dx)
        if dy > 1e-12:
            bounds.append((y_range[1] - y0) / dy)
        elif dy < -1e-12:
            bounds.append((y_range[0] - y0) / dy)
        positives = [b for b in bounds if b > 0]
        return min(positives) if positives else arrow_scale

    safe_span = min(tangent_span, 0.82 * _two_sided_bound())
    safe_arrow = min(arrow_scale, 0.62 * _forward_bound())

    moving_dot = always_redraw(
        lambda: Dot(
            ax.c2p(*xy(tracker.get_value())),
            radius=0.075,
            color=BLACK_LINE,
        )
    )
    p0 = Dot(ax.c2p(x0, y0), radius=0.085, color=BLACK_LINE)
    arrow = Arrow(
        ax.c2p(x0, y0),
        ax.c2p(x0 + safe_arrow * dx, y0 + safe_arrow * dy),
        buff=0,
        color=BLACK_LINE,
        stroke_width=3.0,
        max_tip_length_to_length_ratio=0.14,
    )
    tangent = Line(
        ax.c2p(x0 - safe_span * dx, y0 - safe_span * dy),
        ax.c2p(x0 + safe_span * dx, y0 + safe_span * dy),
        color=DARK_GRAY,
        stroke_width=2.3,
    )

    # Causal drawing sequence.
    self.play(FadeIn(panel.box), FadeIn(panel.title), FadeIn(panel.caption), run_time=0.85)
    self.play(Create(base[0]), Create(base[1]), FadeIn(base[2]), run_time=1.6, rate_func=smootherstep)
    self.add(moving_dot)
    self.play(tracker.animate.set_value(t0), run_time=3.5, rate_func=smootherstep)
    self.wait(1.0)
    self.play(FadeOut(moving_dot), FadeIn(p0, scale=0.45), GrowArrow(arrow),
              run_time=1.15, rate_func=smootherstep)
    self.wait(1.4)
    self.play(Create(tangent), run_time=1.35, rate_func=smootherstep)
    self.wait(2.0)

    right_x = 3.55
    point = self.math(point_eq, 31)
    self.fit(point, 5.7, 0.75)
    point.move_to(RIGHT * right_x + UP * 0.80)
    point_tag = self.latex_text("PUNTO", 21, "bold").next_to(point, LEFT, buff=0.16)
    self.play(FadeIn(point_tag), Write(point), run_time=1.0, rate_func=smootherstep)
    self.wait(1.5)

    deriv_final = self.animate_matching_chain(
        derivative_chain,
        position=RIGHT * right_x + DOWN * 0.15,
        font_size=29,
        max_width=5.8,
        pauses=[1.35] + [1.6] * (len(derivative_chain) - 1),
    )

    vector = self.math(vector_eq, 31)
    self.fit(vector, 5.8, 0.75)
    vector.move_to(RIGHT * right_x + DOWN * 1.25)
    vector_tag = self.latex_text("DIRECCION", 20, "bold").next_to(vector, LEFT, buff=0.14)
    self.play(FadeIn(vector_tag), TransformFromCopy(deriv_final, vector),
              run_time=1.05, rate_func=smootherstep)
    self.wait(1.8)

    # Do not morph two large equations through each other. Reveal the validated
    # final line cleanly after point and direction have both settled.
    result = self.result_panel(line_eq, width=6.15, font_size=32)
    result.move_to(RIGHT * right_x + DOWN * 2.45)
    self.play(FadeIn(result[0]), run_time=0.55, rate_func=smootherstep)
    self.play(Write(result[1]), run_time=1.35, rate_func=smootherstep)
    self.wait(4.2)
    self.clear_stage()


Video03_Tangentes_Auditable._tangent_problem = _fixed_tangent_problem
