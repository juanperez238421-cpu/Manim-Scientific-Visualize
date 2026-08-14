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
        self.audit(audit_id, title)
        self.set_header(header_number, title, subtitle)
        top = self.formula_panel(top_expr, width=11.6, height=1.05, font_size=31)
        top.move_to(UP * 1.55)
        self.play(FadeIn(top[0]), Write(top[1]), run_time=1.35)
        self.wait(2.0)

        base, ax, tracker, moving_dot, tangent, point_arrow = self.tangent_projection(
            xy=xy, t0=t0, t_range=t_range, x_range=x_range, y_range=y_range,
            direction_2d=direction_2d, approach_from=approach_from, arrow_scale=arrow_scale,
            tangent_span=tangent_span, x_label=x_label, y_label=y_label,
        )
        panel = self.figure_panel(base, width=6.55, height=4.55, title="PROYECCION DE LA CURVA",
                                  caption="La proyeccion muestra el punto y la direccion sin perder el vector 3D.")
        panel.group.move_to(LEFT * 3.55 + DOWN * 1.25)
        self.play(FadeIn(panel.box), FadeIn(panel.title), FadeIn(panel.caption), run_time=0.85)
        self.play(Create(base[0]), Create(base[1]), FadeIn(base[2]), run_time=1.6, rate_func=smootherstep)
        self.add(moving_dot)
        self.play(tracker.animate.set_value(t0), run_time=3.5, rate_func=smootherstep)
        self.wait(1.0)
        self.play(FadeOut(moving_dot), FadeIn(point_arrow[0], scale=0.45), GrowArrow(point_arrow[1]),
                  run_time=1.15, rate_func=smootherstep)
        self.wait(1.4)
        self.play(Create(tangent), run_time=1.35, rate_func=smootherstep)
        self.wait(2.0)

        right_x = 3.55
        point = self.math(point_eq, 31)
        self.fit(point, 5.7, 0.75)
        point.move_to(RIGHT * right_x + UP * 0.80)
        point_tag = self.latex_text("PUNTO", 21, "bold").next_to(point, LEFT, buff=0.16)
        self.play(FadeIn(point_tag), Write(point), run_time=1.0)
        self.wait(1.5)

        deriv_final = self.animate_matching_chain(derivative_chain, position=RIGHT * right_x + DOWN * 0.15,
                                                   font_size=29, max_width=5.8,
                                                   pauses=[1.35] + [1.6]*(len(derivative_chain)-1))
        vector = self.math(vector_eq, 31)
        self.fit(vector, 5.8, 0.75)
        vector.move_to(RIGHT * right_x + DOWN * 1.25)
        vector_tag = self.latex_text("DIRECCION", 20, "bold").next_to(vector, LEFT, buff=0.14)
        self.play(FadeIn(vector_tag), TransformFromCopy(deriv_final, vector), run_time=1.1, rate_func=smootherstep)
        self.wait(1.8)

        result = self.result_panel(line_eq, width=6.15, font_size=32)
        result.move_to(RIGHT * right_x + DOWN * 2.45)
        self.play(FadeIn(result[0]), TransformFromCopy(VGroup(point, vector), result[1]), run_time=1.3, rate_func=smootherstep)
        self.wait(4.2)
        self.clear_stage()

    def problem_3a(self) -> None:
        self._tangent_problem(
            header_number=2, audit_id="V3-3A",
            title="3(a) · EL PUNTO Y LA DIRECCION EN t = 0",
            subtitle="En la proyeccion x-z la direccion (1,-1) hace visible la inclinacion de la tangente.",
            top_expr=r"\mathbf r(t)=\langle\sin t,\,t^2-\cos t,\,-e^t\rangle,\qquad t_0=0",
            xy=lambda t: (math.sin(t), -math.exp(t)), t0=0.0, t_range=(-1.15, 0.80),
            x_range=(-1.2, 1.1), y_range=(-2.6, -0.2), direction_2d=(1.0, -1.0),
            approach_from=-0.95, arrow_scale=0.55, tangent_span=0.85, x_label="x", y_label="z",
            point_eq=r"\mathbf r(0)=\langle0,-1,-1\rangle",
            derivative_chain=(
                r"\mathbf r'(t)=\langle\cos t,\,2t+\sin t,\,-e^t\rangle",
                r"\mathbf r'(0)=\langle1,0,-1\rangle",
            ),
            vector_eq=r"\mathbf v=\langle1,0,-1\rangle",
            line_eq=r"\boxed{\mathbf L(s)=\langle0,-1,-1\rangle+s\langle1,0,-1\rangle}",
        )

    def problem_3b(self) -> None:
        self._tangent_problem(
            header_number=3, audit_id="V3-3B",
            title="3(b) · UNA PROYECCION ESTABLE CERCA DE PI",
            subtitle="La proyeccion y-z evita la escala enorme de x = t e^t y conserva una tangente claramente visible.",
            top_expr=r"\mathbf r(t)=\langle te^t,\,t^2-2t,\,-\tan t\rangle,\qquad t_0=\pi",
            xy=lambda t: (t*t - 2*t, -math.tan(t)), t0=math.pi, t_range=(2.35, 3.85),
            x_range=(0.4, 7.0), y_range=(-1.8, 1.8), direction_2d=(2*math.pi-2, -1.0),
            approach_from=2.45, arrow_scale=0.23, tangent_span=0.36, x_label="y", y_label="z",
            point_eq=r"\mathbf r(\pi)=\langle\pi e^\pi,\,\pi^2-2\pi,\,0\rangle",
            derivative_chain=(
                r"\mathbf r'(t)=\langle e^t(1+t),\,2t-2,\,-\sec^2t\rangle",
                r"\mathbf r'(\pi)=\langle e^\pi(1+\pi),\,2\pi-2,\,-1\rangle",
            ),
            vector_eq=r"\mathbf v=\langle e^\pi(1+\pi),\,2\pi-2,\,-1\rangle",
            line_eq=(r"\boxed{\mathbf L(s)=\langle\pi e^\pi,\pi^2-2\pi,0\rangle"
                     r"+s\langle e^\pi(1+\pi),2\pi-2,-1\rangle}"),
        )

    def problem_3c(self) -> None:
        self._tangent_problem(
            header_number=4, audit_id="V3-3C",
            title="3(c) · LEER EL ORDEN DE COMPONENTES ANTES DE DERIVAR",
            subtitle="La proyeccion x-y produce un punto compacto (0,3) y una direccion visible (2,3/2).",
            top_expr=r"\mathbf r(t)=\left\langle t^3-t,\,\frac{6t}{t+1},\,(2t^2+1)^2\right\rangle,\qquad t_0=1",
            xy=lambda t: (t**3 - t, 6*t/(t+1)), t0=1.0, t_range=(0.15, 1.55),
            x_range=(-0.7, 2.4), y_range=(0.4, 4.2), direction_2d=(2.0, 1.5),
            approach_from=0.25, arrow_scale=0.38, tangent_span=0.75, x_label="x", y_label="y",
            point_eq=r"\mathbf r(1)=\langle0,3,9\rangle",
            derivative_chain=(
                r"\mathbf r'(t)=\left\langle3t^2-1,\,\frac{6}{(t+1)^2},\,8t(2t^2+1)\right\rangle",
                r"\mathbf r'(1)=\left\langle2,\frac32,24\right\rangle",
            ),
            vector_eq=r"\mathbf v=\left\langle2,\frac32,24\right\rangle",
            line_eq=r"\boxed{\mathbf L(s)=\langle0,3,9\rangle+s\left\langle2,\frac32,24\right\rangle}",
        )

    def problem_3d(self) -> None:
        self._tangent_problem(
            header_number=5, audit_id="V3-3D",
            title="3(d) · ESPIRAL AMORTIGUADA Y DIRECCION TANGENTE",
            subtitle="La proyeccion x-y muestra la espiral; en t = 0 la direccion proyectada es (-1,1).",
            top_expr=r"\mathbf r(t)=\langle e^{-t}\cos t,\,e^{-t}\sin t,\,e^{-t}\rangle,\qquad t_0=0",
            xy=lambda t: (math.exp(-t)*math.cos(t), math.exp(-t)*math.sin(t)), t0=0.0, t_range=(-0.55, 1.70),
            x_range=(-0.5, 1.8), y_range=(-1.0, 1.55), direction_2d=(-1.0, 1.0),
            approach_from=-0.45, arrow_scale=0.55, tangent_span=0.85, x_label="x", y_label="y",
            point_eq=r"\mathbf r(0)=\langle1,0,1\rangle",
            derivative_chain=(
                r"\mathbf r'(t)=\langle-e^{-t}(\cos t+\sin t),\,e^{-t}(\cos t-\sin t),\,-e^{-t}\rangle",
                r"\mathbf r'(0)=\langle-1,1,-1\rangle",
            ),
            vector_eq=r"\mathbf v=\langle-1,1,-1\rangle",
            line_eq=r"\boxed{\mathbf L(s)=\langle1,0,1\rangle+s\langle-1,1,-1\rangle}",
        )

    def summary_tangent(self) -> None:
        self.audit("V3-SUM", "tangent method map")
        self.set_header(6, "METODO REPRODUCIBLE",
                        "Cada tangente se construye con dos objetos: un punto de la curva y un vector direccion derivado.")
        route = self.process_map([
            ("1", "EVALUAR r(t0)"),
            ("2", "DERIVAR r(t)"),
            ("3", "EVALUAR r'(t0)"),
            ("4", "DIBUJAR DIRECCION"),
            ("5", "FORMAR P + s v"),
            ("6", "VERIFICAR COMPONENTES"),
        ], columns=3)
        route.move_to(DOWN * 0.25)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in route], lag_ratio=0.10),
                  run_time=2.0, rate_func=smootherstep)
        self.wait(4.2)
        self.standard_closing("Punto de la curva. Derivada como direccion. Recta parametrica verificable.")
