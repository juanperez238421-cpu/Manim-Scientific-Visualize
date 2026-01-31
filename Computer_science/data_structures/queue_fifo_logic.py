from manim import *
from core.visual_engine import AcademicScene, make_paragraph
from core.software_tools import make_memory_cell

class QueueFIFOLogic(AcademicScene):
    def construct(self):
        header = self.transition_section("Queue Implementation: FIFO Logic")

        # 1. Create Linear Queue (Array-based representation)
        queue_cells = VGroup(*[
            make_memory_cell(f"idx_{i}", value=v if i < 3 else "") 
            for i, v in enumerate([10, 20, 30, "", ""])
        ]).arrange(RIGHT, buff=0.1)

        # 2. Front and Rear Pointers
        front_ptr = Arrow(UP*1.5, queue_cells[0].get_top(), color=RED).add_tip()
        front_label = Text("FRONT", color=RED).scale(0.4).next_to(front_ptr, UP)
        
        rear_ptr = Arrow(DOWN*1.5, queue_cells[2].get_bottom(), color=BLUE).add_tip()
        rear_label = Text("REAR", color=BLUE).scale(0.4).next_to(rear_ptr, DOWN)

        self.play(Create(queue_cells), FadeIn(front_ptr, front_label, rear_ptr, rear_label))
        self.wait()

        # 3. Enqueue Operation (Push 40)
        caption_enq = make_paragraph("Enqueue: Element added at REAR, pointer moves to idx_3.")
        self.play(FadeIn(caption_enq))
        self.play(
            queue_cells[3][2].animate.set_text("40"),
            rear_ptr.animate.next_to(queue_cells[3].get_bottom(), DOWN, buff=0.1),
            rear_label.animate.next_to(queue_cells[3], DOWN, buff=1.2)
        )
        self.wait()

        # 4. Dequeue Operation (Pop 10)
        self.play(FadeOut(caption_enq))
        caption_deq = make_paragraph("Dequeue: Element removed from FRONT, pointer moves to idx_1.")
        self.play(FadeIn(caption_deq))
        self.play(
            queue_cells[0][2].animate.set_text(""),
            queue_cells[0][0].animate.set_stroke(opacity=0.2),
            front_ptr.animate.next_to(queue_cells[1].get_top(), UP, buff=0.1),
            front_label.animate.next_to(queue_cells[1], UP, buff=1.2)
        )
        self.wait(2)