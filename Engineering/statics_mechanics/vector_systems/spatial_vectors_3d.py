from manim import *
import numpy as np
from core.visual_engine import THEME

class SpatialVectors(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#ffffff"
        axes = ThreeDAxes(axis_config={"color": BLACK})
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # Force Vector at P(2, 3, 4)
        p_coords = [2, 2, 3]
        f_vector_vals = [0, 0, -4] # Force pointing down
        
        start_pt = axes.c2p(*p_coords)
        end_pt = axes.c2p(*(np.array(p_coords) + np.array(f_vector_vals)))
        
        force_vec = Arrow3D(start=start_pt, end=end_pt, color=RED)
        label_f = MathTex(r"\mathbf{F} = -400\mathbf{k} \, \text{N}", color=RED).scale(0.8)
        
        # Position Vector r
        r_vec = Arrow3D(start=axes.c2p(0,0,0), end=start_pt, color=BLUE)
        label_r = MathTex(r"\mathbf{r}_{OP}", color=BLUE).scale(0.8)

        self.add(axes)
        self.play(Create(r_vec), Write(label_r.next_to(start_pt, UP)))
        self.play(Create(force_vec))
        
        # Cross Product Calculation (Moment)
        self.set_camera_orientation(phi=0, theta=-90*DEGREES) # Transition to 2D view for math
        calc = MathTex(r"\mathbf{M}_O = \mathbf{r} \times \mathbf{F}", color=BLACK).to_corner(UL)
        self.add_fixed_in_frame_mobjects(calc)
        self.play(Write(calc))
        self.wait(2)