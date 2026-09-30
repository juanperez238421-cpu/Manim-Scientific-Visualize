"""Physics 9 — City-to-city motion, V3 senior classroom animation.

Standalone ManimCE 0.20.1 scene.
Focus: make physical direction unmistakable, connect the road model to signed
velocity, position equations, x-t graph, v-t graph, and cross-checks.

Render:
    manim -pqh physics9_city_cars_position_velocity_v3.py Physics9CityCarsV3

Optional accelerated QA:
    LESSON_TIME_SCALE=0.08 manim -pql ...
"""

from manim import *
import os

# -----------------------------------------------------------------------------
# Output / visual system
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

INK = "#18202A"
DARK = "#303A46"
MID = "#66717E"
LIGHT = "#D8DEE6"
PALE = "#F4F7FA"
ROAD = "#E9EDF2"
BLUE = "#1F67D2"
BLUE_DARK = "#174D9D"
RED = "#D74747"
RED_DARK = "#A92F2F"
GREEN = "#27865E"
GOLD = "#D59B2D"
WHITE2 = "#FCFDFE"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

A0 = 0.0
B0 = 240.0
VA = 80.0
VB = -40.0
T_MEET = 2.0
X_MEET = 160.0


def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


def fit_width(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def panel(width, height, stroke=LIGHT, fill=WHITE2, radius=0.18):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=radius,
        stroke_color=stroke,
        stroke_width=1.7,
        fill_color=fill,
        fill_opacity=1,
    )


def chip(label, color, width=2.25):
    box = RoundedRectangle(
        width=width,
        height=0.58,
        corner_radius=0.16,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.11,
    )
    t = txt(label, 23, color, BOLD)
    return VGroup(box, t)


def city_icon(name, accent):
    ground = Line(LEFT * 1.0, RIGHT * 1.0, color=DARK, stroke_width=3)
    blocks = VGroup(
        Rectangle(width=0.50, height=0.72, stroke_color=DARK, stroke_width=2, fill_color=accent, fill_opacity=0.12),
        Rectangle(width=0.42, height=1.06, stroke_color=DARK, stroke_width=2, fill_color=accent, fill_opacity=0.12),
        Rectangle(width=0.58, height=0.86, stroke_color=DARK, stroke_width=2, fill_color=accent, fill_opacity=0.12),
    ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
    blocks.next_to(ground, UP, buff=0)
    roof = Triangle(stroke_color=accent, stroke_width=2.5, fill_color=accent, fill_opacity=0.10).scale(0.20)
    roof.next_to(blocks[1], UP, buff=0.02)
    label = txt(name, 25, accent, BOLD).next_to(ground, DOWN, buff=0.12)
    return VGroup(ground, blocks, roof, label)


def directional_car(color, facing=1, label=None, scale=1.0):
    """Asymmetric car whose actual geometry faces the direction of travel.

    facing=+1: nose/headlight to the right.
    facing=-1: nose/headlight to the left.
    This fixes V2's ambiguity where only a small arrow changed direction.
    """
    s = 1 if facing >= 0 else -1

    # Body is intentionally asymmetric: low nose/front, taller rear quarter.
    pts = [
        np.array([-1.40*s, -0.20, 0]),
        np.array([-1.22*s,  0.28, 0]),
        np.array([-0.50*s,  0.46, 0]),
        np.array([ 0.20*s,  0.44, 0]),
        np.array([ 0.72*s,  0.27, 0]),
        np.array([ 1.34*s,  0.16, 0]),
        np.array([ 1.48*s, -0.20, 0]),
    ]
    body = Polygon(*pts, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.16)

    # Cabin / windshield slope identifies the front without relying on text.
    cabin_pts = [
        np.array([-0.48*s, 0.46, 0]),
        np.array([-0.08*s, 0.88, 0]),
        np.array([ 0.55*s, 0.82, 0]),
        np.array([ 0.83*s, 0.28, 0]),
    ]
    cabin = Polygon(*cabin_pts, stroke_color=color, stroke_width=2.7, fill_color=WHITE, fill_opacity=1)
    windshield = Line(np.array([0.55*s, 0.80, 0]), np.array([0.82*s, 0.30, 0]), color=color, stroke_width=4)

    wheels = VGroup(*[
        Circle(radius=0.25, stroke_color=INK, stroke_width=3, fill_color=WHITE, fill_opacity=1).move_to(np.array([x*s, -0.25, 0]))
        for x in (-0.88, 0.93)
    ])
    hubs = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=MID, fill_opacity=1).move_to(w.get_center()) for w in wheels])

    # Headlight is always at the nose; tail light at the rear.
    head = RoundedRectangle(width=0.16, height=0.14, corner_radius=0.03, stroke_width=0, fill_color=GOLD, fill_opacity=1)
    head.move_to(np.array([1.40*s, 0.03, 0]))
    tail = RoundedRectangle(width=0.12, height=0.16, corner_radius=0.03, stroke_width=0, fill_color=RED, fill_opacity=0.9)
    tail.move_to(np.array([-1.34*s, 0.02, 0]))

    # Large direction vector; this reinforces, rather than defines, direction.
    start_x, end_x = (-0.72*s, 0.72*s)
    vec = Arrow(
        np.array([start_x, 1.20, 0]), np.array([end_x, 1.20, 0]),
        buff=0, color=color, stroke_width=6, max_tip_length_to_length_ratio=0.20,
    )
    car = VGroup(body, cabin, windshield, wheels, hubs, head, tail, vec)
    if label:
        lab = txt(label, 24, color, BOLD).next_to(car, UP, buff=0.05)
        car.add(lab)
    return car.scale(scale)


def road_scene(show_cars=True):
    """Premium road with coordinate semantics built into the physical scene."""
    xL, xR, y = -5.60, 5.60, -0.35
    slab = RoundedRectangle(
        width=12.4, height=1.28, corner_radius=0.24,
        stroke_color=LIGHT, stroke_width=1.8, fill_color=ROAD, fill_opacity=1,
    ).move_to([0, y, 0])
    edge1 = Line([xL, y+0.49, 0], [xR, y+0.49, 0], color=DARK, stroke_width=2)
    edge2 = Line([xL, y-0.49, 0], [xR, y-0.49, 0], color=DARK, stroke_width=2)
    dashed = DashedLine([xL+0.15, y, 0], [xR-0.15, y, 0], dash_length=0.30, dashed_ratio=0.56, color=WHITE, stroke_width=4)

    cityA = city_icon("CITY A", BLUE).scale(0.82).move_to([xL, 1.05, 0])
    cityB = city_icon("CITY B", RED).scale(0.82).move_to([xR, 1.05, 0])
    zero = txt("0 km", 22, BLUE, BOLD).move_to([xL, -1.34, 0])
    twoforty = txt("240 km", 22, RED, BOLD).move_to([xR, -1.34, 0])
    plusx = Arrow([2.9, -1.62, 0], [4.65, -1.62, 0], buff=0, color=INK, stroke_width=4)
    pluslab = MathTex(r"+x", color=INK, font_size=32).next_to(plusx, RIGHT, buff=0.12)

    def x_for_km(km):
        return xL + (xR-xL)*(km/240.0)

    group = VGroup(slab, edge1, edge2, dashed, cityA, cityB, zero, twoforty, plusx, pluslab)
    cars = None
    if show_cars:
        carA = directional_car(BLUE, +1, scale=0.64).move_to([x_for_km(34), y+0.28, 0])
        carB = directional_car(RED, -1, scale=0.64).move_to([x_for_km(206), y-0.28, 0])
        group.add(carA, carB)
        cars = (carA, carB)
    return group, x_for_km, cars


class Physics9CityCarsV3(Scene):
    """V3: physical direction first, equations second, graphs last."""

    def play(self, *animations, **kwargs):
        # Preserve intentional run times while allowing accelerated smoke renders.
        base = kwargs.get("run_time", None)
        if base is None:
            base = max([getattr(a, "run_time", 1.0) for a in animations] or [1.0])
        kwargs["run_time"] = max(0.05, float(base) * TIME_SCALE)
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(max(0.05, duration * TIME_SCALE), *args, **kwargs)

    def construct(self):
        self.validate_data()
        self.opening()
        self.problem_model()
        self.sign_convention()
        self.position_equations()
        self.solve_meeting()
        self.live_meeting()
        self.position_graph()
        self.velocity_graph()
        self.cross_checks()
        self.method_summary()
        self.closing()

    def validate_data(self):
        assert abs((B0-A0)/(VA-VB) - T_MEET) < 1e-9
        assert abs(A0 + VA*T_MEET - X_MEET) < 1e-9
        assert abs(B0 + VB*T_MEET - X_MEET) < 1e-9

    # -------------------------- common layout ---------------------------------
    def clear_scene(self, run_time=0.55):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)

    def header(self, n, title, subtitle=None):
        badge = Circle(radius=0.30, stroke_width=0, fill_color=INK, fill_opacity=1).move_to([-6.95, 3.76, 0])
        num = txt(str(n), 23, WHITE, BOLD).move_to(badge)
        title_m = fit_width(txt(title, 34, INK, BOLD), 11.0).move_to([-0.95, 3.76, 0])
        title_m.align_to(badge, LEFT).shift(RIGHT*0.72)
        line = Line([-7.25, 3.30, 0], [7.25, 3.30, 0], color=LIGHT, stroke_width=2)
        g = VGroup(badge, num, title_m, line)
        if subtitle:
            sub = fit_width(txt(subtitle, 21, MID), 10.8).next_to(title_m, DOWN, buff=0.12).align_to(title_m, LEFT)
            g.add(sub)
        self.play(FadeIn(badge, scale=0.8), FadeIn(num), Write(title_m), Create(line), run_time=0.75)
        if subtitle:
            self.play(FadeIn(sub, shift=UP*0.08), run_time=0.45)
        return g

    def equation_panel(self, eq, caption, color=INK, width=6.2):
        bg = panel(width, 1.45)
        formula = MathTex(eq, font_size=43, color=color)
        cap = txt(caption, 21, MID)
        cap.next_to(formula, DOWN, buff=0.15)
        return VGroup(bg, formula, cap)

    # -------------------------- scenes ----------------------------------------
    def opening(self):
        title = txt("TWO CARS. ONE ROAD. ONE MEETING POINT.", 43, INK, BOLD)
        subtitle = txt("From physical direction → signed velocity → equations → graphs", 27, MID)
        title.move_to([0, 2.70, 0]); subtitle.next_to(title, DOWN, buff=0.24)

        road, x_for_km, _ = road_scene(show_cars=False)
        road.scale(0.94).shift(DOWN*0.55)
        # Recompute display positions after group transform using endpoints visually.
        carA = directional_car(BLUE, +1, "CAR A", 0.70).move_to([-3.75, -0.52, 0])
        carB = directional_car(RED, -1, "CAR B", 0.70).move_to([3.75, -0.52, 0])
        toward = VGroup(
            Arrow([-2.55, 0.35, 0], [-0.45, 0.35, 0], buff=0, color=BLUE, stroke_width=5),
            Arrow([2.55, 0.35, 0], [0.45, 0.35, 0], buff=0, color=RED, stroke_width=5),
        )
        question = txt("When and where do they meet?", 31, GREEN, BOLD).move_to([0, -2.95, 0])

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(subtitle, shift=UP*0.12), run_time=0.6)
        self.play(FadeIn(road), run_time=0.7)
        self.play(FadeIn(carA, shift=RIGHT*0.25), FadeIn(carB, shift=LEFT*0.25), run_time=0.8)
        self.play(GrowArrow(toward[0]), GrowArrow(toward[1]), run_time=0.75)
        self.play(Write(question), run_time=0.65)
        self.wait(1.4)
        self.clear_scene()

    def problem_model(self):
        self.header(1, "Build the physical model", "Start from the road — not from algebra.")
        road, x_for_km, cars = road_scene(show_cars=True)
        road.move_to([0, 0.25, 0])

        sep = DoubleArrow([x_for_km(0), 2.28, 0], [x_for_km(240), 2.28, 0], buff=0.06, color=INK, stroke_width=3)
        sep_lab = txt("240 km separation", 26, INK, BOLD).next_to(sep, UP, buff=0.10)
        va = chip("vA = +80 km/h", BLUE, 2.60).move_to([-3.25, -2.42, 0])
        vb = chip("vB = −40 km/h", RED, 2.60).move_to([3.25, -2.42, 0])
        note = txt("The cars physically face each other: A → right, B → left.", 24, GREEN, BOLD).move_to([0, -3.14, 0])

        self.play(FadeIn(road), run_time=0.8)
        self.play(GrowArrow(sep), FadeIn(sep_lab), run_time=0.7)
        self.play(FadeIn(va, shift=RIGHT*0.15), FadeIn(vb, shift=LEFT*0.15), run_time=0.7)
        self.play(FadeIn(note, shift=UP*0.12), run_time=0.55)
        self.wait(1.8)
        self.clear_scene()

    def sign_convention(self):
        self.header(2, "Choose +x before using velocity", "A direction is geometry. A velocity sign is mathematics.")
        road, x_for_km, _ = road_scene(show_cars=False)
        road.scale(0.92).move_to([0, 0.60, 0])

        carA = directional_car(BLUE, +1, scale=0.68).move_to([-3.45, 0.42, 0])
        carB = directional_car(RED, -1, scale=0.68).move_to([3.45, 0.42, 0])
        vecA = Arrow([-4.0, -1.20, 0], [-1.90, -1.20, 0], buff=0, color=BLUE, stroke_width=7)
        vecB = Arrow([4.0, -1.20, 0], [2.60, -1.20, 0], buff=0, color=RED, stroke_width=7)
        labA = MathTex(r"v_A=+80\;\mathrm{km/h}", font_size=38, color=BLUE).next_to(vecA, DOWN, buff=0.15)
        labB = MathTex(r"v_B=-40\;\mathrm{km/h}", font_size=38, color=RED).next_to(vecB, DOWN, buff=0.15)
        key = panel(5.65, 0.88, stroke=GREEN, fill="#F5FBF7").move_to([0, -2.95, 0])
        keytxt = txt("Rightward = positive   |   Leftward = negative", 24, GREEN, BOLD).move_to(key)

        self.play(FadeIn(road), FadeIn(carA), FadeIn(carB), run_time=0.8)
        self.play(GrowArrow(vecA), GrowArrow(vecB), run_time=0.7)
        self.play(Write(labA), Write(labB), run_time=0.8)
        self.play(FadeIn(key), FadeIn(keytxt), run_time=0.55)
        self.wait(2.0)
        self.clear_scene()

    def position_equations(self):
        self.header(3, "Write one position equation for each car", "Uniform motion: x(t) = x₀ + vt")

        general = MathTex(r"x(t)=x_0+vt", font_size=49, color=INK).move_to([0, 2.35, 0])
        left = self.equation_panel(r"x_A(t)=0+(80)t=80t", "Starts at 0 km and moves right", BLUE, 6.35).move_to([-3.45, 0.65, 0])
        right = self.equation_panel(r"x_B(t)=240+(-40)t", "Starts at 240 km and moves left", RED, 6.35).move_to([3.45, 0.65, 0])
        right2 = MathTex(r"x_B(t)=240-40t", font_size=44, color=RED).move_to([3.45, -0.65, 0])
        check = txt("Notice: B's negative direction is already encoded in −40t.", 25, GREEN, BOLD).move_to([0, -2.22, 0])
        q = txt("At the meeting: both cars have the same position x.", 27, INK, BOLD).move_to([0, -2.88, 0])

        self.play(Write(general), run_time=0.7)
        self.play(FadeIn(left, shift=RIGHT*0.20), FadeIn(right, shift=LEFT*0.20), run_time=0.9)
        self.play(TransformFromCopy(right[1], right2), run_time=0.75)
        self.play(FadeIn(check, shift=UP*0.10), run_time=0.55)
        self.play(Write(q), run_time=0.65)
        self.wait(1.8)
        self.clear_scene()

    def solve_meeting(self):
        self.header(4, "Solve the meeting condition", "Same place, same time → set xA(t) = xB(t)")
        lines = VGroup(
            MathTex(r"x_A=x_B", font_size=46, color=INK),
            MathTex(r"80t=240-40t", font_size=46, color=INK),
            MathTex(r"120t=240", font_size=46, color=INK),
            MathTex(r"\boxed{t=2\ \mathrm{h}}", font_size=50, color=GREEN),
        ).arrange(DOWN, buff=0.40).move_to([-2.55, 0.10, 0])
        arrow = Arrow([0.20, 0.15, 0], [1.45, 0.15, 0], buff=0, color=MID, stroke_width=4)
        pos_panel = panel(5.0, 3.3, stroke=BLUE, fill="#F7FAFE").move_to([4.15, 0.05, 0])
        pos_title = txt("Meeting position", 27, BLUE, BOLD).move_to([4.15, 1.28, 0])
        pos_eq1 = MathTex(r"x=80(2)", font_size=44, color=BLUE).move_to([4.15, 0.42, 0])
        pos_eq2 = MathTex(r"\boxed{x=160\ \mathrm{km}}", font_size=48, color=BLUE).move_to([4.15, -0.45, 0])
        pos_note = txt("from City A", 23, MID).move_to([4.15, -1.05, 0])
        pause = txt("Predict before the reveal: should t be more or less than 3 h?", 23, GOLD, BOLD).move_to([0, -2.78, 0])

        self.play(FadeIn(pause), run_time=0.5)
        self.wait(1.5)
        for line in lines:
            self.play(Write(line), run_time=0.62)
        self.play(GrowArrow(arrow), FadeIn(pos_panel), run_time=0.6)
        self.play(FadeIn(pos_title), Write(pos_eq1), run_time=0.6)
        self.play(Write(pos_eq2), FadeIn(pos_note), run_time=0.7)
        self.wait(1.8)
        self.clear_scene()

    def live_meeting(self):
        self.header(5, "Watch both positions evolve", "The road model and the equations must tell the same story.")

        xL, xR, road_y = -5.85, 5.85, -0.25
        slab = RoundedRectangle(width=12.5, height=1.38, corner_radius=0.23, stroke_color=LIGHT, stroke_width=2, fill_color=ROAD, fill_opacity=1).move_to([0, road_y, 0])
        dashed = DashedLine([xL, road_y,0],[xR,road_y,0],dash_length=0.34,dashed_ratio=0.56,color=WHITE,stroke_width=4)
        cityA = city_icon("A", BLUE).scale(0.72).move_to([xL,1.02,0])
        cityB = city_icon("B", RED).scale(0.72).move_to([xR,1.02,0])
        meet_x = xL + (xR-xL)*(160/240)
        meet_line = DashedLine([meet_x,-1.10,0],[meet_x,1.65,0],dash_length=0.14,color=GREEN,stroke_width=3)
        meet_label = txt("x = 160 km", 22, GREEN, BOLD).next_to(meet_line, UP, buff=0.08)
        self.play(FadeIn(VGroup(slab,dashed,cityA,cityB)), Create(meet_line), FadeIn(meet_label), run_time=0.8)

        tracker = ValueTracker(0.0)
        road_x = lambda km: xL + (xR-xL)*(km/240.0)
        carA = always_redraw(lambda: directional_car(BLUE,+1,scale=0.56).move_to([road_x(VA*tracker.get_value()), road_y+0.27,0]))
        carB = always_redraw(lambda: directional_car(RED,-1,scale=0.56).move_to([road_x(B0+VB*tracker.get_value()), road_y-0.27,0]))

        info = panel(11.0,1.55,stroke=LIGHT,fill=WHITE2).move_to([0,-2.45,0])
        time_m = always_redraw(lambda: VGroup(txt("t =",22,MID,BOLD), DecimalNumber(tracker.get_value(),num_decimal_places=2,font_size=30,color=INK), txt("h",22,INK,BOLD)).arrange(RIGHT,buff=0.12).move_to([-4.25,-2.45,0]))
        xa_m = always_redraw(lambda: VGroup(txt("xA =",22,BLUE,BOLD), DecimalNumber(VA*tracker.get_value(),num_decimal_places=1,font_size=29,color=BLUE), txt("km",20,BLUE)).arrange(RIGHT,buff=0.10).move_to([-1.55,-2.45,0]))
        xb_m = always_redraw(lambda: VGroup(txt("xB =",22,RED,BOLD), DecimalNumber(B0+VB*tracker.get_value(),num_decimal_places=1,font_size=29,color=RED), txt("km",20,RED)).arrange(RIGHT,buff=0.10).move_to([1.55,-2.45,0]))
        gap_m = always_redraw(lambda: VGroup(txt("gap =",22,GREEN,BOLD), DecimalNumber(max(0,B0-(VA-VB)*tracker.get_value()),num_decimal_places=1,font_size=29,color=GREEN), txt("km",20,GREEN)).arrange(RIGHT,buff=0.10).move_to([4.25,-2.45,0]))

        self.add(carA,carB)
        self.play(FadeIn(info), FadeIn(time_m), FadeIn(xa_m), FadeIn(xb_m), FadeIn(gap_m), run_time=0.7)
        self.wait(0.7)
        self.play(tracker.animate.set_value(2.0), run_time=5.2, rate_func=linear)
        self.wait(0.6)

        meet_dot = Dot([meet_x,road_y,0],radius=0.10,color=GREEN)
        flash = Circle(radius=0.26,color=GREEN,stroke_width=5).move_to(meet_dot)
        self.play(FadeIn(meet_dot), ShowPassingFlash(flash.copy().scale(2.2), time_width=0.7), run_time=0.9)

        # Freeze final state before removing updaters.
        self.remove(carA,carB,time_m,xa_m,xb_m,gap_m)
        finalA = directional_car(BLUE,+1,scale=0.56).move_to([meet_x-0.28,road_y+0.27,0])
        finalB = directional_car(RED,-1,scale=0.56).move_to([meet_x+0.28,road_y-0.27,0])
        self.add(finalA,finalB)
        info2 = VGroup(
            txt("t = 2.00 h",22,INK,BOLD), txt("xA = 160 km",22,BLUE,BOLD), txt("xB = 160 km",22,RED,BOLD), txt("gap = 0 km",22,GREEN,BOLD)
        ).arrange(RIGHT,buff=0.72).move_to([0,-2.45,0])
        self.add(info2)

        distA = DoubleArrow([xL,-1.35,0],[meet_x,-1.35,0],buff=0.06,color=BLUE,stroke_width=3)
        distB = DoubleArrow([meet_x,-1.74,0],[xR,-1.74,0],buff=0.06,color=RED,stroke_width=3)
        labA = txt("160 km from A",21,BLUE,BOLD).next_to(distA,DOWN,buff=0.06)
        labB = txt("80 km from B",21,RED,BOLD).next_to(distB,DOWN,buff=0.06)
        self.play(GrowArrow(distA), GrowArrow(distB), FadeIn(labA), FadeIn(labB), run_time=0.9)
        self.wait(2.0)
        self.clear_scene()

    def position_graph(self):
        self.header(6, "Position–time graph: two stories on one set of axes", "Intersection = same position at the same time.")
        axes = Axes(
            x_range=[0,3,0.5], y_range=[0,240,40], x_length=9.0, y_length=5.0,
            axis_config={"color":DARK,"stroke_width":2.5,"include_tip":True},
            x_axis_config={"numbers_to_include":[0,1,2,3],"font_size":22},
            y_axis_config={"numbers_to_include":[0,80,160,240],"font_size":22},
        ).move_to([-1.05,-0.15,0])
        labels = axes.get_axis_labels(MathTex(r"t\;(h)",font_size=30,color=INK), MathTex(r"x\;(km)",font_size=30,color=INK))
        gA = axes.plot(lambda t:80*t,x_range=[0,3],color=BLUE,stroke_width=5)
        gB = axes.plot(lambda t:240-40*t,x_range=[0,3],color=RED,stroke_width=5)
        p = Dot(axes.c2p(2,160),radius=0.10,color=GREEN)
        vline = DashedLine(axes.c2p(2,0),axes.c2p(2,160),color=GREEN,stroke_width=2)
        hline = DashedLine(axes.c2p(0,160),axes.c2p(2,160),color=GREEN,stroke_width=2)
        meeting = chip("meeting: (2 h, 160 km)",GREEN,3.10).move_to([5.60,1.25,0])
        la = chip("A: slope +80",BLUE,2.30).move_to([5.55,0.35,0])
        lb = chip("B: slope −40",RED,2.30).move_to([5.55,-0.50,0])
        interp = panel(3.45,1.30,stroke=LIGHT,fill=PALE).move_to([5.55,-1.90,0])
        it1 = txt("steeper line → faster |v|",20,INK,BOLD).move_to([5.55,-1.68,0])
        it2 = txt("negative slope → motion left",20,RED,BOLD).move_to([5.55,-2.08,0])

        self.play(Create(axes), FadeIn(labels), run_time=0.8)
        self.play(Create(gA), run_time=1.1)
        self.play(FadeIn(la), run_time=0.45)
        self.play(Create(gB), run_time=1.1)
        self.play(FadeIn(lb), run_time=0.45)
        self.play(Create(vline),Create(hline),FadeIn(p,scale=1.5),FadeIn(meeting),run_time=0.85)
        self.play(FadeIn(interp),FadeIn(it1),FadeIn(it2),run_time=0.65)
        self.wait(2.3)
        self.clear_scene()

    def velocity_graph(self):
        self.header(7, "Velocity–time graph: direction becomes height", "Constant velocity → horizontal line.")
        axes = Axes(
            x_range=[0,3,0.5], y_range=[-60,100,20], x_length=9.0, y_length=5.0,
            axis_config={"color":DARK,"stroke_width":2.5,"include_tip":True},
            x_axis_config={"numbers_to_include":[0,1,2,3],"font_size":22},
            y_axis_config={"numbers_to_include":[-40,0,40,80],"font_size":22},
        ).move_to([-1.1,-0.15,0])
        labels = axes.get_axis_labels(MathTex(r"t\;(h)",font_size=30,color=INK), MathTex(r"v\;(km/h)",font_size=30,color=INK))
        zero = DashedLine(axes.c2p(0,0),axes.c2p(3,0),color=MID,stroke_width=2)
        gA = axes.plot(lambda t:80,x_range=[0,3],color=BLUE,stroke_width=6)
        gB = axes.plot(lambda t:-40,x_range=[0,3],color=RED,stroke_width=6)
        ca = chip("A: +80 km/h",BLUE,2.45).move_to([5.45,1.25,0])
        cb = chip("B: −40 km/h",RED,2.45).move_to([5.45,0.35,0])
        sign_panel = panel(3.65,2.05,stroke=LIGHT,fill=PALE).move_to([5.45,-1.28,0])
        s1=txt("above 0 → right",21,BLUE,BOLD).move_to([5.45,-0.88,0])
        s2=txt("below 0 → left",21,RED,BOLD).move_to([5.45,-1.40,0])
        s3=txt("horizontal → constant v",20,INK,BOLD).move_to([5.45,-1.92,0])

        self.play(Create(axes),FadeIn(labels),Create(zero),run_time=0.85)
        self.play(Create(gA),FadeIn(ca),run_time=0.9)
        self.play(Create(gB),FadeIn(cb),run_time=0.9)
        self.play(FadeIn(sign_panel),FadeIn(s1),FadeIn(s2),FadeIn(s3),run_time=0.7)
        self.wait(2.4)
        self.clear_scene()

    def cross_checks(self):
        self.header(8, "Cross-check the result two different ways", "A strong physics solution should survive an independent check.")
        p1 = panel(6.25,4.65,stroke=BLUE,fill="#F7FAFE").move_to([-3.35,-0.10,0])
        p2 = panel(6.25,4.65,stroke=GREEN,fill="#F6FBF8").move_to([3.35,-0.10,0])
        t1 = txt("CHECK A · Relative speed",27,BLUE,BOLD).move_to([-3.35,1.68,0])
        a1 = MathTex(r"v_{close}=80+40=120\ \mathrm{km/h}",font_size=38,color=INK).move_to([-3.35,0.72,0])
        a2 = MathTex(r"t=\frac{240}{120}=\boxed{2\ \mathrm{h}}",font_size=42,color=BLUE).move_to([-3.35,-0.20,0])
        a3 = txt("Gap closes at 120 km every hour.",22,MID).move_to([-3.35,-1.22,0])
        t2 = txt("CHECK B · Distances traveled",27,GREEN,BOLD).move_to([3.35,1.68,0])
        b1 = MathTex(r"d_A=80(2)=160\ \mathrm{km}",font_size=38,color=BLUE).move_to([3.35,0.72,0])
        b2 = MathTex(r"d_B=40(2)=80\ \mathrm{km}",font_size=38,color=RED).move_to([3.35,-0.05,0])
        b3 = MathTex(r"160+80=\boxed{240\ \mathrm{km}}",font_size=42,color=GREEN).move_to([3.35,-0.88,0])
        verdict = txt("Both checks agree with the road animation and the graphs.",24,GREEN,BOLD).move_to([0,-2.88,0])

        self.play(FadeIn(p1),FadeIn(p2),FadeIn(t1),FadeIn(t2),run_time=0.7)
        self.play(Write(a1),Write(b1),run_time=0.7)
        self.play(Write(a2),Write(b2),run_time=0.75)
        self.play(FadeIn(a3),Write(b3),run_time=0.7)
        self.play(FadeIn(verdict,shift=UP*0.10),run_time=0.55)
        self.wait(2.2)
        self.clear_scene()

    def method_summary(self):
        self.header(9, "Reusable method for every two-object meeting problem")
        steps = [
            ("1", "Choose +x", "Draw the direction first."),
            ("2", "Assign signs", "Right +, left −."),
            ("3", "Write x(t)", "One equation per object."),
            ("4", "Set positions equal", "Meeting means same x and t."),
            ("5", "Check with graphs", "x–t intersection; v–t signs."),
        ]
        cards = VGroup()
        xs=[-5.65,-2.82,0,2.82,5.65]
        for x,(n,title,body) in zip(xs,steps):
            box=panel(2.42,3.45,stroke=LIGHT,fill=WHITE2).move_to([x,-0.10,0])
            circ=Circle(radius=0.30,stroke_width=0,fill_color=INK,fill_opacity=1).move_to([x,1.07,0])
            num=txt(n,22,WHITE,BOLD).move_to(circ)
            tt=fit_width(txt(title,22,INK,BOLD),2.05).move_to([x,0.44,0])
            bd=fit_width(txt(body,18,MID),2.05).move_to([x,-0.43,0])
            cards.add(VGroup(box,circ,num,tt,bd))
        for card in cards:
            self.play(FadeIn(card,shift=UP*0.15),run_time=0.38)
        takeaway = panel(10.5,1.02,stroke=GREEN,fill="#F5FBF7").move_to([0,-2.55,0])
        phrase = txt("Direction → sign → equation → meeting → graph. Keep this order.",26,GREEN,BOLD).move_to(takeaway)
        self.play(FadeIn(takeaway),Write(phrase),run_time=0.65)
        self.wait(2.4)
        self.clear_scene()

    def closing(self):
        carA = directional_car(BLUE,+1,scale=0.62).move_to([-3.9,0.4,0])
        carB = directional_car(RED,-1,scale=0.62).move_to([3.9,0.4,0])
        eq = MathTex(r"x_A(2)=x_B(2)=160\ \mathrm{km}",font_size=50,color=GREEN).move_to([0,1.65,0])
        title = txt("THE PHYSICS, ALGEBRA, AND GRAPHS AGREE.",36,INK,BOLD).move_to([0,-1.15,0])
        sub = txt("That agreement is the real answer check.",25,MID).move_to([0,-1.78,0])
        self.play(FadeIn(carA,shift=RIGHT*0.25),FadeIn(carB,shift=LEFT*0.25),run_time=0.7)
        self.play(Write(eq),run_time=0.75)
        self.play(Write(title),FadeIn(sub,shift=UP*0.08),run_time=0.7)
        self.wait(2.3)
        self.play(FadeOut(VGroup(carA,carB,eq,title,sub)),run_time=0.8)


if __name__ == "__main__":
    # Scene is rendered by Manim CLI; this block intentionally does nothing.
    pass
