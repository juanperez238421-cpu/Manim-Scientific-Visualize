from manim import *
from core.visual_engine import AcademicScene, make_badge
from core.software_tools import make_memory_cell, make_pointer_arrow

class PointerArithmetic(AcademicScene):
    def construct(self):
        header = self.transition_section("C++ Pointer Arithmetic & Referencing")

        # 1. Create a Memory Block (Array of integers)
        addresses = ["0x7ff1", "0x7ff5", "0x7ff9", "0x7ffd"]
        values = [42, 10, 88, 5]
        cells = VGroup(*[
            make_memory_cell(addresses[i], values[i]) for i in range(len(values))
        ]).arrange(RIGHT, buff=0.1).shift(UP*0.5)

        self.play(Create(cells))
        self.wait()

        # 2. Visualize Pointer 'p'
        ptr_label = Text("int* p = &arr[0];", color=BLUE).scale(0.5)
        ptr_arrow = Arrow(UP*2, cells[0].get_top(), color=BLUE, buff=0.1)
        ptr_group = VGroup(ptr_label.next_to(ptr_arrow, UP), ptr_arrow)

        self.play(FadeIn(ptr_group))
        
        # 3. Explain Dereferencing
        badge_val = make_badge("*p = 42", color=GREEN).next_to(cells[0], DOWN, buff=1)
        self.play(FadeIn(badge_val))
        self.wait()

        # 4. Arithmetic: p + 2
        self.play(FadeOut(badge_val))
        new_ptr_label = Text("p = p + 2;", color=ORANGE).scale(0.5).move_to(ptr_label)
        
        self.play(
            ptr_arrow.animate.next_to(cells[2].get_top(), UP, buff=0.1),
            Transform(ptr_label, new_ptr_label),
            run_time=2
        )
        
        badge_addr = make_badge("Address: 0x7ff9", color=ORANGE).next_to(cells[2], DOWN, buff=1)
        self.play(FadeIn(badge_addr))
        self.wait(2)