from manim import *

from inventor_sketch_to_volume_3d import (
    BG,
    HOLE,
    NAVY_D,
    InventorSketchToVolume3D,
)


class InventorSketchToVolume3DDelivery(InventorSketchToVolume3D):
    """Fast high-quality delivery class preserving the true polygonal 3D solid."""

    def visual_hole(self, x, y, r, depth):
        top_open = Circle(
            radius=r * 0.98,
            fill_color=BG,
            fill_opacity=1,
            stroke_color=NAVY_D,
            stroke_width=1.35,
        ).move_to([x, y, depth + 0.008])
        top_open.set_shade_in_3d(True)

        bottom_open = Circle(
            radius=r * 0.98,
            fill_color=BG,
            fill_opacity=1,
            stroke_color=HOLE,
            stroke_width=1.0,
        ).move_to([x, y, -0.008])
        bottom_open.set_shade_in_3d(True)
        return VGroup(top_open, bottom_open)
