from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# Physics 9 — From constant velocity to realistic motion
# ManimCE 0.20.x | 1920x1080 | 30 fps
# ---------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BG = WHITE
INK = "#111111"
GRAY = "#6B7280"
LIGHT = "#E5E7EB"
BLUE = "#2563EB"
RED = "#DC2626"
AMBER = "#D97706"
GREEN = "#059669"
PURPLE = "#7C3AED"


class VariableVelocityRealWorld(Scene):
    """
    Grade 9 conceptual bridge:
    MRU (constant velocity) -> realistic motion with changing velocity.

    Scenario:
    One car travels about 80 km from City A to City B.
    Along the route it:
      1) accelerates and cruises,
      2) stops to eat,
      3) resumes,
      4) slows near an accident,
      5) crawls through traffic,
      6) speeds up again.

    The lesson explicitly distinguishes:
      - idealized piecewise-constant descriptions,
      - smoother real transitions,
      - instantaneous velocity,
      - acceleration as change in velocity.
    """

    def construct(self):
        self.opening()
        self.constant_velocity_reference()
        self.real_route_story()
        self.position_time_analysis()
        self.velocity_time_analysis()
        self.acceleration_bridge()
        self.final_summary()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def title(self, text, size=42, color=INK):
        return Text(text, font_size=size, color=color, weight=BOLD)

    def body(self, text, size=28, color=INK):
        return Text(text, font_size=size, color=color)

    def section_header(self, number, title, subtitle):
        n = Text(str(number), font_size=30, color=WHITE, weight=BOLD)
        badge = Circle(radius=0.34, fill_color=INK, fill_opacity=1, stroke_width=0)
        n.move_to(badge)
        main = self.title(title, 34)
        sub = self.body(subtitle, 22, GRAY)
        g = VGroup(VGroup(badge, n), main, sub)
        g[0].to_corner(UL, buff=0.5)
        main.next_to(g[0], RIGHT, buff=0.25).align_to(g[0], UP)
        sub.next_to(main, DOWN, buff=0.08).align_to(main, LEFT)
        line = Line(
            np.array([-7.5, 2.7, 0]),
            np.array([7.5, 2.7, 0]),
            stroke_color=LIGHT,
            stroke_width=2,
        )
        return VGroup(g, line)

    def clear_all(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.55)

    def car(self, color=BLUE):
        body = RoundedRectangle(
            width=1.0, height=0.38, corner_radius=0.08,
            stroke_color=INK, stroke_width=2,
            fill_color=color, fill_opacity=1
        )
        roof = Polygon(
            [-0.28, 0.19, 0], [-0.10, 0.44, 0], [0.28, 0.44, 0], [0.42, 0.19, 0],
            stroke_color=INK, stroke_width=2, fill_color=color, fill_opacity=1
        )
        w1 = Circle(0.10, color=INK, fill_color=INK, fill_opacity=1).move_to([-0.30, -0.22, 0])
        w2 = Circle(0.10, color=INK, fill_color=INK, fill_opacity=1).move_to([0.30, -0.22, 0])
        return VGroup(body, roof, w1, w2)

    def road(self, width=13.2):
        asphalt = RoundedRectangle(
            width=width, height=1.25, corner_radius=0.16,
            stroke_color=INK, stroke_width=1.6,
            fill_color="#D1D5DB", fill_opacity=1
        )
        dash = VGroup(*[
            Line([-0.28, 0, 0], [0.28, 0, 0], color=WHITE, stroke_width=5)
            for _ in range(12)
        ]).arrange(RIGHT, buff=0.48).move_to(asphalt)
        return VGroup(asphalt, dash)

    def event_marker(self, x, label, color, icon):
        line = DashedLine([x, -0.9, 0], [x, 0.9, 0], dash_length=0.08, color=color, stroke_width=2)
        circle = Circle(0.28, fill_color=WHITE, fill_opacity=1, stroke_color=color, stroke_width=3)
        txt = Text(icon, font_size=22, color=color, weight=BOLD).move_to(circle)
        cap = Text(label, font_size=20, color=INK).next_to(circle, UP, buff=0.12)
        group = VGroup(line, circle, txt, cap)
        circle.move_to([x, 0.68, 0])
        txt.move_to(circle)
        cap.next_to(circle, UP, buff=0.12)
        return group

    @staticmethod
    def v_profile(t):
        # t in minutes, v in km/h. Linear transitions are deliberate:
        # they avoid physically impossible instantaneous speed jumps.
        pts = [
            (0, 0), (10, 70), (35, 70), (40, 0), (55, 0),
            (60, 65), (75, 65), (82, 25), (92, 25),
            (100, 10), (108, 10), (115, 55), (120, 55)
        ]
        if t <= pts[0][0]:
            return pts[0][1]
        if t >= pts[-1][0]:
            return pts[-1][1]
        for (t0, v0), (t1, v1) in zip(pts[:-1], pts[1:]):
            if t0 <= t <= t1:
                a = (t - t0) / (t1 - t0)
                return v0 + a * (v1 - v0)
        return 0

    @classmethod
    def x_profile(cls, t):
        # Numerical integral of v(t): km/h * h = km
        samples = np.linspace(0, t, max(2, int(t * 4) + 2))
        vals = np.array([cls.v_profile(s) for s in samples])
        return np.trapezoid(vals, samples / 60.0)

    # ------------------------------------------------------------------
    # Scene 0
    # ------------------------------------------------------------------
    def opening(self):
        top = Text("FUNDAMENTOS DE FÍSICA 9°", font_size=28, color=GRAY, weight=BOLD)
        top.to_edge(UP, buff=0.65)
        title = self.title("CUANDO LA VELOCIDAD DEJA DE SER CONSTANTE", 50)
        title.next_to(top, DOWN, buff=0.45)
        subtitle = self.body(
            "Del modelo ideal de MRU a una descripción más realista del movimiento",
            29, GRAY
        ).next_to(title, DOWN, buff=0.26)

        route = Line([-5.7, -1.2, 0], [5.7, -1.2, 0], color=INK, stroke_width=4)
        city_a = self.body("CIUDAD A", 25).next_to(route.get_start(), UP, buff=0.25)
        city_b = self.body("CIUDAD B", 25).next_to(route.get_end(), UP, buff=0.25)
        c = self.car().scale(0.75).move_to(route.get_start() + UP * 0.05)

        question = Text(
            "¿Qué cambia cuando el viaje real ya no puede describirse con una sola velocidad?",
            font_size=27, color=PURPLE, weight=BOLD
        ).to_edge(DOWN, buff=0.75)

        self.play(FadeIn(top), Write(title), FadeIn(subtitle), run_time=1.2)
        self.play(Create(route), FadeIn(city_a), FadeIn(city_b), FadeIn(c), run_time=1.0)
        self.play(c.animate.move_to(route.get_end() + UP * 0.05), run_time=2.2, rate_func=linear)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.8)
        self.wait(2.5)
        self.clear_all()

    # ------------------------------------------------------------------
    # Scene 1
    # ------------------------------------------------------------------
    def constant_velocity_reference(self):
        h = self.section_header(
            1,
            "EL MODELO SIMPLE: VELOCIDAD CONSTANTE",
            "En MRU, el móvil recorre distancias iguales en tiempos iguales."
        )
        self.add(h)

        road = self.road(12.4).move_to(DOWN * 0.7)
        c = self.car().scale(0.72).move_to([-5.6, -0.55, 0])

        clock = Text("0 min", font_size=26, color=INK)
        clock.move_to([0, 1.55, 0])

        eq = MathTex(r"x(t)=x_0+vt", font_size=42, color=INK)
        eq.move_to([0, -2.5, 0])
        note = Text(
            "Una sola pendiente → una sola velocidad",
            font_size=24, color=BLUE, weight=BOLD
        ).next_to(eq, DOWN, buff=0.20)

        self.play(FadeIn(road), FadeIn(c), FadeIn(clock))
        self.play(Write(eq), FadeIn(note))

        for i, x in enumerate([-3.1, -0.6, 1.9, 4.4], start=1):
            new_clock = Text(f"{i*15} min", font_size=26, color=INK).move_to(clock)
            self.play(
                c.animate.move_to([x, -0.55, 0]),
                Transform(clock, new_clock),
                run_time=0.85,
                rate_func=linear
            )
            tick = Line([x, -1.5, 0], [x, -1.28, 0], color=BLUE, stroke_width=4)
            self.play(Create(tick), run_time=0.18)

        ideal = Text(
            "Útil como modelo ideal. Pero un viaje real rara vez conserva exactamente la misma velocidad.",
            font_size=24, color=RED
        ).move_to([0, -3.45, 0])
        self.play(FadeIn(ideal))
        self.wait(2.4)
        self.clear_all()

    # ------------------------------------------------------------------
    # Scene 2
    # ------------------------------------------------------------------
    def real_route_story(self):
        h = self.section_header(
            2,
            "UN VIAJE MÁS REALISTA",
            "Un auto recorre una ruta de aproximadamente 80 km entre dos ciudades."
        )
        self.add(h)

        road = self.road(13.4).move_to(DOWN * 0.45)
        self.add(road)

        city_a = Text("CIUDAD A", font_size=24, color=INK, weight=BOLD).move_to([-6.35, 0.55, 0])
        city_b = Text("CIUDAD B", font_size=24, color=INK, weight=BOLD).move_to([6.35, 0.55, 0])
        self.add(city_a, city_b)

        events = VGroup(
            self.event_marker(-2.3, "Parada para comer", AMBER, "P"),
            self.event_marker(1.2, "Accidente adelante", RED, "!"),
            self.event_marker(3.9, "Tráfico intenso", PURPLE, "T"),
        )
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.12) for e in events], lag_ratio=0.18), run_time=1.4)

        c = self.car().scale(0.70).move_to([-6.0, -0.30, 0])
        speed = DecimalNumber(0, num_decimal_places=0, font_size=31, color=BLUE)
        speed.set_value(0)
        unit = Text("km/h", font_size=22, color=GRAY).next_to(speed, RIGHT, buff=0.12)
        speed_group = VGroup(speed, unit).move_to([0, 1.55, 0])
        status = Text("Sale de Ciudad A", font_size=25, color=INK).next_to(speed_group, DOWN, buff=0.20)

        self.play(FadeIn(c), FadeIn(speed_group), FadeIn(status))

        def segment(target_x, target_v, label, color=INK, rt=1.2, rate=smooth):
            nonlocal status
            new_status = Text(label, font_size=25, color=color).move_to(status)
            self.play(
                c.animate.move_to([target_x, -0.30, 0]),
                ChangeDecimalToValue(speed, target_v),
                Transform(status, new_status),
                run_time=rt,
                rate_func=rate
            )

        segment(-4.6, 70, "Acelera y entra a carretera", BLUE, 1.4, smooth)
        segment(-2.65, 70, "Circula a velocidad casi estable", BLUE, 1.4, linear)
        segment(-2.30, 0, "Frena y se detiene para comer", AMBER, 1.0, smooth)
        pause = Text("15 min detenido", font_size=22, color=AMBER, weight=BOLD).next_to(status, DOWN, buff=0.18)
        self.play(FadeIn(pause))
        self.wait(1.4)
        self.play(FadeOut(pause))
        segment(0.7, 65, "Retoma el viaje", GREEN, 1.5, smooth)
        segment(1.25, 25, "Reduce por un accidente", RED, 1.0, smooth)
        segment(3.7, 10, "Avanza lentamente por tráfico", PURPLE, 1.4, smooth)
        segment(5.8, 55, "El tráfico mejora y vuelve a acelerar", GREEN, 1.6, smooth)

        key = Text(
            "La velocidad ya no es una constante: cambia con el tiempo.",
            font_size=30, color=RED, weight=BOLD
        ).to_edge(DOWN, buff=0.58)
        self.play(FadeIn(key, shift=UP * 0.15))
        self.wait(2.8)
        self.clear_all()

    # ------------------------------------------------------------------
    # Scene 3
    # ------------------------------------------------------------------
    def position_time_analysis(self):
        h = self.section_header(
            3,
            "POSICIÓN VS. TIEMPO: LA PENDIENTE VA CAMBIANDO",
            "La pendiente de x(t) representa la velocidad."
        )
        self.add(h)

        axes = Axes(
            x_range=[0, 120, 20],
            y_range=[0, 85, 10],
            x_length=11.2,
            y_length=4.6,
            axis_config={"color": INK, "stroke_width": 2},
            tips=False
        ).move_to([0, -0.45, 0])
        xlab = Text("tiempo (min)", font_size=22, color=INK).next_to(axes.x_axis, DOWN, buff=0.25)
        ylab = Text("posición (km)", font_size=22, color=INK).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.25)

        ts = np.linspace(0, 120, 160)
        pts = [axes.c2p(t, self.x_profile(float(t))) for t in ts]
        curve = VMobject(stroke_color=BLUE, stroke_width=5)
        curve.set_points_smoothly(pts)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab))
        self.play(Create(curve), run_time=2.0)

        labels = [
            (20, self.x_profile(20), "Pendiente constante\nvelocidad estable", BLUE),
            (48, self.x_profile(48), "Tramo horizontal\nauto detenido", AMBER),
            (80, self.x_profile(80), "Pendiente menor\nreducción de velocidad", RED),
            (104, self.x_profile(104), "Pendiente muy pequeña\ntráfico lento", PURPLE),
        ]
        annotations = VGroup()
        for t, x, txt, col in labels:
            p = axes.c2p(t, x)
            dot = Dot(p, radius=0.07, color=col)
            lab = Text(txt, font_size=20, color=col, line_spacing=0.88)
            lab.next_to(dot, UP if t < 70 else DOWN, buff=0.15)
            annotations.add(VGroup(dot, lab))
        self.play(LaggedStart(*[FadeIn(a) for a in annotations], lag_ratio=0.22), run_time=1.8)

        msg = Text(
            "Una gráfica x-t curva o con pendientes distintas implica velocidades distintas.",
            font_size=25, color=INK, weight=BOLD
        ).to_edge(DOWN, buff=0.42)
        self.play(FadeIn(msg))
        self.wait(3)
        self.clear_all()

    # ------------------------------------------------------------------
    # Scene 4
    # ------------------------------------------------------------------
    def velocity_time_analysis(self):
        h = self.section_header(
            4,
            "VELOCIDAD VS. TIEMPO: AHORA v DEPENDE DE t",
            "La velocidad instantánea indica cómo se mueve el auto en cada instante."
        )
        self.add(h)

        axes = Axes(
            x_range=[0, 120, 20],
            y_range=[0, 80, 10],
            x_length=11.2,
            y_length=4.5,
            axis_config={"color": INK, "stroke_width": 2},
            tips=False
        ).move_to([0, -0.35, 0])
        xlab = Text("tiempo (min)", font_size=22, color=INK).next_to(axes.x_axis, DOWN, buff=0.25)
        ylab = Text("velocidad (km/h)", font_size=22, color=INK).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.25)

        ts = np.linspace(0, 120, 240)
        pts = [axes.c2p(t, self.v_profile(float(t))) for t in ts]
        curve = VMobject(stroke_color=RED, stroke_width=5)
        curve.set_points_as_corners(pts)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab))
        self.play(Create(curve), run_time=2.2)

        event_times = [
            (10, "acelera", GREEN),
            (40, "se detiene", AMBER),
            (60, "acelera", GREEN),
            (82, "frena", RED),
            (100, "tráfico", PURPLE),
            (115, "acelera", GREEN),
        ]
        marks = VGroup()
        for t, label, col in event_times:
            v = self.v_profile(t)
            p = axes.c2p(t, v)
            d = Dot(p, color=col, radius=0.07)
            tx = Text(label, font_size=19, color=col).next_to(d, UP, buff=0.10)
            marks.add(VGroup(d, tx))
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15), run_time=1.4)

        formula = MathTex(r"v=v(t)", font_size=46, color=RED).move_to([5.65, 2.15, 0])
        note = Text(
            "En un movimiento realista,\nla velocidad puede cambiar muchas veces.",
            font_size=23, color=INK, line_spacing=0.9
        ).next_to(formula, DOWN, buff=0.18)
        self.play(Write(formula), FadeIn(note))
        self.wait(3)
        self.clear_all()

    # ------------------------------------------------------------------
    # Scene 5
    # ------------------------------------------------------------------
    def acceleration_bridge(self):
        h = self.section_header(
            5,
            "¿CÓMO DESCRIBIMOS EL CAMBIO DE VELOCIDAD?",
            "Aparece una nueva cantidad física: la aceleración."
        )
        self.add(h)

        v_def = MathTex(r"a=\frac{\Delta v}{\Delta t}", font_size=56, color=INK)
        v_def.move_to([0, 1.25, 0])
        desc = Text(
            "Si la velocidad cambia, existe aceleración.",
            font_size=31, color=RED, weight=BOLD
        ).next_to(v_def, DOWN, buff=0.35)

        cards = VGroup()
        data = [
            ("ACELERAR", "0 → 70 km/h", "a > 0", GREEN),
            ("FRENAR", "70 → 25", "a < 0", RED),
            ("DETENIDO", "v = 0 constante", "a = 0", AMBER),
            ("CRUCERO", "v casi constante", "a ≈ 0", BLUE),
        ]
        for title, middle, bottom, col in data:
            box = RoundedRectangle(
                width=3.35, height=1.65, corner_radius=0.12,
                fill_color="#F9FAFB", fill_opacity=1,
                stroke_color=col, stroke_width=2.4
            )
            t = Text(title, font_size=23, color=col, weight=BOLD)
            m = Text(middle, font_size=18, color=INK)
            b = MathTex(bottom, font_size=29, color=col)
            grp = VGroup(box, t, m, b)
            t.move_to(box.get_center() + UP * 0.48)
            m.move_to(box.get_center())
            b.move_to(box.get_center() + DOWN * 0.47)
            cards.add(grp)
        cards.arrange(RIGHT, buff=0.25).scale(0.90).move_to([0, -1.2, 0])

        self.play(Write(v_def), FadeIn(desc))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.15), run_time=1.6)

        warning = Text(
            "Importante: en la realidad, los cambios de velocidad ocurren durante intervalos de tiempo, no como saltos instantáneos.",
            font_size=22, color=PURPLE
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(warning))
        self.wait(3.2)
        self.clear_all()

    # ------------------------------------------------------------------
    # Scene 6
    # ------------------------------------------------------------------
    def final_summary(self):
        h = self.section_header(
            6,
            "DEL MODELO IDEAL AL MOVIMIENTO REAL",
            "La física usa modelos simples primero y luego incorpora más detalle."
        )
        self.add(h)

        left = RoundedRectangle(
            width=6.2, height=4.0, corner_radius=0.16,
            fill_color="#F9FAFB", fill_opacity=1,
            stroke_color=BLUE, stroke_width=2.5
        ).move_to([-3.45, -0.45, 0])
        right = RoundedRectangle(
            width=6.2, height=4.0, corner_radius=0.16,
            fill_color="#F9FAFB", fill_opacity=1,
            stroke_color=RED, stroke_width=2.5
        ).move_to([3.45, -0.45, 0])

        ltitle = Text("MRU — MODELO IDEAL", font_size=28, color=BLUE, weight=BOLD).next_to(left.get_top(), DOWN, buff=0.35)
        rtitle = Text("MOVIMIENTO REALISTA", font_size=28, color=RED, weight=BOLD).next_to(right.get_top(), DOWN, buff=0.35)

        litems = VGroup(
            Text("• una sola velocidad", font_size=24, color=INK),
            Text("• pendiente x-t constante", font_size=24, color=INK),
            Text("• a = 0", font_size=24, color=INK),
            MathTex(r"x=x_0+vt", font_size=38, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        litems.move_to(left.get_center() + DOWN * 0.15)

        ritems = VGroup(
            Text("• v cambia con el tiempo", font_size=24, color=INK),
            Text("• la pendiente x-t cambia", font_size=24, color=INK),
            Text("• aparecen aceleraciones y frenadas", font_size=24, color=INK),
            MathTex(r"v=v(t),\quad a=\frac{\Delta v}{\Delta t}", font_size=35, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        ritems.move_to(right.get_center() + DOWN * 0.15)

        self.play(FadeIn(left), FadeIn(right), FadeIn(ltitle), FadeIn(rtitle))
        self.play(LaggedStart(*[FadeIn(x) for x in litems], lag_ratio=0.15), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(x) for x in ritems], lag_ratio=0.15), run_time=1.2)

        close = Text(
            "Una descripción más realista del movimiento involucra cambios continuos de velocidad: hay que seguir v instante a instante.",
            font_size=26, color=PURPLE, weight=BOLD
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(close, shift=UP * 0.12))
        self.wait(4.0)
