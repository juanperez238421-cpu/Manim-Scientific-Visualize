from manim import *
from core.visual_engine import AcademicScene, make_paragraph
from core.software_tools import make_memory_cell

class DynamicAllocation(AcademicScene):
    def construct(self):
        header = self.transition_section("Manual Memory Management: Heap vs Stack")

        # Define Areas
        stack_label = Text("STACK (Automatic)", color=GRAY).scale(0.5).to_edge(LEFT, buff=1)
        heap_label = Text("HEAP (Manual / Dynamic)", color=BLUE).scale(0.5).to_edge(RIGHT, buff=1)
        
        # 1. Stack Allocation
        ptr_in_stack = make_memory_cell("0xAA01", "0xBB04", color=GREY_B).next_to(stack_label, DOWN, buff=0.5)
        caption_1 = make_paragraph("Pointer 'p' is allocated on the Stack, storing a Heap address.")
        
        self.play(Write(stack_label), Write(heap_label))
        self.play(Create(ptr_in_stack), FadeIn(caption_1))
        self.wait()

        # 2. Heap Allocation (new)
        data_in_heap = make_memory_cell("0xBB04", "Value", color=BLUE_B).next_to(heap_label, DOWN, buff=0.5)
        conn = Line(ptr_in_stack.get_right(), data_in_heap.get_left(), color=BLUE).add_tip()
        
        self.play(Create(data_in_heap), Create(conn))
        self.wait()

        # 3. The Memory Leak (p = nullptr without delete)
        self.play(FadeOut(caption_1))
        caption_leak = make_paragraph("Memory Leak: Setting p to nullptr without 'delete' leaves data orphaned on the Heap.", color=RED)
        
        self.play(
            ptr_in_stack[2].animate.set_text("NULL"),
            FadeOut(conn),
            FadeIn(caption_leak)
        )
        data_in_heap.set_color(RED)
        self.wait(2)