        lanes.arrange(DOWN, buff=0.62).move_to(DOWN * 0.15)
        reasons = VGroup(
            self.math(r"t+6\ge 0", 25),
            self.math(r"3t\;\text{sin restriccion}", 25),
            self.math(r"t^2-9\ne 0", 25),
        )
        for reason, lane in zip(reasons, lanes):
            reason.next_to(lane, RIGHT, buff=0.25)
        self.reveal_group(reasons, lag=0.20, run_time=1.2, shift=LEFT * 0.08, pause=0.8)
        for lane in lanes:
            self.animate_domain_lane(lane, pause=0.75)

        final_lane = self.domain_lane([(-6, -3, True, False), (-3, 3, False, False), (3, None, False, False)],
                                      x_min=-7, x_max=7, length=8.0, label=r"D", endpoint_labels=(-6, -3, 3))
        final_lane.to_edge(DOWN, buff=0.36)
        self.play(FadeOut(reasons), lanes.animate.set_opacity(0.28), run_time=0.8)
        self.animate_domain_lane(final_lane, pause=2.0)
        result = self.result_panel(r"[-6,-3)\cup(-3,3)\cup(3,\infty)", width=6.2, font_size=36)
        result.next_to(final_lane, UP, buff=0.28)
        self.play(FadeIn(result[0]), Write(result[1]), run_time=1.2)
        self.wait(4.0)
        self.clear_stage()

    def problem_1d(self) -> None:
        self.audit("V1-1D", "log restriction dominates exp hole at zero")
        self.set_header(5, "1(d) · UNA RESTRICCION DOMINA A LA OTRA",
                        "El logaritmo exige t > 2; por eso el hueco t = 0 de e^(1/t) queda fuera automaticamente.")
        expr = self.formula_panel(AUDIT_DATA["1d"]["expr"], width=11.1, height=1.05, font_size=31)
        expr.move_to(UP * 1.55)
        self.play(FadeIn(expr[0]), Write(expr[1]), run_time=1.25)
        self.wait(2.0)

        lanes = VGroup(
            self.domain_lane([(2, None, False, False)], x_min=-2, x_max=8, length=8.0, label=r"D_x", endpoint_labels=(2,)),
            self.domain_lane([(None, 0, False, False), (0, None, False, False)], x_min=-2, x_max=8, length=8.0,
                             label=r"D_y", endpoint_labels=(0,)),
            self.domain_lane([(None, None, False, False)], x_min=-2, x_max=8, length=8.0, label=r"D_z"),
        )
        lanes.arrange(DOWN, buff=0.62).move_to(DOWN * 0.20)
        reasons = VGroup(
            self.math(r"\ln(t-2):\;t>2", 25),
            self.math(r"e^{1/t}:\;t\ne 0", 25),
            self.math(r"\cos(2t):\;\mathbb R", 25),
        )
        for reason, lane in zip(reasons, lanes):
            reason.next_to(lane, RIGHT, buff=0.25)
        self.reveal_group(reasons, lag=0.20, run_time=1.2, shift=LEFT * 0.08, pause=0.8)
        for lane in lanes:
            self.animate_domain_lane(lane, pause=0.65)
        dominance = self.note_panel("LECTURA DE LA INTERSECCION",
                                    ["Todo t > 2 ya cumple t != 0.", "La restriccion del logaritmo decide el dominio final."],
                                    width=5.5, title_size=24, body_size=21)
        dominance.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(dominance, shift=UP * 0.08), run_time=1.0)
        self.wait(2.6)
        result = self.result_panel(r"\operatorname{Dom}(\mathbf r)=(2,\infty)", width=5.2, font_size=39)
        result.move_to(DOWN * 2.75)
        self.play(FadeOut(dominance), FadeIn(result[0]), Write(result[1]), run_time=1.2)
        self.wait(4.0)
        self.clear_stage()

    def summary_domain(self) -> None:
        self.audit("V1-SUM", "domain method map")
        self.set_header(6, "METODO REPRODUCIBLE",
                        "El objetivo no es memorizar casos: es traducir cada componente a un conjunto y luego intersectar.")
        route = self.process_map([
            ("1", "SEPARAR COMPONENTES"),
            ("2", "DETECTAR RESTRICCIONES"),
            ("3", "DIBUJAR CADA CONJUNTO"),
            ("4", "INTERSECTAR"),
            ("5", "REVISAR EXTREMOS"),
            ("6", "ESCRIBIR INTERVALOS"),
        ], columns=3)
        route.move_to(DOWN * 0.30)
        self.fit(route, 13.8, 4.9)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in route], lag_ratio=0.10),
                  run_time=2.0, rate_func=smootherstep)
        self.wait(4.2)
        self.standard_closing("Restriccion por componente. Interseccion al final. Verificacion siempre.")


# VIDEO 2
class Video02_Limites_Auditable(WorkshopBase):
    def construct(self) -> None:
        self.audit("V2-START", "Video 2 vector limits")
        self.standard_opening(
            "CALCULO DE VARIAS VARIABLES · TALLER 1",
            "LIMITES DE FUNCIONES VECTORIALES",
            "Un mismo t se aproxima al objetivo en las tres componentes.",
            "Resolver componente a componente y reconstruir el vector al final.",
        )
        self.intro_limit()
        self.problem_2a()
        self.problem_2b()
        self.problem_2c()
        self.summary_limit()
        self.audit("V2-END", "Video 2 complete")

    def intro_limit(self) -> None:
        self.audit("V2-01", "componentwise limit principle")
        self.set_header(1, "IDEA CENTRAL: UN PARAMETRO, TRES SALIDAS",
                        "Si cada componente tiene limite, el vector limite se arma con esos tres resultados en el mismo orden.")
        formula = self.result_panel(
            r"\lim_{t\to a}\langle f(t),g(t),h(t)\rangle=\langle\lim f,\lim g,\lim h\rangle",
            width=10.6, font_size=34)
        formula.move_to(UP * 1.45)
        self.play(FadeIn(formula[0]), Write(formula[1]), run_time=1.45)
        self.wait(2.4)

        tline = NumberLine(x_range=[-2, 2, 1], length=8.2, include_numbers=False, color=MID_GRAY, stroke_width=1.8)
        tline.move_to(DOWN * 0.25)
        target = Dot(tline.n2p(0), radius=0.08, color=BLACK_LINE)
        target_label = self.math(r"a", 26).next_to(target, DOWN, buff=0.12)
        eps = ValueTracker(1.7)
        left = always_redraw(lambda: Dot(tline.n2p(-eps.get_value()), radius=0.065, color=BLACK_LINE))
        right = always_redraw(lambda: Circle(radius=0.065, color=BLACK_LINE, fill_color=WHITE, fill_opacity=1,
                                              stroke_width=2).move_to(tline.n2p(eps.get_value())))
        self.play(Create(tline), FadeIn(target), FadeIn(target_label), run_time=1.0)
        self.add(left, right)
        self.play(eps.animate.set_value(0.10), run_time=4.0, rate_func=smootherstep)
        self.wait(1.8)
        cards = VGroup(*[
            self.formula_panel(expr, width=3.65, height=1.05, font_size=31)
            for expr in (r"f(t)\to L_x", r"g(t)\to L_y", r"h(t)\to L_z")
        ])
        cards.arrange(RIGHT, buff=0.32).move_to(DOWN * 2.0)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.15), run_time=1.6)
        self.wait(3.0)
        self.clear_stage()

    def _limit_problem(
        self,
        *,
        header_number: int,
        audit_id: str,
        title: str,
        subtitle: str,
        top_expr: str,
        t0: float,
        funcs: Sequence[Callable[[float], float]],
        plot_x_range: tuple[float, float],
        y_ranges: Sequence[tuple[float, float]],
        chains: Sequence[Sequence[str]],
        final_vector: str,
        note: tuple[str, Sequence[str]] | None = None,
    ) -> None:
        self.audit(audit_id, title)
        self.set_header(header_number, title, subtitle)
        top = self.formula_panel(top_expr, width=11.8, height=1.08, font_size=30)
        top.move_to(UP * 1.55)
        self.play(FadeIn(top[0]), Write(top[1]), run_time=1.35)
        self.wait(2.0)

        plots, axes_list, eps, moving = self.mini_limit_graphs(
            funcs, t0=t0, x_range=plot_x_range, y_ranges=y_ranges
        )
        fig_panel = self.figure_panel(plots, width=6.45, height=4.25,
                                      title="APROXIMACION POR AMBOS LADOS",
                                      caption="Los puntos negro y blanco usan el mismo epsilon en las tres componentes.")
        fig_panel.group.move_to(LEFT * 3.55 + DOWN * 1.20)
        self.play(FadeIn(fig_panel.box), FadeIn(fig_panel.title), FadeIn(fig_panel.caption), run_time=0.9)
        self.play(LaggedStart(*[Create(g[0]) for g in plots], lag_ratio=0.12), run_time=1.0)
        self.play(LaggedStart(*[Create(g[1]) for g in plots], lag_ratio=0.14), run_time=1.55, rate_func=smootherstep)
        self.play(FadeIn(VGroup(*[g[2] for g in plots])), run_time=0.6)
        self.add(moving)
        self.play(eps.animate.set_value(0.055), run_time=4.2, rate_func=smootherstep)
        self.wait(1.8)
