from manim import *
from core.visual_engine import AcademicScene, make_paragraph
from core.software_tools import make_uml_class

class InheritancePatterns(AcademicScene):
    def construct(self):
        header = self.transition_section("OOP: Inheritance & UML Relationships")

        # 1. Define Base Class
        base_class = make_uml_class(
            "Vehicle", 
            ["speed: float", "fuel: int"], 
            ["move()", "stop()"]
        ).shift(UP * 1.5)

        # 2. Define Derived Class
        derived_class = make_uml_class(
            "ElectricCar", 
            ["battery_lvl: int"], 
            ["charge()", "move() override"]
        ).shift(DOWN * 1.5)

        # 3. Inheritance Connector (Triangular tip per UML standard)
        # Using a specialized arrow to represent generalization
        conn = Arrow(
            derived_class.get_top(), 
            base_class.get_bottom(), 
            buff=0.1, 
            color=BLACK,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Hollow triangle tip (standard UML Generalization)
        tip = Triangle(color=BLACK, fill_opacity=1).scale(0.15).move_to(base_class.get_bottom() + DOWN*0.1)

        self.play(FadeIn(base_class))
        self.play(make_paragraph("Base Class: Defines common attributes and behaviors."))
        self.wait()

        self.play(FadeIn(derived_class), Create(conn), Create(tip))
        self.play(make_paragraph("Derived Class: Inherits members and adds specialized functionality."))
        self.wait(2)