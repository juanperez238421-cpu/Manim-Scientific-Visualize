            color=DARK_GRAY,
            stroke_width=2.3,
        )
        arrow = Arrow(
            ax.c2p(x0, y0),
            ax.c2p(x0 + arrow_scale * dx, y0 + arrow_scale * dy),
            buff=0,
            color=BLACK_LINE,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.14,
        )
        p0 = Dot(ax.c2p(x0, y0), radius=0.085, color=BLACK_LINE)
        return base, ax, tracker, moving_dot, tangent, VGroup(p0, arrow)


# =============================================================================
# VIDEO 1 — DOMAINS
# =============================================================================
class Video01_Dominios_Auditable(WorkshopBase):
    def construct(self) -> None:
        self.audit("V1-START", "Video 1 domains")
        self.standard_opening(
            "CALCULO DE VARIAS VARIABLES · TALLER 1",
            "DOMINIO DE FUNCIONES VECTORIALES",
            "Tres componentes comparten un mismo parametro t.",
            "Construir restricciones, intersectarlas y verificar extremos.",
        )
        self.intro_logic()
        self.problem_1a()
        self.problem_1b()
        self.problem_1c()
        self.problem_1d()
        self.summary_domain()
        self.audit("V1-END", "Video 1 complete")

    def intro_logic(self) -> None:
        self.audit("V1-01", "domain intersection principle")
        self.set_header(1, "IDEA CENTRAL: EL DOMINIO ES UNA INTERSECCION",
                        "Cada componente impone su propia condicion; el parametro solo es valido cuando todas se cumplen.")

        master = self.result_panel(r"\operatorname{Dom}(\mathbf r)=D_x\cap D_y\cap D_z", width=5.8, font_size=42)
        master.move_to(UP * 1.65)
        cards = VGroup()
        for badge, formula, domain in [
            (r"\mathbf i", r"x(t)", r"D_x"),
            (r"\mathbf j", r"y(t)", r"D_y"),
            (r"\mathbf k", r"z(t)", r"D_z"),
        ]:
            box = RoundedRectangle(width=3.45, height=1.55, corner_radius=0.10,
                                   stroke_color=BLACK_LINE, stroke_width=1.8,
                                   fill_color=WHITE, fill_opacity=1)
            content = VGroup(self.math(badge, 28), self.math(formula, 34), self.math(domain, 27))
            content.arrange(DOWN, buff=0.10).move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange(RIGHT, buff=0.38).move_to(DOWN * 0.70)
        arrows = VGroup(*[
            Arrow(master.get_bottom(), card.get_top(), buff=0.08, color=MID_GRAY, stroke_width=1.6,
                  max_tip_length_to_length_ratio=0.09)
            for card in cards
        ])
        group = VGroup(master, cards, arrows)
        self.assert_content_safe(group, "domain intro")

        self.play(FadeIn(master[0]), Write(master[1]), run_time=1.35, rate_func=smootherstep)
        self.wait(2.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.14), run_time=1.25)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in cards], lag_ratio=0.18),
                  run_time=1.8, rate_func=smootherstep)
        self.wait(3.0)
        self.clear_stage()

    def problem_1a(self) -> None:
        self.audit("V1-1A", "sqrt(t^2-9): parabola and sign regions")
        self.set_header(2, "1(a) · LA RAIZ CUADRADA CREA DOS REGIONES VALIDAS",
                        "Primero se visualiza el radicando; despues se traduce su signo a una condicion sobre t.")
        expr = self.formula_panel(AUDIT_DATA["1a"]["expr"], width=10.2, height=1.03, font_size=34)
        expr.move_to(UP * 1.55)
        self.play(FadeIn(expr[0]), Write(expr[1]), run_time=1.25)
        self.wait(2.0)

        axes = Axes(x_range=[-5, 5, 1], y_range=[-10, 17, 5], x_length=5.6, y_length=3.2,
                    tips=False, axis_config={"color": MID_GRAY, "stroke_width": 1.5, "include_ticks": False})
        parabola = axes.plot(lambda t: t*t - 9, x_range=[-4.5, 4.5], color=BLACK_LINE, stroke_width=2.7)
        roots = VGroup(Dot(axes.c2p(-3, 0), radius=0.07, color=BLACK_LINE),
                       Dot(axes.c2p(3, 0), radius=0.07, color=BLACK_LINE))
        root_labels = VGroup(self.math("-3", 20).next_to(roots[0], DOWN, buff=0.08),
                             self.math("3", 20).next_to(roots[1], DOWN, buff=0.08))
        graph_group = VGroup(axes, parabola, roots, root_labels)
        graph_panel = self.figure_panel(graph_group, width=6.45, height=4.35,
                                        title="SIGNO DEL RADICANDO",
                                        caption="La curva esta sobre el eje cuando t <= -3 o t >= 3.")

        chain_anchor = RIGHT * 3.55 + DOWN * 0.15
        graph_panel.group.move_to(LEFT * 3.55 + DOWN * 1.15)
        self.play(FadeIn(graph_panel.box), FadeIn(graph_panel.title), FadeIn(graph_panel.caption), run_time=0.9)
        self.play(Create(axes), run_time=0.95, rate_func=smootherstep)
        self.play(Create(parabola), run_time=1.55, rate_func=smootherstep)
        self.play(LaggedStart(FadeIn(roots[0], scale=0.4), FadeIn(roots[1], scale=0.4), lag_ratio=0.18), run_time=0.8)
        self.play(FadeIn(root_labels), run_time=0.5)
        self.wait(2.0)

        final_eq = self.animate_matching_chain([
            r"t^2-9\ge 0",
            r"(t-3)(t+3)\ge 0",
            r"t\le -3\quad\text{o}\quad t\ge 3",
        ], position=chain_anchor + UP * 0.70, font_size=39, max_width=6.1,
           pauses=[2.0, 2.2, 2.8])
        lane = self.domain_lane([(None, -3, False, True), (3, None, True, False)],
                                x_min=-6, x_max=6, length=5.3, label=r"D_x", endpoint_labels=(-3, 3))
        lane.move_to(chain_anchor + DOWN * 0.70)
        self.animate_domain_lane(lane, pause=2.0)
        result = self.result_panel(r"\operatorname{Dom}(\mathbf r)=(-\infty,-3]\cup[3,\infty)", width=6.1, font_size=34)
        result.move_to(chain_anchor + DOWN * 1.85)
        self.play(FadeIn(result[0]), TransformFromCopy(final_eq, result[1]), run_time=1.15, rate_func=smootherstep)
        self.wait(3.8)
        self.clear_stage()

    def problem_1b(self) -> None:
        self.audit("V1-1B", "all three components defined on R")
        self.set_header(3, "1(b) · TRES COMPONENTES SIN RESTRICCION",
                        "Trigonometria y exponencial estan definidas para todo numero real: las tres lineas coinciden.")
        expr = self.formula_panel(AUDIT_DATA["1b"]["expr"], width=10.9, height=1.03, font_size=32)
        expr.move_to(UP * 1.55)
        self.play(FadeIn(expr[0]), Write(expr[1]), run_time=1.3)
        self.wait(1.8)

        lines = VGroup()
        labels = [r"D_x", r"D_y", r"D_z"]
        for lab in labels:
            lane = self.domain_lane([(None, None, False, False)], x_min=-5, x_max=5, length=8.4, label=lab)
            lines.add(lane)
        lines.arrange(DOWN, buff=0.58).move_to(DOWN * 0.35)
        captions = VGroup(
            self.math(r"\cos(2t)", 27), self.math(r"e^{-t}", 27), self.math(r"\sin(2t)", 27)
        )
        for cap, lane in zip(captions, lines):
            cap.next_to(lane, RIGHT, buff=0.22)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.08) for c in captions], lag_ratio=0.18), run_time=1.0)
        for lane in lines:
            self.animate_domain_lane(lane, pause=0.55)

        tracker = ValueTracker(-4.6)
        dots = VGroup(*[
            always_redraw(lambda lane=lane: Dot(lane[0].n2p(tracker.get_value()), radius=0.065, color=BLACK_LINE))
            for lane in lines
        ])
        self.add(dots)
        self.play(tracker.animate.set_value(4.6), run_time=4.2, rate_func=smootherstep)
        self.wait(1.6)
        result = self.result_panel(r"D_x\cap D_y\cap D_z=\mathbb R", width=5.0, font_size=40)
        result.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(result[0]), Write(result[1]), run_time=1.2)
        self.wait(3.5)
        self.clear_stage()

    def problem_1c(self) -> None:
        self.audit("V1-1C", "intersection of ray with two holes")
        self.set_header(4, "1(c) · INTERSECCION DE UNA SEMIRRECTA CON DOS HUECOS",
                        "La raiz fija el inicio en -6; el denominador elimina -3 y 3; la componente lineal no restringe.")
        expr = self.formula_panel(AUDIT_DATA["1c"]["expr"], width=11.2, height=1.05, font_size=31)
        expr.move_to(UP * 1.55)
        self.play(FadeIn(expr[0]), Write(expr[1]), run_time=1.25)
        self.wait(2.0)

        lanes = VGroup(
            self.domain_lane([(-6, None, True, False)], x_min=-7, x_max=7, length=8.0, label=r"D_x", endpoint_labels=(-6,)),
            self.domain_lane([(None, None, False, False)], x_min=-7, x_max=7, length=8.0, label=r"D_y"),
            self.domain_lane([(None, -3, False, False), (-3, 3, False, False), (3, None, False, False)],
                             x_min=-7, x_max=7, length=8.0, label=r"D_z", endpoint_labels=(-3, 3)),
        )
