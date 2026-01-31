from manim import *
from core.visual_engine import AcademicScene, make_paragraph
from core.physics_tools import create_piv_streamlines
try:
    from manim_slides import Slide
except ImportError:
    from manim import Scene as Slide

class GWVTPresentation(Slide, AcademicScene):
    def construct(self):
        # 1. Title Slide
        title = Text("Gravitational Vortex Turbine (GWVT):\nExperimental Validation", 
                     color=BLACK, weight=BOLD).scale(0.8)
        author = Text("Juan Pérez, M.Sc.", color=GRAY).scale(0.4).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(author))
        self.next_slide() 

        # 2. Methodology Section
        self.play(FadeOut(title), FadeOut(author))
        header = self.transition_section("Methodology: PIV Analysis")
        
        bullets = BulletedList(
            "Non-intrusive flow measurement",
            "Particle Image Velocimetry (PIV) integration",
            "Vector field mapping from .npy datasets",
            color=BLACK
        ).scale(0.7).next_to(header, DOWN, buff=1)
        
        self.play(FadeIn(bullets))
        self.next_slide()

        # 3. Live Data Visualization
        self.play(FadeOut(bullets))
        caption = make_paragraph("Real-time streamline generation from experimental PIV data.")
        
        # Load your actual data
        flow_field = create_piv_streamlines("assets/piv_data/vortex_field.npy")
        
        self.play(FadeIn(flow_field), FadeIn(caption))
        self.play(flow_field.animating_updater)
        self.wait(5)
        self.next_slide()