"""Public scene classes composing the standard mixins."""
from __future__ import annotations
from manim import *
from .core import CoreMixin
from .panels import PanelsMixin
from .tables import TablesMixin
from .equations import EquationsMixin
from .opening import OpeningMixin
from .theme import *

class JPClassroomScene(CoreMixin, PanelsMixin, TablesMixin, EquationsMixin, OpeningMixin, MovingCameraScene):
    """Canonical 2D/moving-camera classroom scene."""

class JPMathClassroomScene(JPClassroomScene):
    """Semantic alias for mathematics/statistics/physics 2D lessons."""

class JPThreeDClassroomScene(PanelsMixin, EquationsMixin, OpeningMixin, ThreeDScene):
    """3D companion preserving typography and visual constants."""
    def setup(self) -> None:
        super().setup(); self.camera.background_color = WHITE; self.validate_lesson_data()
    def validate_lesson_data(self) -> None:
        pass
    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Text:
        return Text(content, font_size=size, color=BLACK_TEXT, weight=weight, **kwargs)
    def math(self, expression: str, size: int = 38, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT, **kwargs)
    def fit(self, mob: Mobject, max_width: float = SAFE_WIDTH, max_height: float = SAFE_HEIGHT) -> Mobject:
        if mob.width > max_width: mob.scale_to_fit_width(max_width)
        if mob.height > max_height: mob.scale_to_fit_height(max_height)
        return mob
