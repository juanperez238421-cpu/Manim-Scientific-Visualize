from manim import *
import numpy as np
from core.visual_engine import AcademicScene, make_paragraph
from core.physics_tools import make_dimension_line

class CombinedShapesCentroid(AcademicScene):
    def construct(self):
        # 1. Setup and Header
        header = self.transition_section("Centroid of Composite Shapes: Additive & Subtractive")
        origin_point = LEFT * 3 + DOWN * 1.5

        # 2. Value Trackers for Parametric Dimensions
        rect_w = ValueTracker(4.0)
        rect_h = ValueTracker(2.0)
        tri_h  = ValueTracker(1.5)
        circ_r = ValueTracker(0.6)

        # 3. Geometric Logic Helper
        def get_data():
            rw, rh = rect_w.get_value(), rect_h.get_value()
            th = tri_h.get_value()
            cr = circ_r.get_value()
            
            # Position of circle (centered in rectangle for this example)
            cx, cy = rw / 2, rh / 2
            
            # Areas
            a_rect = rw * rh
            a_tri  = 0.5 * rw * th
            a_circ = -PI * (cr ** 2) # Negative because it's a hole
            a_total = a_rect + a_tri + a_circ
            
            # Individual Centroids (local to origin_point)
            x_rect, y_rect = rw / 2, rh / 2
            x_tri,  y_tri  = rw / 2, rh + (th / 3)
            x_circ, y_circ = cx, cy
            
            # Composite Centroid Formula: sum(A*x) / sum(A)
            x_cm = (a_rect * x_rect + a_tri * x_tri + a_circ * x_circ) / a_total
            y_cm = (a_rect * y_rect + a_tri * y_tri + a_circ * y_circ) / a_total
            
            return rw, rh, th, cr, x_cm, y_cm

        # 4. Redrawable Geometry
        rectangle = always_redraw(lambda:
            Rectangle(width=get_data()[0], height=get_data()[1], color=BLACK)
            .set_fill(BLUE_D, opacity=0.2).move_to(origin_point, DL)
        )

        triangle = always_redraw(lambda:
            Polygon(
                rectangle.get_corner(UL),
                rectangle.get_corner(UR),
                rectangle.get_top() + UP * get_data()[2],
                color=BLACK
            ).set_fill(BLUE_B, opacity=0.3)
        )

        hole = always_redraw(lambda:
            Circle(radius=get_data()[3], color=BLACK)
            .set_fill(WHITE, opacity=1).move_to(rectangle.get_center())
        )

        # Centroid Marker
        centroid_marker = always_redraw(lambda:
            Dot(origin_point + RIGHT * get_data()[4] + UP * get_data()[5], color=RED, z_index=10)
        )

        # 5. Formulas and Labels
        formula = always_redraw(lambda:
            MathTex(
                r"\bar{x} = \frac{\sum A_i \bar{x}_i}{\sum A_i} = " + f"{get_data()[4]:.2f}m",
                r"\quad \bar{y} = \frac{\sum A_i \bar{y}_i}{\sum A_i} = " + f"{get_data()[5]:.2f}m",
                color=BLACK
            ).scale(0.6).to_edge(DOWN, buff=1.8)
        )

        # 6. Animation
        self.play(Create(rectangle), Create(triangle))
        self.play(FadeIn(hole))
        self.play(Create(centroid_marker), Write(formula))
        
        caption = make_paragraph(
            "Composite centroid calculation: The triangle adds area, while the circle "
            "acts as a hole (negative area), pulling the center of mass away."
        )
        self.play(FadeIn(caption))
        self.wait()

        # Dynamic dimension change
        self.play(
            rect_w.animate.set_value(2.5),
            tri_h.animate.set_value(3.0),
            circ_r.animate.set_value(0.4),
            run_time=4
        )
        self.wait()

        # Show dimensioning example
        dim_h = always_redraw(lambda:
            make_dimension_line(
                rectangle.get_corner(UR), 
                rectangle.get_corner(DR), 
                f"{rect_h.get_value():.1f}m", 
                offset=RIGHT*0.5
            )
        )
        self.play(Create(dim_h))
        self.play(rect_h.animate.set_value(3.5), run_time=2)
        self.wait(2)