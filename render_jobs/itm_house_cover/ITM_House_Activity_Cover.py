from manim import *

config.background_color = WHITE
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30


class ITMHouseActivityCover(Scene):
    """Standalone cover only. The house animation is not rendered here."""

    def construct(self):
        # Official ITM logo is downloaded by the render workflow.
        logo = ImageMobject("assets/logo_ITM.png")
        logo.set_width(4.9)
        logo.move_to(UP * 1.75)

        title = Tex(
            r"\textbf{Actividad: Modelado CAD y Dise\~no de Vivienda}",
            color=BLACK,
            font_size=44,
        )
        title.set_width(min(title.width, 11.8))
        title.move_to(DOWN * 0.55)

        weight_total = Tex(
            r"\textbf{Valor de la actividad: }10\%\textbf{ de la nota total}",
            color=BLACK,
            font_size=36,
        )
        weight_total.move_to(DOWN * 1.55)

        weight_house = Tex(
            r"Representaci\'on de la vivienda (plano + modelo 3D): \textbf{4\%}",
            color=BLACK,
            font_size=31,
        )
        weight_house.move_to(DOWN * 2.35)

        divider = Line(LEFT * 4.7, RIGHT * 4.7, color=GREY_B, stroke_width=1.5)
        divider.move_to(DOWN * 0.05)

        self.wait(0.7)
        self.play(FadeIn(logo, shift=UP * 0.12), run_time=1.2)
        self.wait(0.8)
        self.play(Create(divider), run_time=0.6)
        self.play(Write(title), run_time=1.6)
        self.wait(1.0)
        self.play(Write(weight_total), run_time=1.25)
        self.wait(0.8)
        self.play(Write(weight_house), run_time=1.35)
        self.wait(2.0)
