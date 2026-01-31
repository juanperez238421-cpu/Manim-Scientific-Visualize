from manim import *
from core.visual_engine import AcademicScene, make_badge
from core.physics_tools import draw_point_load, make_beam_support

class BeamAnalyzer(AcademicScene):
    def construct(self):
        # 1. Problem Definition
        L = 10  # Beam length
        P = 500 # Load in Newtons
        a = 5   # Load position
        
        header = self.transition_section("Shear (V) & Bending Moment (M) Analysis")
        
        # 2. Structural Setup
        beam = Line(LEFT*5, RIGHT*5, color=BLACK, stroke_width=6).shift(UP*0.5)
        support_a = make_beam_support(beam.get_left(), type="pin")
        support_b = make_beam_support(beam.get_right(), type="roller")
        load = draw_point_load(beam.get_center(), P, label_text="500 N")
        
        self.play(Create(beam), FadeIn(support_a), FadeIn(support_b))
        self.play(FadeIn(load))
        self.wait()

        # 3. Shear Diagram (V)
        axes_v = Axes(x_range=[0, 10, 1], y_range=[-300, 300, 100], 
                      x_length=8, y_length=3, axis_config={"color": BLACK}).scale(0.7).shift(DOWN*1.5)
        v_label = Text("V (N)", color=BLACK).scale(0.4).next_to(axes_v, UP, buff=0.1)
        
        # V(x) = 250 (0 < x < 5), V(x) = -250 (5 < x < 10)
        v_graph = VGroup(
            axes_v.plot_line_graph([0, 5, 5, 10], [250, 250, -250, -250], add_vertex_dots=False, line_color=BLUE)
        )
        
        self.play(Create(axes_v), Write(v_label))
        self.play(Create(v_graph), run_time=2)
        self.wait()

        # 4. Bending Moment Diagram (M)
        # Transformation to Moment
        axes_m = axes_v.copy()
        m_label = Text("M (N·m)", color=BLACK).scale(0.4).next_to(axes_m, UP, buff=0.1)
        m_graph = axes_m.plot(lambda x: 250*x if x <= 5 else 250*(10-x), x_range=[0, 10], color=GREEN)
        
        self.play(ReplacementTransform(v_graph, m_graph), ReplacementTransform(v_label, m_label))
        max_m = make_badge("M_max = 1250 Nm", color=GREEN).next_to(m_graph.get_top(), UP, buff=0.1)
        self.play(FadeIn(max_m))
        self.wait(2)