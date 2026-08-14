        # Three algebra cards on the right, one at a time.
        anchors = [RIGHT * 3.55 + UP * 0.75, RIGHT * 3.55 + DOWN * 0.25, RIGHT * 3.55 + DOWN * 1.25]
        finals = []
        badges = [r"\mathbf i", r"\mathbf j", r"\mathbf k"]
        for badge, chain, anchor in zip(badges, chains, anchors):
            badge_mob = self.math(badge, 27).move_to(anchor + LEFT * 2.65)
            self.play(FadeIn(badge_mob), run_time=0.45)
            fin = self.animate_matching_chain(chain, position=anchor + RIGHT * 0.15,
                                              font_size=31, max_width=5.35,
                                              pauses=[1.2] + [1.55] * (len(chain)-1))
            finals.append(fin)
        if note:
            note_panel = self.note_panel(note[0], list(note[1]), width=5.9, title_size=22, body_size=19)
            note_panel.move_to(RIGHT * 3.55 + DOWN * 2.30)
            self.play(FadeIn(note_panel, shift=UP * 0.06), run_time=0.9)
            self.wait(2.3)
        result = self.result_panel(final_vector, width=6.1, font_size=37)
        result.move_to(RIGHT * 3.55 + DOWN * 2.55)
        if note:
            self.play(FadeOut(note_panel), run_time=0.6)
        self.play(
            FadeIn(result[0]),
            TransformFromCopy(VGroup(*finals), result[1]),
            run_time=1.7,
            rate_func=smootherstep,
        )
        self.wait(4.0)
        self.clear_stage()

    def problem_2a(self) -> None:
        self._limit_problem(
            header_number=2,
            audit_id="V2-2A",
            title="2(a) · SIMPLIFICAR SOLO DONDE APARECE LA INDETERMINACION",
            subtitle="La primera componente tiene 0/0 y se factoriza; las otras dos permiten sustitucion directa.",
            top_expr=(r"\lim_{t\to1}\left\langle\frac{t^2-1}{t-1},"
                      r"\frac{5t-1}{t+1},\frac{2e^{t-1}-2}{t}\right\rangle"),
            t0=1.0,
            funcs=(lambda t: t + 1, lambda t: (5*t - 1)/(t + 1), lambda t: (2*math.exp(t-1)-2)/t),
            plot_x_range=(0.25, 1.75),
            y_ranges=((1.0, 3.0), (0.3, 3.1), (-1.1, 1.1)),
            chains=(
                (r"\frac{t^2-1}{t-1}", r"\frac{(t-1)(t+1)}{t-1}", r"t+1\to2"),
                (r"\frac{5t-1}{t+1}", r"\frac{5(1)-1}{1+1}=2"),
                (r"\frac{2e^{t-1}-2}{t}", r"\frac{2e^0-2}{1}=0"),
            ),
            final_vector=r"\boxed{\langle2,2,0\rangle}",
        )

    def problem_2b(self) -> None:
        self._limit_problem(
            header_number=3,
            audit_id="V2-2B",
            title="2(b) · FACTORIZAR PRIMERO Y LEER LITERALMENTE",
            subtitle="Se conserva la lectura del taller: denominador t-21 en j y tercera componente sqrt(t)-3.",
            top_expr=(r"\lim_{t\to2}\left\langle\frac{t^2+t-6}{t-2},"
                      r"\frac{t^2+2t-3}{t-21},\sqrt t-3\right\rangle"),
            t0=2.0,
            funcs=(lambda t: t + 3, lambda t: (t*t + 2*t - 3)/(t - 21), lambda t: math.sqrt(t) - 3),
            plot_x_range=(0.7, 3.3),
            y_ranges=((3.2, 6.8), (-0.65, 0.05), (-2.3, -1.0)),
            chains=(
                (r"\frac{t^2+t-6}{t-2}", r"\frac{(t+3)(t-2)}{t-2}", r"t+3\to5"),
                (r"\frac{t^2+2t-3}{t-21}", r"\frac{4+4-3}{2-21}=-\frac5{19}"),
                (r"\sqrt t-3", r"\sqrt2-3"),
            ),
            final_vector=r"\boxed{\left\langle5,-\frac5{19},\sqrt2-3\right\rangle}",
            note=("LECTURA AUDITABLE", ["No se corrige silenciosamente el enunciado.", "Se resuelve exactamente la expresion escrita en el taller."]),
        )

    def problem_2c(self) -> None:
        self._limit_problem(
            header_number=4,
            audit_id="V2-2C",
            title="2(c) · IDENTIDAD TRIGONOMETRICA Y ORDEN DE MAGNITUD",
            subtitle="La primera componente se simplifica; la segunda cae a cero; la exponencial se evalua directamente.",
            top_expr=(r"\lim_{t\to0}\left\langle\frac{1-\cos^2t}{1-\cos t},"
                      r"t^2\sin t,e^{-t+1}\right\rangle"),
            t0=0.0,
            funcs=(lambda t: 1 + math.cos(t), lambda t: t*t*math.sin(t), lambda t: math.exp(-t+1)),
            plot_x_range=(-0.9, 0.9),
            y_ranges=((1.45, 2.05), (-0.7, 0.7), (1.0, 6.8)),
            chains=(
                (r"\frac{1-\cos^2t}{1-\cos t}",
                 r"\frac{(1-\cos t)(1+\cos t)}{1-\cos t}", r"1+\cos t\to2"),
                (r"t^2\sin t", r"|t^2\sin t|\le t^2\to0"),
                (r"e^{-t+1}", r"e^{1}=e"),
            ),
            final_vector=r"\boxed{\langle2,0,e\rangle}",
        )

    def summary_limit(self) -> None:
        self.audit("V2-SUM", "limit method map")
        self.set_header(5, "METODO REPRODUCIBLE",
                        "La estructura siempre es la misma: inspeccionar, simplificar solo si hace falta, evaluar y rearmar.")
        route = self.process_map([
            ("1", "SEPARAR i, j, k"),
            ("2", "PROBAR SUSTITUCION"),
            ("3", "DETECTAR 0/0"),
            ("4", "SIMPLIFICAR"),
            ("5", "EVALUAR"),
            ("6", "REARMAR VECTOR"),
        ], columns=3)
        route.move_to(DOWN * 0.25)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in route], lag_ratio=0.10),
                  run_time=2.0, rate_func=smootherstep)
        self.wait(4.2)
        self.standard_closing("Mismo parametro. Tres limites escalares. Un vector final.")


# =============================================================================
# VIDEO 3 — TANGENT LINES
# =============================================================================
class Video03_Tangentes_Auditable(WorkshopBase):
    def construct(self) -> None:
        self.audit("V3-START", "Video 3 tangent lines")
        self.standard_opening(
            "CALCULO DE VARIAS VARIABLES · TALLER 1",
            "RECTA TANGENTE A UNA CURVA VECTORIAL",
            "El punto fija la posicion; la derivada fija la direccion.",
            "Ver la secante convertirse en tangente antes de escribir la formula.",
        )
        self.intro_secant()
        self.problem_3a()
        self.problem_3b()
        self.problem_3c()
        self.problem_3d()
        self.summary_tangent()
        self.audit("V3-END", "Video 3 complete")

    def intro_secant(self) -> None:
        self.audit("V3-01", "dynamic secant to tangent")
        self.set_header(1, "DE SECANTE A TANGENTE",
                        "Cuando el segundo punto se acerca al primero, la direccion de la secante converge a la direccion derivada.")
        ax = Axes(x_range=[-2.5, 3.0, 1], y_range=[-0.5, 3.6, 1], x_length=7.0, y_length=4.1,
                  tips=False, axis_config={"color": MID_GRAY, "stroke_width": 1.5, "include_ticks": False})
        curve = ax.plot(lambda x: 0.42*x*x + 0.15, x_range=[-2.2, 2.6], color=BLACK_LINE, stroke_width=2.8)
        x0 = 0.40
        p0 = Dot(ax.c2p(x0, 0.42*x0*x0 + 0.15), radius=0.085, color=BLACK_LINE)
        h = ValueTracker(1.9)
        p1 = always_redraw(lambda: Dot(ax.c2p(x0 + h.get_value(), 0.42*(x0+h.get_value())**2 + 0.15),
                                       radius=0.070, color=BLACK_LINE))
        secant = always_redraw(lambda: Line(p0.get_center(), p1.get_center(), color=MID_GRAY, stroke_width=2.1).scale(2.0))
        tangent_slope = 0.84*x0
        tangent = Line(ax.c2p(-1.7, (0.42*x0*x0+0.15) + tangent_slope*(-1.7-x0)),
                       ax.c2p(2.5, (0.42*x0*x0+0.15) + tangent_slope*(2.5-x0)),
                       color=BLACK_LINE, stroke_width=2.7)
        visual = VGroup(ax, curve, p0)
        panel = self.figure_panel(visual, width=8.0, height=5.0, title="LIMITE GEOMETRICO DE SECANTES",
                                  caption="El movimiento es continuo: h disminuye y la secante estabiliza su direccion.")
        panel.group.move_to(LEFT * 2.55 + DOWN * 0.42)
        self.play(FadeIn(panel.box), FadeIn(panel.title), FadeIn(panel.caption), run_time=0.9)
        self.play(Create(ax), Create(curve), FadeIn(p0), run_time=1.5, rate_func=smootherstep)
        self.add(secant, p1)
        self.wait(1.3)
        self.play(h.animate.set_value(0.16), run_time=5.0, rate_func=smootherstep)
        self.wait(1.2)
        self.play(FadeOut(secant), FadeOut(p1), Create(tangent), run_time=1.35, rate_func=smootherstep)
        self.wait(2.4)
        formulas = VGroup(
            self.formula_panel(r"\mathbf v=\mathbf r'(t_0)", width=4.7, height=1.0, font_size=39),
            self.formula_panel(r"\mathbf L(s)=\mathbf r(t_0)+s\,\mathbf r'(t_0)", width=5.4, height=1.1, font_size=35),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 4.9 + DOWN * 0.40)
        self.play(LaggedStart(FadeIn(formulas[0]), FadeIn(formulas[1]), lag_ratio=0.28), run_time=1.7)
        self.wait(3.5)
        self.clear_stage()

    def _tangent_problem(
        self,
        *,
