from manim import *
from core.visual_engine import AcademicScene, make_paragraph

class TrussAnalysis(AcademicScene):
    def construct(self):
        header = self.transition_section("Truss Analysis: Method of Sections")
        
        # Abstract Truss Geometry (Triangle-based)
        pts = [LEFT*3, ORIGIN, RIGHT*3, UP*2, UP*2 + LEFT*3]
        truss = VGroup(
            Line(pts[0], pts[1]), Line(pts[1], pts[2]), Line(pts[2], pts[3]),
            Line(pts[3], pts[4]), Line(pts[4], pts[0]), Line(pts[1], pts[3])
        ).set_color(GRAY).shift(DOWN*0.5)
        
        self.play(Create(truss))
        
        # The "Section" Line
        cut_line = Line(UP*2 + LEFT*1.5, DOWN*2 + LEFT*1.5, color=RED, stroke_width=2).set_dashed_ratio(0.5)
        cut_label = Text("Section n-n", color=RED).scale(0.4).next_to(cut_line, UP)
        
        self.play(Create(cut_line), Write(cut_label))
        self.wait()
        
        # Equation breakdown
        eq = MathTex(r"\sum M_{K} = 0 \implies F_{BC}(d) - A_y(x) = 0", color=BLACK).scale(0.8).to_edge(RIGHT, buff=1)
        caption = make_paragraph("Cutting the truss at elements KJ, KC, and BC to isolate the left segment.")
        
        self.play(Write(eq), FadeIn(caption))
        self.wait(3)