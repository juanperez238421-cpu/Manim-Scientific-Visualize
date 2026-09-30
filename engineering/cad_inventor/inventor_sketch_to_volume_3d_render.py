from manim import *

from inventor_sketch_to_volume_3d import (
    BG,
    HOLE,
    NAVY_D,
    InventorSketchToVolume3D,
)


class InventorSketchToVolume3DOptimized(InventorSketchToVolume3D):
    """Delivery renderer with reduced cylindrical tessellation and identical scene logic."""

    def visual_hole(self, x, y, r, depth):
        wall = Cylinder(
            radius=r,
            height=depth,
            direction=OUT,
            resolution=(4, 16),
            fill_color=HOLE,
            fill_opacity=1,
            stroke_color=HOLE,
            stroke_width=0.35,
        ).move_to([x, y, depth / 2])
        wall.set_shade_in_3d(True)

        top_open = Circle(
            radius=r * 0.96,
            fill_color=BG,
            fill_opacity=1,
            stroke_color=NAVY_D,
            stroke_width=1.1,
        ).move_to([x, y, depth + 0.006])
        top_open.set_shade_in_3d(True)
        return VGroup(wall, top_open)
