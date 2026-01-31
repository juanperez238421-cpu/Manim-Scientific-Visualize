from manim import *
from core.visual_engine import AcademicScene, make_badge
from core.software_tools import make_node_box, make_pointer_arrow

class LinkedListsMaster(AcademicScene):
    def construct(self):
        header = self.transition_section("Linked Lists: SLL, DLL, and Circular Logic")

        # 1. Doubly Linked List (DLL) Setup
        vals = [10, 20, 30]
        nodes = VGroup(*[
            make_node_box(v, pointer_label="prev | next", width=2.5) 
            for v in vals
        ]).arrange(RIGHT, buff=1.5).shift(UP*0.5)

        # Draw bidirectional arrows
        arrows = VGroup()
        for i in range(len(nodes)-1):
            fw = make_pointer_arrow(nodes[i], nodes[i+1])
            bw = make_pointer_arrow(nodes[i+1], nodes[i]).shift(DOWN*0.3)
            arrows.add(fw, bw)

        self.play(Create(nodes), Create(arrows))
        self.wait()

        # 2. Node Insertion Shifting (Inserting 25 between 20 and 30)
        new_node = make_node_box(25, pointer_label="prev | next", width=2.5).shift(DOWN*2 + RIGHT*0.75)
        self.play(FadeIn(new_node), nodes[2].animate.shift(RIGHT*2), arrows[2:].animate.shift(RIGHT*2))
        
        # Re-linking
        new_arrows = VGroup(
            make_pointer_arrow(nodes[1], new_node),
            make_pointer_arrow(new_node, nodes[2])
        )
        self.play(Create(new_arrows))
        self.play(make_badge("O(1) Insertion", color=GREEN).to_edge(RIGHT))
        self.wait(2)

        # 3. Circular Logic (CSLL)
        self.play(FadeOut(new_node), FadeOut(new_arrows), nodes[2].animate.shift(LEFT*2), arrows[2:].animate.shift(LEFT*2))
        wrap_arrow = CurvedArrow(nodes[2].get_bottom(), nodes[0].get_bottom(), angle=-TAU/4, color=BLUE)
        self.play(Create(wrap_arrow))
        self.play(make_badge("Circular: tail -> head", color=ORANGE).next_to(wrap_arrow, DOWN))
        self.wait(2)