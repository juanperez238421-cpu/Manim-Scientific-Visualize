from manim import *
import numpy as np

class TurbineGeometry(ThreeDScene):
    def setup(self):
        self.camera.background_color = "#ffffff"

    def construct(self):
        axes = ThreeDAxes(axis_config={"color": BLACK})
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Parametric Surface: The Vortex Basin
        # r(u, v) = [v*cos(u), v*sin(u), 0.5 * v**2]
        basin = Surface(
            lambda u, v: np.array([
                v * np.cos(u),
                v * np.sin(u),
                0.2 * (v**2) # Parabolic basin shape
            ]),
            u_range=[0, TAU],
            v_range=[0.5, 3],
            checkerboard_colors=[GREY_B, GREY_D],
            fill_opacity=0.4
        )

        # The Impeller (Simplified)
        impeller = Cylinder(radius=0.6, height=1.5, color=BLUE_E, fill_opacity=0.8)
        impeller.rotate(90*DEGREES, axis=RIGHT)
        impeller.move_to(ORIGIN + UP*0.5)

        # Labels
        labels = self.get_axis_labels(axes)
        title = Text("GWVT Parametric Model", color=BLACK).to_corner(UL).scale(0.6)
        self.add_fixed_in_frame_mobjects(title)

        # Animation
        self.play(Create(axes), Write(labels))
        self.play(Create(basin), run_time=2)
        self.play(FadeIn(impeller, shift=UP))
        
        # Rotate camera to show geometry
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()