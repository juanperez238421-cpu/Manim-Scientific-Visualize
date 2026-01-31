from manim import *
from core.visual_engine import AcademicScene, make_badge
from core.software_tools import make_uml_class

class EncapsulationMCQ(AcademicScene):
    def construct(self):
        header = self.transition_section("Assessment: Encapsulation & Access Modifiers")

        # 1. Code Snippet to analyze
        code_uml = make_uml_class(
            "Account",
            ["- balance: double", "# id: int"],
            ["+ get_balance()"]
        ).scale(0.8).to_edge(LEFT, buff=1)

        question = Text("Which member is accessible only within the class and its children?", 
                        color=BLACK).scale(0.45).next_to(header, DOWN, buff=0.5)

        options = VGroup(
            Text("A) balance (private)", color=BLACK),
            Text("B) id (protected)", color=BLACK),
            Text("C) get_balance (public)", color=BLACK),
            Text("D) None of the above", color=BLACK)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(question, DOWN, buff=0.8).shift(RIGHT*2)

        self.play(FadeIn(code_uml), Write(question))
        self.play(LaggedStart(*[Write(opt) for opt in options], lag_ratio=0.5))
        self.wait(2)

        # 2. Reveal Answer
        correct_box = SurroundingRectangle(options[1], color=GREEN, buff=0.1)
        feedback = make_badge("Correct: Protected (#) allows child access.", color=GREEN).next_to(options[1], RIGHT)
        
        self.play(Create(correct_box))
        self.play(FadeIn(feedback))
        self.wait(3)