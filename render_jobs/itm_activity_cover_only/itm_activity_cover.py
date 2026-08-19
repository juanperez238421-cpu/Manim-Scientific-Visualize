from pathlib import Path

from manim import (
    BLUE_E,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Create,
    FadeIn,
    FadeOut,
    ImageMobject,
    Line,
    Scene,
    Tex,
    VGroup,
    Write,
    config,
)


config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = WHITE

BLUE_ITM = "#005DAA"
TEXT_DARK = "#18324A"
TEXT_MUTED = "#516272"


class ITMActivityCover(Scene):
    """Portada universal; se renderiza sin volver a procesar el modelo 3D."""

    def construct(self):
        logo_path = Path(__file__).resolve().parent / "assets" / "itm_logo.png"
        logo = ImageMobject(str(logo_path)).set_width(9.6).to_edge(UP, buff=0.52)

        activity = Tex(
            r"\textbf{ACTIVIDAD}",
            font_size=34,
            color=BLUE_ITM,
        )
        title = Tex(
            r"\textbf{CROQUIS, EXTRUSIÓN Y MODELO 3D CAD}",
            font_size=45,
            color=TEXT_DARK,
        )
        rule = Line(5.8 * LEFT, 5.8 * RIGHT, color=BLUE_E, stroke_width=3)
        value_total = Tex(
            r"\textbf{VALOR DE LA ACTIVIDAD: 10\% DE LA NOTA TOTAL}",
            font_size=34,
            color=BLUE_ITM,
        )
        value_delivery = Tex(
            r"\textbf{VALOR DE ESTA ENTREGA: 4\% DEL 10\%}",
            font_size=31,
            color=TEXT_MUTED,
        )

        text_block = VGroup(activity, title, rule, value_total, value_delivery)
        text_block.arrange(DOWN, buff=0.32).shift(1.15 * DOWN)

        self.play(FadeIn(logo, shift=0.18 * DOWN), run_time=1.10)
        self.play(Write(activity), run_time=0.65)
        self.play(Write(title), run_time=1.30)
        self.play(Create(rule), run_time=0.45)
        self.play(Write(value_total), run_time=1.10)
        self.play(Write(value_delivery), run_time=1.05)
        self.wait(2.60)
        self.play(FadeOut(VGroup(activity, title, rule, value_total, value_delivery)), FadeOut(logo), run_time=0.80)
