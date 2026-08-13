# VIDEO 2 — LIMITS
# =============================================================================
class Video02_Limites_VisualSenior(VisualCalculusBase):
    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()
        assert_close(1 + 1, 2, label="2a first")
        assert_close((5*1-1)/(1+1), 2, label="2a second")
        assert_close((2*math.exp(0)-2)/1, 0, label="2a third")
        assert_close(2+3, 5, label="2b first")
        assert_close((4+4-3)/(2-21), -5/19, label="2b second")
        assert_close(math.sqrt(2)-3, math.sqrt(2)-3, label="2b third")

    def construct(self) -> None:
        self.latex_opening(
            "PROBLEMA 2: LIMITES DE FUNCIONES VECTORIALES",
            "El vector converge solo cuando cada componente converge.",
            "Animaremos el parametro acercandose al punto y veremos cada salida estabilizarse.",
        )
        self.limit_idea()
        self.part_a()
        self.part_b()
        self.part_c()
        self.summary_limit()

    def limit_idea(self) -> None:
        self.section(1,"IDEA VISUAL: UN PARAMETRO, TRES SALIDAS","El parametro se aproxima al punto objetivo y las tres coordenadas deben estabilizarse.")
        nl = NumberLine(x_range=[-2,2,1],length=7,include_numbers=True,font_size=24,color=MID_GRAY).move_to(UP*0.45)
        target=Dot(nl.n2p(0),radius=0.09,color=BLACK_LINE)
        left=self.approach_dot(nl,-1.7,0,"t")
        right=self.approach_dot(nl,1.7,0,"t")
        formula=self.math_card(r"\lim_{t\to t_0}\mathbf r(t)=\left\langle\lim x(t),\lim y(t),\lim z(t)\right\rangle",10.2,1.12,39)
        formula.move_to(DOWN*1.65)
        self.play(Create(nl),FadeIn(target),run_time=RUN_NORMAL)
        self.play(FadeIn(left),FadeIn(right),run_time=RUN_NORMAL)
        self.play(left[0].animate.move_to(nl.n2p(-0.15)),right[0].animate.move_to(nl.n2p(0.15)),
                  left[1].animate.next_to(nl.n2p(-0.15),UP,buff=0.08),right[1].animate.next_to(nl.n2p(0.15),UP,buff=0.08),run_time=2.2)
        self.play(FadeIn(formula),run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def component_limit_visual(self, title: str, expr: str, chain: list[str], result: str,
                               position, width=5.8) -> VGroup:
        box = RoundedRectangle(width=width,height=2.55,corner_radius=0.11,stroke_color=BLACK_LINE,
                               stroke_width=1.5,fill_color=WHITE,fill_opacity=1)
        head=self.text(title,21,BOLD)
        eq=self.math(expr,29)
        self.fit(eq,width-0.5,0.55)
        chain_mobs=VGroup(*[self.math(c,27) for c in chain]).arrange(DOWN,aligned_edge=LEFT,buff=0.10)
        self.fit(chain_mobs,width-0.55,1.20)
        res=self.math(result,31)
        content=VGroup(head,eq,chain_mobs,res).arrange(DOWN,buff=0.09)
        self.fit(content,width-0.45,2.25)
        content.move_to(box)
        grp=VGroup(box,content).move_to(position)
        return grp

    def part_a(self) -> None:
        self.section(2,"2(a): CANCELAR SOLO DONDE APARECE 0/0","Las otras componentes se evaluan directamente en t=1.")
        expr=self.math_card(r"\lim_{t\to1}\left\langle\frac{t^2-1}{t-1},\frac{5t-1}{t+1},\frac{2e^{t-1}-2}{t}\right\rangle",11.3,1.05,37)
        expr.move_to(UP*1.70)
        self.play(FadeIn(expr),run_time=RUN_NORMAL)

        # moving input t -> 1
        nl=NumberLine(x_range=[0,2,0.25],length=5.3,include_numbers=True,font_size=18,color=MID_GRAY).move_to(LEFT*4.55+UP*0.10)
        dot=Dot(nl.n2p(0.25),radius=0.08,color=BLACK_LINE)
        targ=Dot(nl.n2p(1),radius=0.09,color=WHITE,stroke_color=BLACK_LINE,stroke_width=2)
        tlabel=self.math("t",22).next_to(dot,UP,buff=0.08)
        self.play(Create(nl),FadeIn(dot),FadeIn(targ),FadeIn(tlabel),run_time=RUN_NORMAL)
        self.play(dot.animate.move_to(nl.n2p(0.93)),tlabel.animate.next_to(nl.n2p(0.93),UP,buff=0.08),run_time=1.8)

        c1=self.component_limit_visual("COMPONENTE i",r"\frac{t^2-1}{t-1}",
                                       [r"\frac{(t-1)(t+1)}{t-1}",r"t+1"],r"\longrightarrow 2",RIGHT*3.25+UP*0.55,5.7)
        c2=self.component_limit_visual("COMPONENTE j",r"\frac{5t-1}{t+1}",
                                       [r"\frac{5(1)-1}{1+1}"],r"\longrightarrow 2",RIGHT*3.25+DOWN*1.70,5.7)
        self.play(FadeIn(c1[0]),run_time=RUN_QUICK)
        self.play(LaggedStart(*[Write(m) for m in c1[1]],lag_ratio=0.18),run_time=RUN_SLOW*1.4)
        self.play(FadeIn(c2[0]),run_time=RUN_QUICK)
        self.play(LaggedStart(*[Write(m) for m in c2[1]],lag_ratio=0.18),run_time=RUN_SLOW*1.4)

        k_card=self.math_card(r"\frac{2e^{t-1}-2}{t}\xrightarrow[t\to1]{}\frac{2e^0-2}{1}=0",6.8,1.02,34)
        k_card.move_to(LEFT*3.8+DOWN*2.15)
        self.play(FadeIn(k_card),run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.result_reveal(r"\boxed{\lim_{t\to1}\mathbf r(t)=\langle2,2,0\rangle}",7.7,40)
        self.clear_stage()

    def part_b(self) -> None:
        self.section(3,"2(b): FACTORIZAR PRIMERO Y LEER LITERALMENTE","Conservamos literalmente la segunda y la tercera componente del taller.")
        expr=self.math_card(r"\lim_{t\to2}\left\langle\frac{t^2+t-6}{t-2},\frac{t^2+2t-3}{t-21},\sqrt t-3\right\rangle",11.5,1.05,36)
        expr.move_to(UP*1.75)
        self.play(FadeIn(expr),run_time=RUN_NORMAL)

        # Three channels ending at result markers.
        cards=VGroup(
            self.restriction_gate("i: REMOVIBLE",r"t^2+t-6=(t-2)(t+3)",r"\Rightarrow t+3\to5",4.2),
            self.restriction_gate("j: SUSTITUCION",r"\frac{4+4-3}{2-21}",r"\Rightarrow -5/19",4.2),
            self.restriction_gate("k: CONTINUA",r"\sqrt2-3",r"\Rightarrow \sqrt2-3",4.2),
        ).arrange(RIGHT,buff=0.25).scale(0.92).move_to(UP*0.25)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*0.10) for c in cards],lag_ratio=0.14),run_time=RUN_SLOW)

        # Visual removable hole for first scalar component y=t+3 except at t=2.
        ax=Axes(x_range=[0,4,1],y_range=[2,8,1],x_length=5.8,y_length=2.65,tips=False,
                axis_config={"color":MID_GRAY,"stroke_width":1.3}).move_to(LEFT*3.9+DOWN*1.65)
        graph=ax.plot(lambda x:x+3,x_range=[0.2,3.8],color=BLACK_LINE,stroke_width=2.4)
        hole=Dot(ax.c2p(2,5),radius=0.09,color=WHITE,stroke_color=BLACK_LINE,stroke_width=2.2)
        approach=Dot(ax.c2p(0.55,3.55),radius=0.075,color=BLACK_LINE)
        hlabel=self.math("t\to2",22).next_to(hole,UR,buff=0.08)
        self.play(Create(ax),Create(graph),FadeIn(hole),FadeIn(approach),FadeIn(hlabel),run_time=RUN_NORMAL)
        self.play(approach.animate.move_to(ax.c2p(1.93,4.93)),run_time=1.8)

        literal=self.latex_note("LECTURA DEL ENUNCIADO",["No se corrige $t-21$ a $t-2$.",r"No se cambia $\sqrt t-3$." ],width=5.6)
        literal.move_to(RIGHT*3.85+DOWN*1.75)
        self.play(FadeIn(literal),run_time=RUN_NORMAL)
        self.result_reveal(r"\boxed{\left\langle5,-\frac5{19},\sqrt2-3\right\rangle}",7.1,40)
        self.clear_stage()

    def part_c(self) -> None:
        self.section(4,"2(c): IDENTIDAD TRIGONOMETRICA + ORDEN DE MAGNITUD","La primera componente se simplifica; la segunda cae a cero; la tercera es continua.")
        expr=self.math_card(r"\lim_{t\to0}\left\langle\frac{1-\cos^2t}{1-\cos t},t^2\sin t,e^{-t+1}\right\rangle",11.2,1.05,36)
        expr.move_to(UP*1.70)
        self.play(FadeIn(expr),run_time=RUN_NORMAL)

        chain=self.transform_equation_chain([
            r"\frac{1-\cos^2t}{1-\cos t}",
            r"\frac{(1-\cos t)(1+\cos t)}{1-\cos t}",
            r"1+\cos t\xrightarrow[t\to0]{}2",
        ],size=38,position=LEFT*3.65+UP*0.25,pause=1.0)

        # t^2 sin t: envelope |t^2 sin t| <= t^2
        ax=Axes(x_range=[-1.4,1.4,0.5],y_range=[-1.0,1.0,0.5],x_length=5.8,y_length=2.7,
                tips=False,axis_config={"color":MID_GRAY,"stroke_width":1.2}).move_to(RIGHT*3.6+UP*0.10)
        g=ax.plot(lambda x:x*x*math.sin(x),x_range=[-1.3,1.3],color=BLACK_LINE,stroke_width=2.4)
        up=ax.plot(lambda x:x*x,x_range=[-1.0,1.0],color=MID_GRAY,stroke_width=1.4)
        lo=ax.plot(lambda x:-x*x,x_range=[-1.0,1.0],color=MID_GRAY,stroke_width=1.4)
        zero=Dot(ax.c2p(0,0),radius=0.08,color=BLACK_LINE)
        self.play(Create(ax),Create(up),Create(lo),Create(g),FadeIn(zero),run_time=RUN_SLOW)
        squeeze=self.math(r"|t^2\sin t|\le t^2\to0",30).next_to(ax,DOWN,buff=0.12)
        self.play(Write(squeeze),run_time=RUN_NORMAL)

        exp=self.math_card(r"e^{-t+1}\xrightarrow[t\to0]{}e^1=e",5.8,0.95,34)
        exp.move_to(DOWN*2.25)
        self.play(FadeIn(exp),run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.result_reveal(r"\boxed{\lim_{t\to0}\mathbf r(t)=\langle2,0,e\rangle}",7.7,40)
        self.clear_stage()

    def summary_limit(self) -> None:
        self.section(5,"METODO REPRODUCIBLE","Detectar indeterminaciones solo donde existen; despues recomponer el vector.")
        route=self.process_map([
            ("1","SEPARAR i,j,k"),("2","SUSTITUIR t_0"),("3","DETECTAR 0/0"),
            ("4","SIMPLIFICAR"),("5","EVALUAR"),("6","RECOMPONER VECTOR")
        ],columns=3)
        route.move_to(DOWN*0.20)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*0.10) for c in route],lag_ratio=0.10),run_time=RUN_SLOW*1.5)
        self.wait(PAUSE_FINAL)
        self.standard_closing("Un limite vectorial es tres limites escalares coordinados.")


# =============================================================================
# VIDEO 3 — TANGENT LINES
# =============================================================================
class Video03_RectasTangentes_VisualSenior(VisualCalculusBase):
    def validate_lesson_data(self) -> None:
        super().validate_lesson_data()
        # Problem 3 exact point/derivative checks.
        assert_close(math.sin(0),0,label="3a x0")
        assert_close(0**2-math.cos(0),-1,label="3a y0")
        assert_close(-math.exp(0),-1,label="3a z0")
        assert_close(math.exp(math.pi)*(1+math.pi), math.exp(math.pi)*(1+math.pi), label="3b dx")
        assert_close(6/(1+1)**2,1.5,label="3c dy")
        assert_close(8*1*(2*1**2+1),24,label="3c dz")

    def construct(self) -> None:
        self.latex_opening(
            "PROBLEMA 3: RECTA TANGENTE A UNA CURVA VECTORIAL",
