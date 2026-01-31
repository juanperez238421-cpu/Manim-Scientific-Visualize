from manim import *
import math
from core.visual_engine import AcademicScene, make_paragraph

class DynamicHouse(AcademicScene):
    def construct(self):
        # 1. Setup and Title
        header = self.transition_section("Parametric Centroid Analysis: Composite Geometry")
        SHIFT_V = LEFT * 2 + DOWN * 1.5

        # 2. Dimension Trackers (Parametric Control)
        body_w = ValueTracker(4.0)
        body_h = ValueTracker(2.0)
        roof_h = ValueTracker(1.5)
        door_w = ValueTracker(1.2)
        door_h = ValueTracker(1.6)
        win_r  = ValueTracker(0.6)
        WIN_REL_Y = 0.6 # Window vertical position factor

        # 3. Helper for Geometric Math
        def get_geom():
            w, h = body_w.get_value(), body_h.get_value()
            rh = roof_h.get_value()
            dw = min(door_w.get_value(), 0.4 * w)   # Constrain door width
            dh = min(door_h.get_value(), 0.8 * h)   # Constrain door height
            r  = min(win_r.get_value(), 0.2 * w)    # Constrain window radius
            
            # Areas
            a_body = w * h
            a_roof = 0.5 * w * rh
            a_door = dw * dh
            a_win  = PI * r**2
            a_total = a_body + a_roof - a_door - a_win
            
            # Local Centroids (Relative to SHIFT_V origin)
            x_cm = (a_body*(w/2) + a_roof*(w/2) - a_door*(w*0.25) - a_win*(w*0.75)) / a_total
            y_cm = (a_body*(h/2) + a_roof*(h + rh/3) - a_door*(dh/2) - a_win*(h*WIN_REL_Y)) / a_total
            
            return w, h, rh, dw, dh, r, x_cm, y_cm

        # 4. Redrawable Geometry
        house_body = always_redraw(lambda: 
            Rectangle(width=get_geom()[0], height=get_geom()[1], color=BLACK)
            .set_fill(BLUE_E, opacity=0.1).move_to(SHIFT_V, DL)
        )
        
        roof = always_redraw(lambda:
            Polygon(
                house_body.get_corner(UL), 
                house_body.get_corner(UR), 
                house_body.get_top() + UP * get_geom()[2],
                color=BLACK
            ).set_fill(GREY_B, opacity=0.3)
        )

        door = always_redraw(lambda:
            Rectangle(width=get_geom()[3], height=get_geom()[4], color=BLACK)
            .set_fill(WHITE, opacity=1).move_to(house_body.get_corner(DL) + RIGHT*0.5, DL)
        )

        window = always_redraw(lambda:
            Circle(radius=get_geom()[5], color=BLACK)
            .set_fill(WHITE, opacity=1).move_to(house_body.get_corner(DR) + LEFT*1.0 + UP*1.2)
        )

        # Centroid Marker
        centroid_dot = always_redraw(lambda: 
            Dot(SHIFT_V + RIGHT*get_geom()[6] + UP*get_geom()[7], color=RED, z_index=5)
        )
        
        centroid_label = always_redraw(lambda:
            MathTex(f"G({get_geom()[6]:.2f}, {get_geom()[7]:.2f})", color=RED)
            .scale(0.6).next_to(centroid_dot, UR, buff=0.1)
        )

        # 5. Animation Sequence
        self.play(Create(house_body), Create(roof))
        self.play(FadeIn(door), FadeIn(window))
        self.play(Create(centroid_dot), Write(centroid_label))
        
        caption = make_paragraph(
            "The red dot represents the Center of Mass (G). Observe how it shifts "
            "as we modify the base width and roof height."
        )
        self.play(FadeIn(caption))
        self.wait()

        # Dynamic parameter change
        self.play(
            body_w.animate.set_value(6.0),
            roof_h.animate.set_value(3.0),
            run_time=4,
            rate_func=linear
        )
        self.wait(2)

        # Dimension Labeling Example
        dim_line = always_redraw(lambda: 
            Line(house_body.get_corner(DL), house_body.get_corner(DR), color=GRAY)
            .shift(DOWN*0.3)
        )
        dim_text = always_redraw(lambda:
            Text(f"w = {body_w.get_value():.1f}m", color=GRAY).scale(0.4).next_to(dim_line, DOWN, buff=0.1)
        )
        
        self.play(Create(dim_line), Write(dim_text))
        self.play(body_w.animate.set_value(4.0), run_time=2)
        self.wait(3)