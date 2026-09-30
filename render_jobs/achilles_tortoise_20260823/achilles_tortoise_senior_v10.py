from manim import *
from jp_classroom_style import (
    JPClassroomScene,
    BLACK_TEXT,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT_GRAY,
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


class AchillesTortoiseSeniorV10(JPClassroomScene):
    """Senior QA V10 continuous-diagram English reconstruction of Achilles and the Tortoise.

    Direction rule: after the race diagram and analysis panel appear, they stay
    visible through the paradox, convergence, and final physical catch.
    """

    V_A = 10.0
    V_T = 1.0
    LEAD = 10.0
    T_CATCH = 10.0 / 9.0
    X_CATCH = 100.0 / 9.0

    def validate_lesson_data(self):
        assert abs(self.T_CATCH - self.LEAD / (self.V_A - self.V_T)) < 1e-12
        assert abs(self.X_CATCH - self.V_A * self.T_CATCH) < 1e-12
        assert abs(self.X_CATCH - (self.LEAD + self.V_T * self.T_CATCH)) < 1e-12
        stages = [
            (0.0, 10.0, 10.0, 11.0, 1.0),
            (10.0, 11.0, 11.0, 11.1, 0.1),
            (11.0, 11.1, 11.1, 11.11, 0.01),
            (11.1, 11.11, 11.11, 11.111, 0.001),
        ]
        for a0, a1, t0, t1, dt in stages:
            assert abs((a1 - a0) / self.V_A - dt) < 1e-10
            assert abs((t1 - t0) / self.V_T - dt) < 1e-10

    def chip(self, content, width=2.35, height=0.58, size=23):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.11,
            stroke_color=BLACK_LINE, stroke_width=1.6, fill_color=PAPER_GRAY, fill_opacity=1)
        txt = self.text(content, size, BOLD)
        self.fit(txt, width - 0.24, height - 0.14)
        txt.move_to(box)
        return VGroup(box, txt)

    def math_chip(self, expression, width=2.35, height=0.58, size=27):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.11,
            stroke_color=BLACK_LINE, stroke_width=1.6, fill_color=PAPER_GRAY, fill_opacity=1)
        eq = self.math(expression, size)
        self.fit(eq, width - 0.24, height - 0.14)
        eq.move_to(box)
        return VGroup(box, eq)

    def runner_icon(self, scale=1.0):
        head = Circle(radius=0.15, stroke_color=BLACK_LINE, stroke_width=2.3)
        torso = Line([0, -0.14, 0], [-0.08, -0.62, 0], color=BLACK_LINE, stroke_width=3)
        arm1 = Line([-0.03, -0.30, 0], [0.30, -0.44, 0], color=BLACK_LINE, stroke_width=3)
        arm2 = Line([-0.03, -0.31, 0], [-0.32, -0.16, 0], color=BLACK_LINE, stroke_width=3)
        leg1 = Line([-0.08, -0.62, 0], [0.28, -0.91, 0], color=BLACK_LINE, stroke_width=3)
        leg2 = Line([-0.08, -0.62, 0], [-0.42, -0.88, 0], color=BLACK_LINE, stroke_width=3)
        return VGroup(head, torso, arm1, arm2, leg1, leg2).scale(scale)

    def tortoise_icon(self, scale=1.0):
        shell = Ellipse(width=0.78, height=0.43, stroke_color=DARK_GRAY, stroke_width=2.2,
            fill_color=PAPER_GRAY, fill_opacity=1)
        shell_arc1 = Arc(radius=0.22, start_angle=0.2, angle=2.7, color=MID_GRAY, stroke_width=1.3).move_to(shell)
        shell_arc2 = Arc(radius=0.22, start_angle=PI + 0.2, angle=2.7, color=MID_GRAY, stroke_width=1.3).move_to(shell)
        head = Circle(radius=0.11, stroke_color=DARK_GRAY, stroke_width=2, fill_color=WHITE, fill_opacity=1).next_to(shell, RIGHT, buff=-0.02)
        eye = Dot(radius=0.018, color=BLACK).move_to(head.get_center() + RIGHT * 0.035 + UP * 0.025)
        legs = VGroup(
            Line([-0.22, -0.18, 0], [-0.31, -0.34, 0], color=DARK_GRAY, stroke_width=2),
            Line([0.18, -0.18, 0], [0.12, -0.34, 0], color=DARK_GRAY, stroke_width=2),
        )
        tail = Line([-0.39, 0.01, 0], [-0.56, 0.08, 0], color=DARK_GRAY, stroke_width=2)
        return VGroup(shell, shell_arc1, shell_arc2, head, eye, legs, tail).scale(scale)

    def master_track(self):
        return NumberLine(x_range=[0, 12, 1], length=13.0, include_numbers=True, font_size=18,
            color=BLACK_LINE, stroke_width=2.0, tick_size=0.075,
            decimal_number_config={"color": BLACK_TEXT}).move_to([0, 0.78, 0])

    def analysis_panel(self):
        return RoundedRectangle(width=13.75, height=3.60, corner_radius=0.15,
            stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE, fill_opacity=1).move_to([0, -2.02, 0])

    def interval_band(self, track, x0, x1):
        p0, p1 = track.n2p(x0), track.n2p(x1)
        width = max(abs(p1[0] - p0[0]), 0.14)
        return RoundedRectangle(width=width, height=0.48, corner_radius=0.07,
            stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=PAPER_GRAY, fill_opacity=0.50).move_to([(p0[0] + p1[0]) / 2, track.get_center()[1], 0])

    def connector_pair(self, band, panel):
        return VGroup(
            Line(band.get_corner(DL), panel.get_corner(UL) + RIGHT * 0.55, color=LIGHT_GRAY, stroke_width=1.5),
            Line(band.get_corner(DR), panel.get_corner(UR) + LEFT * 0.55, color=LIGHT_GRAY, stroke_width=1.5),
        )

    def build_master_scene(self):
        track = self.master_track()
        panel = self.analysis_panel()
        runner = self.runner_icon(0.57).move_to(track.n2p(0) + UP * 1.30)
        tortoise = self.tortoise_icon(0.66).move_to(track.n2p(10) + UP * 0.12)
        r_label = self.text("ACHILLES", 18, BOLD).next_to(runner, UP, buff=0.03)
        t_label = self.text("TORTOISE", 18, BOLD).next_to(tortoise, UP, buff=0.04)
        chips = VGroup(
            self.math_chip(r"v_A=10\,\mathrm{m/s}", 2.55),
            self.math_chip(r"v_T=1\,\mathrm{m/s}", 2.45),
            self.math_chip(r"\Delta x_0=10\,\mathrm{m}", 2.70),
        ).arrange(RIGHT, buff=0.24).move_to([0, 1.92, 0])
        return {"track": track, "panel": panel, "runner": runner, "tortoise": tortoise,
            "r_label": r_label, "t_label": t_label, "chips": chips}

    def physical_meeting(self, m):
        self.set_header(1, "THE REAL RACE: WHERE DO THEY MEET?",
            "Achilles runs at 10 m/s. The tortoise runs at 1 m/s and starts 10 m ahead.")
        self.play(Create(m["track"]), FadeIn(m["panel"]), run_time=RUN_NORMAL)
        self.play(FadeIn(m["runner"], shift=RIGHT * 0.12), FadeIn(m["tortoise"], shift=RIGHT * 0.05),
            Write(m["r_label"]), Write(m["t_label"]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.07) for c in m["chips"]], lag_ratio=0.15), run_time=RUN_SLOW)

        title = self.text("POSITION EQUATIONS", 23, BOLD).move_to([0, -0.55, 0])
        eqs = VGroup(
            self.math(r"x_A(t)=10t", 33), self.math(r"x_T(t)=10+t", 33),
            self.math(r"10t=10+t\;\Rightarrow\;t^*=\frac{10}{9}\,\mathrm{s}=1.111\ldots\,\mathrm{s}", 32),
            self.math(r"x^*=10t^*=\frac{100}{9}\,\mathrm{m}=11.111\ldots\,\mathrm{m}", 31),
        ).arrange(DOWN, buff=0.16).move_to([0, -2.10, 0])
        self.fit(eqs, 12.7, 2.60)
        self.play(Write(title), run_time=RUN_NORMAL)
        for eq in eqs:
            self.play(Write(eq), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT * 0.45)
        result_box = SurroundingRectangle(VGroup(eqs[-2], eqs[-1]), buff=0.11, color=BLACK_LINE, stroke_width=2.1)
        self.play(Create(result_box), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)

        meet_x = m["track"].n2p(self.X_CATCH)[0]
        meet_line = DashedLine([meet_x, 0.05, 0], [meet_x, 1.70, 0], color=MID_GRAY, dash_length=0.08)
        self.play(FadeOut(m["r_label"]), FadeOut(m["t_label"]),
            m["runner"].animate.move_to(m["track"].n2p(self.X_CATCH) + UP * 1.30),
            m["tortoise"].animate.move_to(m["track"].n2p(self.X_CATCH) + UP * 0.12),
            run_time=4.8, rate_func=linear)
        self.play(Create(meet_line), run_time=RUN_NORMAL)
        meet_formula = self.math(r"x^*=\frac{100}{9}\,\mathrm{m}", 24)
        meet_caption = self.text("MEETING POSITION", 17, BOLD)
        meet_callout = VGroup(meet_formula, meet_caption).arrange(DOWN, buff=0.04)
        callout_box = SurroundingRectangle(meet_callout, buff=0.10, color=BLACK_LINE, stroke_width=1.5,
            fill_color=WHITE, fill_opacity=1)
        meet_callout_group = VGroup(callout_box, meet_callout).move_to([4.25, 2.45, 0])
        callout_arrow = Arrow(meet_callout_group.get_corner(DR) + DOWN * 0.02, [meet_x, 1.62, 0], buff=0.08,
            color=MID_GRAY, stroke_width=1.6, max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(meet_callout_group), GrowArrow(callout_arrow), run_time=RUN_NORMAL)
        pulse = Circle(radius=0.25, stroke_color=BLACK_LINE, stroke_width=2).move_to([meet_x, 0.78, 0])
        self.play(GrowFromCenter(pulse), run_time=RUN_QUICK)
        self.play(FadeOut(pulse), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)
        m["meet_line"] = meet_line
        m["meet_tag"] = VGroup(meet_callout_group, callout_arrow)
        m["panel_content"] = VGroup(title, eqs, result_box)

    def zeno_reframe(self, m):
        self.set_header(2, "ZENO CHANGES THE DESCRIPTION, NOT THE MOTION",
            "Instead of watching the whole catch, follow the places where the tortoise was one step earlier.")
        self.play(m["runner"].animate.move_to(m["track"].n2p(0) + UP * 1.30),
            m["tortoise"].animate.move_to(m["track"].n2p(10) + UP * 0.12), FadeOut(m["meet_tag"]),
            run_time=2.2, rate_func=smooth)
        intro = VGroup(self.text("Zeno's rule", 24, BOLD),
            self.text("Achilles first reaches the place where the tortoise was.", 25),
            self.text("During that same time, the tortoise moves ahead and creates a smaller gap.", 25),
        ).arrange(DOWN, buff=0.20).move_to([0, -2.02, 0])
        self.fit(intro, 12.7, 2.5)
        self.play(FadeOut(m["panel_content"], shift=DOWN * 0.04), run_time=RUN_NORMAL)
        self.play(FadeIn(intro, shift=UP * 0.05), run_time=RUN_NORMAL)
        band = self.interval_band(m["track"], 0, 10)
        connectors = self.connector_pair(band, m["panel"])
        current = self.math(r"\text{current interval: }[0,10]\,\mathrm{m}", 27).move_to([0, -3.28, 0])
        self.play(Create(band), Create(connectors), Write(current), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        m["intro_content"], m["band"], m["connectors"], m["current_interval_label"] = intro, band, connectors, current

    def make_lens_contents(self):
        lens_title = self.text("MAGNIFIED VIEW OF THE SELECTED INTERVAL", 21, BOLD).move_to([0, -0.52, 0])
        meta = self.math(r"\text{Stage 1}\quad [0,10]\,\mathrm{m}\quad \Delta t=1\,\mathrm{s}", 24).move_to([0, -1.02, 0])
        x_l, x_target, x_r, y = -5.10, 3.25, 4.45, -2.05
        baseline = Line([x_l - 0.35, y, 0], [x_r + 0.35, y, 0], color=BLACK_LINE, stroke_width=2.0)
        target = DashedLine([x_target, y - 0.47, 0], [x_target, y + 0.62, 0], color=LIGHT_GRAY, dash_length=0.07)
        target_tag = self.chip("TARGET", width=1.05, height=0.40, size=14).move_to([x_target - 0.95, y + 0.48, 0])
        lr = self.runner_icon(0.42).move_to([x_l, y + 0.62, 0])
        lt = self.tortoise_icon(0.48).move_to([x_target, y + 0.10, 0])
        return {"title": lens_title, "meta": meta, "baseline": baseline, "target": target, "target_tag": target_tag,
            "runner": lr, "tortoise": lt, "x_l": x_l, "x_target": x_target, "x_r": x_r, "y": y}

    def stage_meta(self, stage, a0, a1, dt, gap):
        return self.math(rf"\text{{Stage {stage}}}\quad [{a0},{a1}]\,\mathrm{{m}}\quad \Delta t={dt}\,\mathrm{{s}}", 24).move_to([0, -1.02, 0])

    def gap_bracket(self, lens, gap_text):
        y = lens["y"] - 0.55
        line = Line([lens["x_target"], y, 0], [lens["x_r"], y, 0], color=MID_GRAY, stroke_width=3.5)
        caps = VGroup(Line(line.get_start() + DOWN * 0.10, line.get_start() + UP * 0.10, color=MID_GRAY, stroke_width=2),
            Line(line.get_end() + DOWN * 0.10, line.get_end() + UP * 0.10, color=MID_GRAY, stroke_width=2))
        label = self.math(rf"\text{{new gap}}={gap_text}\,\mathrm{{m}}", 24).next_to(line, DOWN, buff=0.08)
        return VGroup(line, caps, label)

    def analyze_intervals(self, m):
        self.set_header(3, "ONE GAP, MAGNIFIED AGAIN AND AGAIN",
            "The race stays visible above. Only the selected interval is recentered and magnified inside the same analysis panel.")
        lens = self.make_lens_contents()
        self.play(FadeOut(m["intro_content"]), FadeOut(m["current_interval_label"]), FadeIn(lens["title"]), FadeIn(lens["meta"]),
            Create(lens["baseline"]), Create(lens["target"]), Write(lens["target_tag"]), FadeIn(lens["runner"]), FadeIn(lens["tortoise"]), run_time=RUN_SLOW)
        specs = [(1,0.0,10.0,10.0,11.0,"1","1"),(2,10.0,11.0,11.0,11.1,"0.1","0.1"),
                 (3,11.0,11.1,11.1,11.11,"0.01","0.01"),(4,11.1,11.11,11.11,11.111,"0.001","0.001")]
        checkpoint_dots = VGroup(); gap_visual = None
        for index,(stage,a0,a1,t0,t1,dt,gap) in enumerate(specs):
            if index>0:
                new_meta=self.stage_meta(stage,f"{a0:g}",f"{a1:g}",dt,gap)
                new_band=self.interval_band(m["track"],a0,a1); new_connectors=self.connector_pair(new_band,m["panel"])
                self.play(lens["runner"].animate.move_to([lens["x_l"],lens["y"]+0.62,0]),
                    lens["tortoise"].animate.move_to([lens["x_target"],lens["y"]+0.10,0]), Transform(lens["meta"],new_meta),
                    Transform(m["band"],new_band),Transform(m["connectors"],new_connectors),FadeOut(gap_visual),run_time=RUN_CAMERA,rate_func=smooth)
            self.play(m["runner"].animate.move_to(m["track"].n2p(a1)+UP*1.30),
                m["tortoise"].animate.move_to(m["track"].n2p(t1)+UP*0.12),
                lens["runner"].animate.move_to([lens["x_target"],lens["y"]+0.62,0]),
                lens["tortoise"].animate.move_to([lens["x_r"],lens["y"]+0.10,0]),
                run_time=2.7 if stage==1 else 2.25,rate_func=linear)
            dot=Dot(m["track"].n2p(a1),radius=0.055,color=BLACK); checkpoint_dots.add(dot)
            gap_visual=self.gap_bracket(lens,gap)
            self.play(GrowFromCenter(dot),Create(gap_visual[0]),Create(gap_visual[1]),Write(gap_visual[2]),run_time=RUN_NORMAL)
            cue=self.text("This remaining gap becomes the next magnified interval." if stage<4 else
                "The same recenter-and-magnify step can continue without end.",20,BOLD).move_to([0,-3.45,0])
            self.play(Write(cue),run_time=RUN_NORMAL);self.wait(PAUSE_READ);self.play(FadeOut(cue),run_time=RUN_QUICK)
            gap_band=self.interval_band(m["track"],a1,t1);gap_connectors=self.connector_pair(gap_band,m["panel"])
            self.play(Transform(m["band"],gap_band),Transform(m["connectors"],gap_connectors),run_time=RUN_NORMAL)
        pattern=VGroup(self.math(r"10\rightarrow1\rightarrow0.1\rightarrow0.01\rightarrow0.001\rightarrow\cdots",31),
            self.math(r"g_n=10\left(\frac{1}{10}\right)^n",34),self.math(r"\lim_{n\to\infty}g_n=0",36)).arrange(DOWN,buff=0.17).move_to([0,-2.05,0])
        self.play(FadeOut(lens["meta"]),FadeOut(lens["target_tag"]),FadeOut(gap_visual),FadeOut(lens["runner"]),FadeOut(lens["tortoise"]),
            FadeOut(lens["target"]),FadeOut(lens["baseline"]),Transform(lens["title"],self.text("THE REPEATING PATTERN",22,BOLD).move_to([0,-0.62,0])),
            FadeIn(pattern,shift=UP*0.08),run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        m["lens_title"],m["pattern"],m["checkpoint_dots"]=lens["title"],pattern,checkpoint_dots

    def convergence(self, m):
        self.set_header(4,"INFINITELY MANY STAGES, FINITE TOTAL TIME",
            "Now turn the repeated checkpoints into a geometric sequence of time intervals.")
        self.play(FadeOut(m["pattern"]),FadeOut(m["connectors"]),FadeOut(m["band"]),run_time=RUN_NORMAL)
        self.play(Transform(m["lens_title"],self.text("FROM CHECKPOINT TIMES TO A LIMIT",22,BOLD).move_to([0,-0.58,0])),run_time=RUN_NORMAL)
        left_title=self.text("STEP 1  ·  TIME INTERVALS",18,BOLD).move_to([-3.65,-1.00,0])
        right_title=self.text("STEP 2  ·  PARTIAL SUMS",18,BOLD).move_to([3.35,-1.00,0])
        times=VGroup(self.math(r"\Delta t_1=1\,\mathrm{s}",26),self.math(r"\Delta t_2=0.1\,\mathrm{s}",26),
            self.math(r"\Delta t_3=0.01\,\mathrm{s}",26),self.math(r"\Delta t_4=0.001\,\mathrm{s}",26)).arrange(DOWN,aligned_edge=LEFT,buff=0.12).move_to([-3.72,-2.02,0])
        ratio_arrows=VGroup()
        for a,b in zip(times[:-1],times[1:]):
            arrow=Arrow(a.get_right()+RIGHT*0.16,b.get_right()+RIGHT*0.16,buff=0.02,color=MID_GRAY,stroke_width=1.5,max_tip_length_to_length_ratio=0.12)
            label=self.math(r"\times\frac{1}{10}",18).next_to(arrow,RIGHT,buff=0.05);ratio_arrows.add(VGroup(arrow,label))
        partials=VGroup(self.math(r"S_1=1.000",25),self.math(r"S_2=1.100",25),self.math(r"S_3=1.110",25),self.math(r"S_4=1.111",25)).arrange(DOWN,aligned_edge=LEFT,buff=0.14).move_to([3.25,-2.02,0])
        divider=Line([0,-0.92,0],[0,-3.10,0],color=LIGHT_GRAY,stroke_width=1.4)
        self.play(Write(left_title),Write(right_title),Create(divider),run_time=RUN_NORMAL)
        for i in range(4):
            self.play(Write(times[i]),Write(partials[i]),run_time=RUN_NORMAL)
            if i<3:self.play(GrowArrow(ratio_arrows[i][0]),Write(ratio_arrows[i][1]),run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT*0.35)
        pattern_line=self.math(r"\Delta t_n=\left(\frac{1}{10}\right)^{n-1}\mathrm{s}",29).move_to([0,-3.35,0])
        self.play(Write(pattern_line),run_time=RUN_NORMAL);self.wait(PAUSE_READ)
        step1_group=VGroup(left_title,right_title,times,ratio_arrows,partials,divider,pattern_line)
        self.play(FadeOut(step1_group),run_time=RUN_NORMAL)
        deriv_title=self.text("STEP 3  ·  WRITE A FINITE PARTIAL SUM",19,BOLD).move_to([0,-0.98,0])
        sN_1=self.math(r"S_N=1+\frac{1}{10}+\frac{1}{10^2}+\cdots+\frac{1}{10^{N-1}}",31).move_to([0,-1.58,0])
        sN_2=self.math(r"S_N=\frac{1-\left(\frac{1}{10}\right)^N}{1-\frac{1}{10}}",34).move_to([0,-2.28,0])
        reason=self.text("This is a finite geometric sum, so no infinity has been used yet.",20,BOLD).move_to([0,-2.93,0])
        self.play(Write(deriv_title),run_time=RUN_NORMAL);self.play(Write(sN_1),run_time=RUN_NORMAL)
        self.play(TransformFromCopy(sN_1,sN_2),run_time=RUN_SLOW);self.play(Write(reason),run_time=RUN_NORMAL);self.wait(PAUSE_READ)
        step4_title=self.text("STEP 4  ·  TAKE THE LIMIT",19,BOLD).move_to([0,-0.98,0])
        limit_fact=self.math(r"\left(\frac{1}{10}\right)^N\longrightarrow 0\qquad(N\to\infty)",30).move_to([0,-1.58,0])
        limit_eq=self.math(r"T=\lim_{N\to\infty}S_N=\frac{1-0}{1-\frac{1}{10}}=\frac{10}{9}\,\mathrm{s}",34).move_to([0,-2.30,0])
        decimal_bridge=self.math(r"1.000\;\to\;1.100\;\to\;1.110\;\to\;1.111\;\to\;\cdots\;\to\;1.111\ldots",26).move_to([0,-3.05,0])
        conclusion=self.text("Infinitely many checkpoints accumulate at a finite time.",21,BOLD).move_to([0,-3.52,0])
        self.play(ReplacementTransform(deriv_title,step4_title),FadeOut(sN_1),FadeOut(sN_2),FadeOut(reason),run_time=RUN_NORMAL)
        self.play(Write(limit_fact),run_time=RUN_NORMAL);self.play(Write(limit_eq),run_time=RUN_SLOW)
        self.play(Write(decimal_bridge),run_time=RUN_NORMAL);self.play(Write(conclusion),run_time=RUN_NORMAL);self.wait(PAUSE_SUMMARY)
        m["time_group"]=VGroup(step4_title,limit_fact,limit_eq,decimal_bridge,conclusion)

    def final_catch(self, m):
        self.set_header(5,"THE LIMIT IS THE PHYSICAL MEETING",
            "The limiting checkpoint time is exactly the ordinary catch time found at the start.")
        self.play(FadeOut(m["time_group"]),run_time=RUN_NORMAL)
        final_results=VGroup(self.math(r"\boxed{t^*=\frac{10}{9}\,\mathrm{s}=1.111\ldots\,\mathrm{s}}",32),
            self.math(r"\boxed{x^*=\frac{100}{9}\,\mathrm{m}=11.111\ldots\,\mathrm{m}}",32)).arrange(DOWN,buff=0.22).move_to([0,-1.95,0])
        synthesis=self.text("Zeno gives infinitely many checkpoints; the limit gives one finite meeting.",21,BOLD).move_to([0,-3.12,0])
        self.play(Transform(m["lens_title"],self.text("FINAL RESULT",22,BOLD).move_to([0,-0.62,0])),FadeIn(final_results,shift=UP*0.06),run_time=RUN_NORMAL)
        self.play(Write(synthesis),run_time=RUN_NORMAL)
        self.play(m["runner"].animate.move_to(m["track"].n2p(self.X_CATCH)+UP*1.30),m["tortoise"].animate.move_to(m["track"].n2p(self.X_CATCH)+UP*0.12),run_time=2.2,rate_func=smooth)
        meet_x=m["track"].n2p(self.X_CATCH)[0]
        final_formula=self.math(r"x^*=\frac{100}{9}\,\mathrm{m}",22);final_label=self.text("MEETING POINT",16,BOLD)
        final_callout_text=VGroup(final_formula,final_label).arrange(DOWN,buff=0.03)
        final_box=SurroundingRectangle(final_callout_text,buff=0.08,color=BLACK_LINE,stroke_width=1.5,fill_color=WHITE,fill_opacity=1)
        final_callout=VGroup(final_box,final_callout_text).move_to([4.15,2.42,0])
        final_arrow=Arrow(final_callout.get_corner(DR),[meet_x,1.62,0],buff=0.08,color=MID_GRAY,stroke_width=1.6,max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(final_callout),GrowArrow(final_arrow),Indicate(m["meet_line"],scale_factor=1.01),run_time=RUN_NORMAL);self.wait(PAUSE_READ)
        self.play(m["runner"].animate.move_to(m["track"].n2p(11.65)+UP*1.30),m["tortoise"].animate.move_to(m["track"].n2p(11.165)+UP*0.12),run_time=1.75,rate_func=linear)
        overtake=self.text("For every t > 10/9 s, Achilles is ahead.",21,BOLD).move_to([0,-3.52,0])
        self.play(ReplacementTransform(synthesis,overtake),run_time=RUN_NORMAL);self.wait(PAUSE_FINAL)

    def construct(self):
        master=self.build_master_scene()
        self.physical_meeting(master)
        self.zeno_reframe(master)
        self.analyze_intervals(master)
        self.convergence(master)
        self.final_catch(master)
