from manim import *
from core.visual_engine import AcademicScene, make_badge
from core.software_tools import make_pointer_arrow

class PolymorphismDemo(AcademicScene):
    def construct(self):
        header = self.transition_section("Dynamic Dispatch: Virtual Functions")

        # Setup Objects
        base_ptr = Square(side_length=0.8, color=BLUE).to_edge(LEFT, buff=1.5)
        ptr_label = Text("Animal* ptr", color=BLUE).scale(0.4).next_to(base_ptr, UP)

        dog_obj = Circle(radius=0.7, color=GREEN, fill_opacity=0.2).shift(RIGHT*2 + UP*1.5)
        dog_label = Text("Perro", color=GREEN).scale(0.5).move_to(dog_obj)
        
        cat_obj = Circle(radius=0.7, color=ORANGE, fill_opacity=0.2).shift(RIGHT*2 + DOWN*1.5)
        cat_label = Text("Gato", color=ORANGE).scale(0.5).move_to(cat_obj)

        self.play(FadeIn(base_ptr, ptr_label), FadeIn(dog_obj, dog_label, cat_obj, cat_label))

        # Scenario A: Pointing to Dog
        arrow = make_pointer_arrow(base_ptr, dog_obj, label="ptr = new Perro()")
        call_label = Text("ptr->hablar()", color=BLACK).scale(0.6).to_edge(DOWN, buff=1.5)
        output_dog = make_badge("Output: ¡Guau!", color=GREEN).next_to(call_label, RIGHT)

        self.play(Create(arrow))
        self.play(Write(call_label))
        self.play(FadeIn(output_dog))
        self.wait()

        # Scenario B: Re-pointing to Cat (Polymorphism)
        arrow_cat = make_pointer_arrow(base_ptr, cat_obj, label="ptr = new Gato()")
        output_cat = make_badge("Output: ¡Miau!", color=ORANGE).move_to(output_dog)

        self.play(
            ReplacementTransform(arrow, arrow_cat),
            ReplacementTransform(output_dog, output_cat),
            run_time=2
        )
        self.wait(2)