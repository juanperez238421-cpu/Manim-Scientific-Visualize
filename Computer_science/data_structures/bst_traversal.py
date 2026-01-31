from manim import *
from core.visual_engine import AcademicScene, THEME

class BSTTraversal(AcademicScene):
    def construct(self):
        header = self.transition_section("Binary Search Tree: Recursive Traversal")

        # 1. Define Tree Coordinates (Manual tree layout)
        root_pos = UP*2
        l_child = LEFT*2 + ORIGIN
        r_child = RIGHT*2 + ORIGIN
        ll_child = LEFT*3 + DOWN*2
        lr_child = LEFT*1 + DOWN*2

        # 2. Nodes (Circles with Values)
        def bst_node(val, pos):
            c = Circle(radius=0.5, color=BLACK, fill_color=WHITE, fill_opacity=1).move_to(pos)
            t = Text(str(val), color=BLACK).scale(0.5).move_to(c)
            return VGroup(c, t)

        n50 = bst_node(50, root_pos)
        n30 = bst_node(30, l_child)
        n70 = bst_node(70, r_child)
        n20 = bst_node(20, ll_child)
        n40 = bst_node(40, lr_child)

        lines = VGroup(
            Line(n50.get_bottom(), n30.get_top()),
            Line(n50.get_bottom(), n70.get_top()),
            Line(n30.get_bottom(), n20.get_top()),
            Line(n30.get_bottom(), n40.get_top())
        ).set_color(GRAY)

        self.play(Create(lines), Create(VGroup(n50, n30, n70, n20, n40)))

        # 3. Search Animation (Find 40)
        search_target = Text("Search Target: 40", color=THEME["accent_orange"]).to_edge(LEFT, buff=1)
        self.play(Write(search_target))

        # Cursor Path
        cursor = Triangle(color=RED, fill_opacity=1).scale(0.2).rotate(PI)
        
        # Step 1: Root
        self.play(cursor.animate.next_to(n50, UP))
        self.play(Indicate(n50, color=ORANGE))
        self.play(make_paragraph("40 < 50: Moving to the left child.").scale(0.8))

        # Step 2: Left
        self.play(cursor.animate.next_to(n30, UP))
        self.play(Indicate(n30, color=ORANGE))
        self.play(make_paragraph("40 > 30: Moving to the right child.").scale(0.8))

        # Step 3: Target Found
        self.play(cursor.animate.next_to(n40, UP))
        self.play(n40[0].animate.set_fill(GREEN), Indicate(n40))
        self.play(make_paragraph("Target 40 found! Search completed.").scale(0.8))
        self.wait(2)