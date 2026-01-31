from manim import *
import numpy as np
from core.visual_engine import AcademicScene, make_badge
from core.physics_tools import create_piv_streamlines

class PIVValidationScene(AcademicScene):
    def construct(self):
        # UI Elements
        title = Text("Vector Field Reconstruction", color=BLACK).to_edge(UP)
        data_badge = make_badge("Dataset: GWVT_Vortex_01.npy", color=BLUE).next_to(title, DOWN)
        
        self.add(title, data_badge)

        # Scientific Visualization
        # We call the core physics tool that handles the NumPy mapping
        streamlines = create_piv_streamlines(
            "assets/piv_data/vortex_field.npy", 
            density=3.0, 
            stroke_width=3
        )

        description = Paragraph(
            "Visualizing the tangential velocity components",
            "within the gravitational vortex core.",
            color=BLACK
        ).scale(0.5).to_edge(LEFT, buff=0.5)

        self.play(
            LaggedStart(
                Write(description),
                Create(streamlines),
                lag_ratio=0.5
            )
        )
        self.wait(10)