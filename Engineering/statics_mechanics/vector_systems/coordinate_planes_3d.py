from manim import *
import numpy as np

class CoordinatePlanes3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)

        axes = ThreeDAxes(axis_config={"color": BLACK, "stroke_width": 1}).set_opacity(0.4)
        
        # XY Plane representation (from your P.py logic)
        xy_plane = Polygon(
            [-4, -3, 0], [4, -3, 0], [4, 3, 0], [-4, 3, 0],
            color=BLACK, stroke_width=1, fill_color=GRAY, fill_opacity=0.2
        )
        
        vector = Arrow3D(start=[0,0,0], end=[2,2,3], color=RED)
        
        self.add(axes, xy_plane)
        self.play(Create(vector))
        self.wait()