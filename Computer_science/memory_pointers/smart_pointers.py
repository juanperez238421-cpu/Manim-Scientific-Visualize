from manim import *
from core.visual_engine import AcademicScene, make_badge
from core.software_tools import make_pointer_arrow

class SmartPointers(AcademicScene):
    def construct(self):
        header = self.transition_section("Modern C++: unique_ptr Ownership")

        # Heap Object
        heap_obj = RoundedRectangle(width=2, height=1.5, color=BLUE, fill_opacity=0.1).shift(RIGHT*3)
        obj_label = Text("Resource", color=BLUE).scale(0.4).move_to(heap_obj)
        
        # Pointers
        p1 = Square(side_length=1, color=BLACK).shift(LEFT*3 + UP*1)
        p1_label = Text("p1", color=BLACK).scale(0.5).next_to(p1, LEFT)
        
        p2 = Square(side_length=1, color=BLACK).shift(LEFT*3 + DOWN*1)
        p2_label = Text("p2", color=BLACK).scale(0.5).next_to(p2, LEFT)

        # 1. Initial Ownership
        arrow1 = make_pointer_arrow(p1, heap_obj, label="Owns")
        self.play(Create(p1), Write(p1_label), Create(heap_obj), Write(obj_label))
        self.play(Create(arrow1))
        self.wait()

        # 2. Move Semantics: std::move(p1)
        move_text = Text("std::move(p1)", color=ORANGE).scale(0.6).to_edge(UP, buff=1.5)
        self.play(Write(move_text))
        
        arrow2 = make_pointer_arrow(p2, heap_obj, label="New Owner")
        
        self.play(
            Create(p2), Write(p2_label),
            ReplacementTransform(arrow1, arrow2),
            p1.animate.set_stroke(opacity=0.3),
            run_time=2
        )
        
        badge = make_badge("p1 is now empty", color=RED).next_to(p1, UP)
        self.play(FadeIn(badge))
        self.wait(2)