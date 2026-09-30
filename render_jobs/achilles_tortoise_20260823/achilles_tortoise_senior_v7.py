from manim import *
from jp_classroom_style import (
    JPClassroomScene,
    BLACK_TEXT,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    PAPER_GRAY,
    RUN_QUICK,
    RUN_NORMAL,
    RUN_SLOW,
    RUN_CAMERA,
    PAUSE_SHORT,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_SUMMARY,
    PAUSE_FINAL,
)


class AchillesTortoiseSenior(JPClassroomScene):
    """Senior classroom reconstruction of Achilles and the Tortoise.

    Narrative contract:
    1. Solve the physical catch problem first, step by step.
    2. Compute the catch position as a separate step.
    3. Verify the meeting visually.
    4. Restart from t=0 and introduce Zeno's description.
    5. Magnify the remaining gap stage by stage without deep-camera artifacts.
    6. Resolve the paradox with a convergent geometric series.
    """

    V_A = 10.0
    V_T = 1.0
    X_A0 = 0.0
    X_T0 = 10.0
    T_CATCH = 10.0 / 9.0
    X_CATCH = 100.0 / 9.0

    def validate_lesson_data(self):
        assert abs(self.T_CATCH - self.X_T0 / (self.V_A - self.V_T)) < 1e-12
        assert abs(self.X_CATCH - self.V_A * self.T_CATCH) < 1e-12
        assert abs(self.X_CATCH - (self.X_T0 + self.V_T * self.T_CATCH)) < 1e-12
        for n in range(4):
            dt = 10 ** (-n)
            gap = 10 ** (-n)
            assert dt > 0 and gap > 0

    def fresh_header(self, number, title, subtitle):
        for mob in (self.header_group, self.subtitle_group):
            if mob is not None:
                self.remove(mob)
        self.header_group = None
        self.subtitle_group = None
        self.set_header(number, title, subtitle)

    def step_row(self, number, equation, caption, y):
        badge_box = RoundedRectangle(
            width=0.64,
            height=0.52,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        badge = VGroup(badge_box, self.text(str(number), 23, BOLD).move_to(badge_box))
        eq = self.math(equation, 40)
        cap = self.text(caption, 21)
        body = VGroup(eq, cap).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        row = VGroup(badge, body).arrange(RIGHT, buff=0.30)
        row.move_to([-5.85, y, 0], aligned_edge=LEFT)
        self.fit(row, 12.5, 1.0)
        return row

    def make_track(self, y=-0.8):
        return NumberLine(
            x_range=[0, 13, 1],
            length=13.0,
            include_numbers=True,
            font_size=19,
            color=BLACK_LINE,
            stroke_width=2,
            tick_size=0.08,
            decimal_number_config={"color": BLACK_TEXT},
        ).move_to([0, y, 0])

    def meeting_solution(self):
        self.fresh_header(
            1,
            "PRIMERO RESOLVEMOS EL ENCUENTRO",
            "Antes de la paradoja: calculamos paso a paso el tiempo y la posición donde Aquiles alcanza a la tortuga.",
        )

        givens = VGroup(
            self.math(r"v_A=10\,\mathrm{m/s}", 34),
            self.math(r"v_T=1\,\mathrm{m/s}", 34),
            self.math(r"x_A(0)=0\,\mathrm{m}", 34),
            self.math(r"x_T(0)=10\,\mathrm{m}", 34),
        ).arrange(RIGHT, buff=0.65)
        self.fit(givens, 13.7, 0.70)
        givens.move_to([0, 2.02, 0])
        lead = self.text("Ventaja inicial de la tortuga: 10 m", 23, BOLD).next_to(givens, DOWN, buff=0.10)
        self.play(Write(givens), Write(lead), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        rows = [
            self.step_row(1, r"x_A(t)=0+10t=10t", "Ecuación de posición de Aquiles", 0.90),
            self.step_row(2, r"x_T(t)=10+1t=10+t", "Ecuación de posición de la tortuga", -0.05),
            self.step_row(3, r"x_A=x_T\Rightarrow 10t=10+t", "En el encuentro ocupan la misma posición", -1.00),
            self.step_row(4, r"10t-t=10\Rightarrow 9t=10", "Aislamos los términos con t", -1.95),
            self.step_row(5, r"t=\frac{10}{9}=1.111\ldots\,\mathrm{s}", "Tiempo de encuentro", -2.90),
        ]
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT)

        time_box = SurroundingRectangle(rows[-1], buff=0.10, color=BLACK_LINE, stroke_width=2.4)
        self.play(Create(time_box), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)
        self.play(*[FadeOut(m) for m in [givens, lead, *rows, time_box]], run_time=RUN_NORMAL)

        subtitle = self.text("Con el tiempo calculado, determinamos ahora la posición.", 30, BOLD)
        self.fit(subtitle, 13.5, 0.60)
        subtitle.move_to([0, 1.85, 0])
        self.play(Write(subtitle), run_time=RUN_NORMAL)

        pos_rows = [
            self.step_row(6, r"x_A=10t", "Partimos de la posición de Aquiles", 0.65),
            self.step_row(7, r"x_A=10\left(\frac{10}{9}\right)", "Sustituimos t = 10/9 s", -0.35),
            self.step_row(8, r"x_A=\frac{100}{9}=11.111\ldots\,\mathrm{m}", "Posición de encuentro", -1.35),
        ]
        for row in pos_rows:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT)

        result = VGroup(
            self.math(r"\boxed{t^*=\frac{10}{9}\,\mathrm{s}\approx1.111\,\mathrm{s}}", 42),
            self.math(r"\boxed{x^*=\frac{100}{9}\,\mathrm{m}\approx11.111\,\mathrm{m}}", 42),
        ).arrange(DOWN, buff=0.24).move_to([3.75, -2.85, 0])
        self.fit(result, 7.2, 1.45)
        self.play(Write(result), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage(keep_header=True)

    def verify_meeting(self):
        self.fresh_header(
            2,
            "VERIFICACIÓN DEL ENCUENTRO",
            "La animación avanza hasta t = 10/9 s; las dos trayectorias coinciden en x = 100/9 m.",
        )
        track = self.make_track()
        timer = ValueTracker(0.0)

        a_dot = always_redraw(lambda: Dot(
            track.n2p(self.V_A * timer.get_value()) + UP * 0.45,
            radius=0.10,
            color=BLACK,
        ))
        t_dot = always_redraw(lambda: Square(
            side_length=0.18,
            stroke_color=DARK_GRAY,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        ).move_to(track.n2p(self.X_T0 + self.V_T * timer.get_value()) + DOWN * 0.45))
        a_label = always_redraw(lambda: self.text("Aquiles", 19, BOLD).next_to(a_dot, UP, buff=0.06))
        t_label = always_redraw(lambda: self.text("Tortuga", 19, BOLD).next_to(t_dot, DOWN, buff=0.06))
        clock = always_redraw(lambda: VGroup(
            self.text("t =", 27, BOLD),
            DecimalNumber(timer.get_value(), num_decimal_places=3, font_size=30, color=BLACK_TEXT),
            self.text("s", 27),
        ).arrange(RIGHT, buff=0.10).move_to([0, 1.90, 0]))

        self.play(Create(track), run_time=RUN_NORMAL)
        self.add(a_dot, t_dot, a_label, t_label, clock)
        self.play(timer.animate.set_value(self.T_CATCH), run_time=4.2, rate_func=linear)

        x = track.n2p(self.X_CATCH)[0]
        meet_line = DashedLine([x, -2.05, 0], [x, 0.70, 0], color=MID_GRAY, dash_length=0.08)
        meet = VGroup(
            self.math(r"t^*=\frac{10}{9}\,\mathrm{s}", 30),
            self.math(r"x^*=\frac{100}{9}\,\mathrm{m}", 30),
        ).arrange(DOWN, buff=0.08).next_to(meet_line, UP, buff=0.10)
        conclusion = self.text("Aquiles sí alcanza a la tortuga.", 32, BOLD).move_to([0, -3.20, 0])
        self.play(Create(meet_line), Write(meet), run_time=RUN_NORMAL)
        self.play(Write(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.remove(a_dot, t_dot, a_label, t_label, clock)
        self.clear_stage(keep_header=True)

    def zeno_intro(self):
        self.fresh_header(
            3,
            "REINICIAMOS LA CARRERA: AHORA PENSAMOS COMO ZENÓN",
            "Zenón describe el mismo recorrido como una secuencia infinita de metas intermedias cada vez más pequeñas.",
        )
        statement = self.text(
            "La paradoja no cambia las velocidades: cambia la forma de dividir el recorrido.",
            30,
            BOLD,
        )
        self.fit(statement, 13.4, 0.60)
        statement.move_to([0, 1.85, 0])
        self.play(Write(statement), run_time=RUN_NORMAL)

        chain = self.math(r"10\,\mathrm{m}\rightarrow1\,\mathrm{m}\rightarrow0.1\,\mathrm{m}\rightarrow0.01\,\mathrm{m}\rightarrow\cdots", 42)
        self.fit(chain, 12.8, 0.75)
        chain.move_to([0, 0.65, 0])
        self.play(Write(chain), run_time=RUN_SLOW)

        steps = VGroup(
            self.text("1. Aquiles llega a 10 m; la tortuga ya está en 11 m.", 25),
            self.text("2. Aquiles llega a 11 m; la tortuga ya está en 11.1 m.", 25),
            self.text("3. Aquiles llega a 11.1 m; la tortuga ya está en 11.11 m.", 25),
            self.text("4. Siempre puede definirse una etapa todavía más pequeña.", 25, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(steps, 13.3, 2.1)
        steps.move_to([0, -1.30, 0])
        self.play(LaggedStart(*[Write(s) for s in steps], lag_ratio=0.20), run_time=RUN_SLOW)
        prompt = self.text("Ahora hacemos ZOOM ×10 en cada intervalo.", 31, BOLD).move_to([0, -3.35, 0])
        self.play(Write(prompt), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage(keep_header=True)

    def stage_panel(self, stage, xa, xt, gap, dt):
        box = RoundedRectangle(
            width=13.0,
            height=3.45,
            corner_radius=0.14,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to([0, -1.25, 0])
        title = self.text(f"ETAPA {stage} — INTERVALO AMPLIADO ×10", 27, BOLD).move_to([0, -0.02, 0])
        line = Line([-4.85, -1.35, 0], [4.85, -1.35, 0], color=BLACK_LINE, stroke_width=2)
        a = Dot([-4.1, -1.10, 0], radius=0.10, color=BLACK)
        t = Square(side_length=0.20, stroke_color=DARK_GRAY, fill_color=PAPER_GRAY, fill_opacity=1).move_to([4.1, -1.60, 0])
        labels = VGroup(
            self.math(rf"x_A={xa}\,\mathrm{{m}}", 31).move_to([-3.65, -2.15, 0]),
            self.math(rf"x_T={xt}\,\mathrm{{m}}", 31).move_to([3.65, -2.15, 0]),
        )
        measure = Line([-4.1, -2.65, 0], [4.1, -2.65, 0], color=MID_GRAY, stroke_width=1.8)
        ticks = VGroup(
            Line([-4.1, -2.75, 0], [-4.1, -2.55, 0], color=MID_GRAY),
            Line([4.1, -2.75, 0], [4.1, -2.55, 0], color=MID_GRAY),
        )
        gap_label = self.math(rf"d_{stage}={gap}\,\mathrm{{m}}", 31).next_to(measure, DOWN, buff=0.08)
        dt_label = self.math(rf"\Delta t_{stage}={dt}\,\mathrm{{s}}", 31).move_to([0, -0.62, 0])
        return VGroup(box, title, line, a, t, labels, measure, ticks, gap_label, dt_label)

    def zeno_zoom(self):
        self.fresh_header(
            4,
            "ZOOM PASO A PASO DE LA PARADOJA",
            "La barra superior mantiene el contexto; abajo ampliamos diez veces el intervalo seleccionado en cada etapa.",
        )

        context = NumberLine(
            x_range=[9.8, 11.2, 0.2],
            length=11.2,
            include_numbers=False,
            color=BLACK_LINE,
            stroke_width=2,
            tick_size=0.07,
        ).move_to([0, 1.45, 0])
        context_title = self.text("CONTEXTO CERCA DEL PUNTO DE ENCUENTRO", 22, BOLD).move_to([0, 2.03, 0])
        labels = VGroup(
            self.math("10", 23).next_to(context.n2p(10.0), DOWN, buff=0.08),
            self.math("11", 23).next_to(context.n2p(11.0), DOWN, buff=0.08),
            self.math("11.1", 23).next_to(context.n2p(11.1), UP, buff=0.08),
        )
        self.play(Create(context), Write(context_title), Write(labels), run_time=RUN_NORMAL)

        data = [
            (1, 10.0, 11.0, "10", "11", "1", "1"),
            (2, 11.0, 11.1, "11", "11.1", "0.1", "0.1"),
            (3, 11.1, 11.11, "11.1", "11.11", "0.01", "0.01"),
            (4, 11.11, 11.111, "11.11", "11.111", "0.001", "0.001"),
        ]

        def focus_rect(xa, xt):
            x1, x2 = context.n2p(xa)[0], context.n2p(xt)[0]
            w = max(abs(x2 - x1), 0.10)
            return Rectangle(
                width=w,
                height=0.50,
                stroke_color=BLACK_LINE,
                stroke_width=2,
                fill_color=PAPER_GRAY,
                fill_opacity=0.35,
            ).move_to([(x1 + x2) / 2, context.get_center()[1], 0])

        first = data[0]
        focus = focus_rect(first[1], first[2])
        panel = self.stage_panel(first[0], first[3], first[4], first[5], first[6])
        zoom = self.text("ZOOM ×10", 25, BOLD).move_to([0, 0.35, 0])
        arrow = Arrow([focus.get_center()[0], 1.05, 0], [0, 0.22, 0], buff=0.10, color=MID_GRAY, stroke_width=2)
        self.play(Create(focus), GrowArrow(arrow), Write(zoom), run_time=RUN_NORMAL)
        self.play(FadeIn(panel), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)

        for stage, a_num, t_num, xa, xt, gap, dt in data[1:]:
            new_focus = focus_rect(a_num, t_num)
            new_panel = self.stage_panel(stage, xa, xt, gap, dt)
            self.play(
                Transform(focus, new_focus),
                ReplacementTransform(panel, new_panel),
                Indicate(zoom, scale_factor=1.10),
                run_time=RUN_CAMERA,
            )
            panel = new_panel
            self.wait(PAUSE_EXPLAIN)

        finite = self.text(
            "En toda etapa finita queda una distancia positiva; el zoom puede repetirse indefinidamente.",
            24,
            BOLD,
        )
        self.fit(finite, 13.1, 0.58)
        finite.move_to([0, -3.62, 0])
        self.play(Write(finite), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(panel), FadeOut(focus), FadeOut(arrow), FadeOut(zoom), FadeOut(finite), run_time=RUN_NORMAL)

        pattern = VGroup(
            self.text("Distancias restantes:", 28, BOLD),
            self.math(r"1,\;0.1,\;0.01,\;0.001,\ldots", 42),
            self.math(r"d_n=10\left(\frac{1}{10}\right)^n>0\quad\text{para todo }n\text{ finito}", 37),
            self.math(r"\lim_{n\to\infty}d_n=0", 42),
        ).arrange(DOWN, buff=0.24).move_to([0, -1.30, 0])
        self.fit(pattern, 13.4, 3.4)
        self.play(LaggedStart(*[Write(m) for m in pattern], lag_ratio=0.20), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage(keep_header=True)

    def resolution(self):
        self.fresh_header(
            5,
            "LA CLAVE: INFINITAS ETAPAS NO SIGNIFICAN TIEMPO INFINITO",
            "Los tiempos de cada etapa disminuyen geométricamente y su suma converge exactamente al tiempo de encuentro.",
        )
        series = VGroup(
            self.math(r"T=1+0.1+0.01+0.001+\cdots", 44),
            self.math(r"T=\sum_{n=0}^{\infty}\left(\frac{1}{10}\right)^n", 44),
            self.math(r"T=\frac{1}{1-\frac{1}{10}}=\frac{10}{9}=1.111\ldots\,\mathrm{s}", 44),
        ).arrange(DOWN, buff=0.34).move_to([0, 0.45, 0])
        self.play(LaggedStart(*[Write(m) for m in series], lag_ratio=0.30), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)

        position = self.math(r"10+1+0.1+0.01+\cdots=\frac{100}{9}=11.111\ldots\,\mathrm{m}", 40)
        position.move_to([0, -2.0, 0])
        self.play(Write(position), run_time=RUN_SLOW)
        final = self.text("INFINITAS ETAPAS  ≠  TIEMPO INFINITO", 34, BOLD).move_to([0, -3.25, 0])
        self.play(Write(final), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage(keep_header=True)

        self.fresh_header(
            6,
            "MISMO RESULTADO, DOS DESCRIPCIONES",
            "El cálculo de MRU y la serie de Zenón conducen al mismo tiempo y a la misma posición de encuentro.",
        )
        left = self.note_panel(
            "MRU",
            ["x_A = 10t", "x_T = 10 + t", "10t = 10 + t", "t = 10/9 s", "x = 100/9 m"],
            width=6.2,
            body_size=24,
        ).move_to([-3.45, 0.25, 0])
        right = self.note_panel(
            "ZENÓN",
            ["1 s", "+ 0.1 s", "+ 0.01 s", "+ 0.001 s + ...", "suma = 10/9 s"],
            width=6.2,
            body_size=24,
        ).move_to([3.45, 0.25, 0])
        self.play(FadeIn(left, shift=RIGHT * 0.12), FadeIn(right, shift=LEFT * 0.12), run_time=RUN_SLOW)
        answer = VGroup(
            self.math(r"\boxed{t=\frac{10}{9}\,\mathrm{s}}", 43),
            self.math(r"\boxed{x=\frac{100}{9}\,\mathrm{m}}", 43),
        ).arrange(RIGHT, buff=1.25).move_to([0, -2.55, 0])
        self.play(Write(answer), run_time=RUN_SLOW)
        takeaway = self.text(
            "La paradoja surge al confundir una cantidad infinita de subdivisiones con una duración infinita.",
            27,
            BOLD,
        )
        self.fit(takeaway, 13.7, 0.58)
        takeaway.move_to([0, -3.48, 0])
        self.play(Write(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)

    def construct(self):
        self.meeting_solution()
        self.verify_meeting()
        self.zeno_intro()
        self.zeno_zoom()
        self.resolution()
