# VIDEO 1 — DOMAINS
# =============================================================================
class Video01_Dominios_VisualSenior(VisualCalculusBase):
    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()
        # Samples validating the stated domains.
        assert 4**2 - 9 >= 0
        assert (-4)**2 - 9 >= 0
        assert 0**2 - 9 < 0
        assert -6 + 6 >= 0
        assert (3**2 - 9) == 0
        assert 2.1 - 2 > 0

    def construct(self) -> None:
        self.latex_opening(
            "PROBLEMA 1: DOMINIO DE FUNCIONES VECTORIALES",
            "Cada componente impone una condicion sobre el mismo parametro t.",
            "Veremos las restricciones como regiones y despues construiremos su interseccion.",
        )
        self.method_map()
        self.part_a()
        self.part_b()
        self.part_c()
        self.part_d()
        self.summary_domain()

    def method_map(self) -> None:
        self.section(1, "IDEA VISUAL: TRES COMPONENTES, UN SOLO DOMINIO",
                     "El parametro t debe atravesar simultaneamente las tres condiciones.")
        formula = self.math_card(r"\operatorname{Dom}(\mathbf r)=D_x\cap D_y\cap D_z", 7.0, 1.08, 42)
        formula.move_to(UP * 1.35)
        gates = VGroup(
            self.restriction_gate("COMPONENTE i", r"x(t)", r"\text{produce }D_x", 3.8),
            self.restriction_gate("COMPONENTE j", r"y(t)", r"\text{produce }D_y", 3.8),
            self.restriction_gate("COMPONENTE k", r"z(t)", r"\text{produce }D_z", 3.8),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.45)
        arrows = VGroup(*[
            Arrow(g.get_bottom(), formula.get_top() + LEFT * (2.0 - i * 2.0), buff=0.15,
                  stroke_width=2.0, color=MID_GRAY) for i, g in enumerate(gates)
        ])
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.12) for g in gates], lag_ratio=0.15), run_time=RUN_SLOW)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def part_a(self) -> None:
        self.section(2, "1(a): LA RAIZ DEFINE DOS REGIONES VALIDAS",
                     "En lugar de memorizar el intervalo, observamos cuando t^2-9 esta sobre o en cero.")
        expr = self.math_card(r"\mathbf r(t)=\sqrt{t^2-9}\,\mathbf i+t^2\,\mathbf j+\mathbf k", 9.4, 1.0, 38)
        expr.move_to(UP * 1.65)

        axes = Axes(x_range=[-5, 5, 1], y_range=[-10, 17, 5], x_length=6.2, y_length=3.0,
                    tips=False, axis_config={"color": MID_GRAY, "stroke_width": 1.4})
        curve = axes.plot(lambda x: x*x - 9, x_range=[-4.6, 4.6], color=BLACK_LINE, stroke_width=2.6)
        zero = Line(axes.c2p(-5,0), axes.c2p(5,0), color=LIGHT_GRAY, stroke_width=2)
        roots = VGroup(Dot(axes.c2p(-3,0), color=BLACK_LINE), Dot(axes.c2p(3,0), color=BLACK_LINE))
        root_labels = VGroup(self.math("-3", 22).next_to(roots[0], DOWN, buff=0.08),
                             self.math("3", 22).next_to(roots[1], DOWN, buff=0.08))
        graph_group = VGroup(axes, zero, curve, roots, root_labels).scale(0.92).move_to(LEFT*3.65 + DOWN*0.45)

        logic = self.equation_stack([
            r"t^2-9\ge 0",
            r"(t-3)(t+3)\ge 0",
            r"t\le -3\quad\text{o}\quad t\ge 3",
        ], sizes=[38,38,38], max_width=5.9)
        logic.move_to(RIGHT*3.6 + DOWN*0.10)

        self.play(FadeIn(expr), run_time=RUN_NORMAL)
        self.play(Create(axes), Create(zero), run_time=RUN_NORMAL)
        self.play(Create(curve), run_time=RUN_SLOW)
        self.play(FadeIn(roots), FadeIn(root_labels), run_time=RUN_NORMAL)
        self.animate_equation_stack(logic, pause=1.25)

        line = self.domain_line(-5,5,[(-5,-3,False,True),(3,5,True,False)], center=RIGHT*3.55+DOWN*2.55, length=5.6)
        self.play(FadeIn(line[0]), run_time=RUN_QUICK)
        self.play(Create(line[1]), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.result_reveal(r"\boxed{\operatorname{Dom}(\mathbf r)=(-\infty,-3]\cup[3,\infty)}", 8.8, 38)
        self.clear_stage()

    def part_b(self) -> None:
        self.section(3, "1(b): TRES COMPONENTES SIN RESTRICCION",
                     "Seno, coseno y exponencial estan definidos para todo numero real.")
        expr = self.math_card(r"\mathbf r(t)=\cos(2t)\,\mathbf i+e^{-t}\,\mathbf j+\sin(2t)\,\mathbf k", 9.4, 1.0, 38)
        expr.move_to(UP*1.75)
        cards = self.component_triplet((r"\cos(2t)", r"e^{-t}", r"\sin(2t)"), width=3.55)
        cards.move_to(LEFT*4.65 + DOWN*0.25)

        axes1 = Axes(x_range=[-3,3,1], y_range=[-1.3,1.3,1], x_length=5.5, y_length=1.55,
                     tips=False, axis_config={"color": MID_GRAY, "stroke_width":1.1})
        g1 = axes1.plot(lambda x: math.cos(2*x), x_range=[-3,3], color=BLACK_LINE, stroke_width=2.2)
        axes2 = Axes(x_range=[-3,3,1], y_range=[0,7,2], x_length=5.5, y_length=1.55,
                     tips=False, axis_config={"color": MID_GRAY, "stroke_width":1.1})
        g2 = axes2.plot(lambda x: math.exp(-x), x_range=[-1.8,3], color=BLACK_LINE, stroke_width=2.2)
        axes3 = Axes(x_range=[-3,3,1], y_range=[-1.3,1.3,1], x_length=5.5, y_length=1.55,
                     tips=False, axis_config={"color": MID_GRAY, "stroke_width":1.1})
        g3 = axes3.plot(lambda x: math.sin(2*x), x_range=[-3,3], color=BLACK_LINE, stroke_width=2.2)
        plots = VGroup(VGroup(axes1,g1),VGroup(axes2,g2),VGroup(axes3,g3)).arrange(DOWN,buff=0.18)
        plots.scale(0.82).move_to(RIGHT*3.45+DOWN*0.35)

        self.play(FadeIn(expr), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(c,shift=RIGHT*0.10) for c in cards],lag_ratio=0.16), run_time=RUN_SLOW)
        for p in plots:
            self.play(Create(p[0]), Create(p[1]), run_time=RUN_NORMAL)
        check = self.text("NINGUNA GRAFICA SE ROMPE POR EL VALOR DE t", 22, BOLD).next_to(plots, DOWN, buff=0.18)
        self.play(FadeIn(check), run_time=RUN_NORMAL)
        all_real = self.domain_line(-5,5,[(-5,5,False,False)], center=DOWN*2.45, length=7.3)
        self.play(FadeIn(all_real[0]), Create(all_real[1]), run_time=RUN_SLOW)
        self.result_reveal(r"\boxed{\operatorname{Dom}(\mathbf r)=\mathbb R}", 6.3, 42)
        self.clear_stage()

    def part_c(self) -> None:
        self.section(4, "1(c): INTERSECCION DE UNA SEMIRRECTA CON DOS HUECOS",
                     "La raiz fija una cota inferior y el denominador elimina dos puntos.")
        expr = self.math_card(r"\mathbf r(t)=\sqrt{t+6}\,\mathbf i+3t\,\mathbf j+\frac{1}{t^2-9}\,\mathbf k", 9.8, 1.0, 36)
        expr.move_to(UP*1.78)
        gate1 = self.restriction_gate("RAIZ", r"t+6\ge0", r"t\ge -6", 4.1)
        gate2 = self.restriction_gate("LINEAL", r"3t", r"\text{sin restriccion}", 4.1)
        gate3 = self.restriction_gate("DENOMINADOR", r"t^2-9\ne0", r"t\ne\pm3", 4.1)
        gates = VGroup(gate1,gate2,gate3).arrange(RIGHT,buff=0.30).scale(0.92).move_to(UP*0.15)

        l1 = self.domain_line(-7,7,[(-6,7,True,False)], center=LEFT*0.2+DOWN*0.95, length=8.2, label="D_i")
        l2 = self.domain_line(-7,7,[(-7,7,False,False)], center=LEFT*0.2+DOWN*1.65, length=8.2, label="D_j")
        l3 = self.domain_line(-7,7,[(-7,7,False,False)], exclusions=[-3,3], center=LEFT*0.2+DOWN*2.35, length=8.2, label="D_k")
        lines=VGroup(l1,l2,l3)

        self.play(FadeIn(expr), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(g,shift=UP*0.12) for g in gates],lag_ratio=0.12), run_time=RUN_SLOW)
        for line in lines:
            self.play(FadeIn(line[0]), Create(line[1]), run_time=RUN_NORMAL)
        inter = self.domain_line(-7,7,[(-6,-3,True,False),(-3,3,False,False),(3,7,False,False)],
                                 exclusions=[-3,3], center=DOWN*2.98, length=8.2, label="INTERSECCION")
        self.play(FadeIn(inter[0]), run_time=RUN_NORMAL)
        self.play(Create(inter[1]), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.result_reveal(r"\boxed{[-6,-3)\cup(-3,3)\cup(3,\infty)}", 8.3, 39)
        self.clear_stage()

    def part_d(self) -> None:
        self.section(5, "1(d): UNA RESTRICCION DOMINA A LA OTRA",
                     "El logaritmo fija una region que ya excluye el punto prohibido del exponencial.")
        expr = self.math_card(r"\mathbf r(t)=\ln(t-2)\,\mathbf i+e^{1/t}\,\mathbf j-\cos(2t)\,\mathbf k", 9.6, 1.0, 36)
        expr.move_to(UP*1.75)
        gates = VGroup(
            self.restriction_gate("LOGARITMO", r"t-2>0", r"t>2", 4.0),
            self.restriction_gate("EXPONENCIAL", r"e^{1/t}", r"t\ne0", 4.0),
            self.restriction_gate("COSENO", r"-\cos(2t)", r"\text{sin restriccion}", 4.0),
        ).arrange(RIGHT,buff=0.30).scale(0.94).move_to(UP*0.25)

        l_log = self.domain_line(-4,7,[(2,7,False,False)],center=UP*-1.05,length=8.0,label="D_i")
        l_exp = self.domain_line(-4,7,[(-4,7,False,False)],exclusions=[0],center=UP*-1.85,length=8.0,label="D_j")
        l_cos = self.domain_line(-4,7,[(-4,7,False,False)],center=UP*-2.65,length=8.0,label="D_k")
        self.play(FadeIn(expr),run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(g,shift=UP*0.10) for g in gates],lag_ratio=0.13),run_time=RUN_SLOW)
        for line in (l_log,l_exp,l_cos):
            self.play(FadeIn(line[0]),Create(line[1]),run_time=RUN_NORMAL)
        dominance = self.math(r"(2,\infty)\subset \mathbb R\setminus\{0\}",34).move_to(RIGHT*4.7+DOWN*2.95)
        self.play(Write(dominance),run_time=RUN_NORMAL)
        self.result_reveal(r"\boxed{\operatorname{Dom}(\mathbf r)=(2,\infty)}",7.6,40)
        self.clear_stage()

    def summary_domain(self) -> None:
        self.section(6,"METODO REPRODUCIBLE","Separar, restringir, intersectar y escribir el resultado.")
        route = self.process_map([
            ("1","SEPARAR COMPONENTES"),("2","BUSCAR RAICES / LOGS"),("3","REVISAR DENOMINADORES"),
            ("4","DIBUJAR CADA DOMINIO"),("5","INTERSECTAR"),("6","ESCRIBIR INTERVALOS")
        ],columns=3)
        route.move_to(DOWN*0.15)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*0.10) for c in route],lag_ratio=0.10),run_time=RUN_SLOW*1.5)
        self.wait(PAUSE_FINAL)
        self.standard_closing("El dominio vectorial es una interseccion de condiciones escalares.")


# =============================================================================
