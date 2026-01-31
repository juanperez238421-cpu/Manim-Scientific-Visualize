from manim import *
import textwrap

# =================================================================
# GLOBAL THEME CONFIGURATION
# =================================================================
THEME = {
    "bg_color": "#ffffff",
    "text_color": "#000000",
    "accent_blue": "#2979ff",
    "accent_orange": "#ff9100",
    "accent_red": "#ff5252",
    "accent_green": "#4caf50",
    "code_bg": "#f7f7f7",
    "window_border": "#dddddd"
}

# =================================================================
# ACADEMIC TEXT COMPONENTS
# =================================================================

def make_paragraph(text, width=12.0, font_size=24):
    """
    Creates a safe, wrapped paragraph of text optimized for 
    the bottom narration band of the screen.
    """
    wrapped = textwrap.fill(text, width=85)
    para = Paragraph(
        *wrapped.split("\n"), 
        line_spacing=0.5, 
        color=THEME["text_color"],
        font_size=font_size
    )
    if para.width > width:
        para.scale_to_fit_width(width)
    return para.to_edge(DOWN, buff=0.5)

def make_badge(text, color=THEME["accent_blue"]):
    """
    Creates a technical badge (e.g., for O(n) notation or 
    status indicators) with a rounded background.
    """
    lbl = Text(text, color=WHITE, weight=BOLD).scale(0.35)
    bg = RoundedRectangle(
        corner_radius=0.1, 
        width=lbl.width + 0.3, 
        height=0.45, 
        fill_color=color, 
        fill_opacity=1, 
        stroke_width=0
    )
    return VGroup(bg, lbl)

# =================================================================
# CODE & TERMINAL VISUALIZERS
# =================================================================

def make_code_window(code_str, language="cpp", title="Source Code"):
    """
    Returns a stylized code block with a 'window' background 
    and line highlighting capabilities.
    """
    code_block = Code(
        code_string=code_str.strip(),
        language=language,
        background="window",
        background_config={
            "stroke_color": THEME["window_border"],
            "stroke_width": 1,
        },
        font_size=20,
        tab_width=4,
        line_spacing=0.6,
    )
    return code_block

def make_console_box(lines, width=6.0):
    """
    Simulates a CLI / Terminal output box with prompt indicators.
    """
    console_text = VGroup(*[
        Text(f"> {line}", font="Monospace", color="#d1d1d1").scale(0.4) 
        for line in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    
    bg = Rectangle(
        width=width, 
        height=console_text.height + 0.5, 
        fill_color="#1e1e1e", 
        fill_opacity=1, 
        stroke_color=THEME["window_border"]
    )
    console_text.move_to(bg.get_center())
    return VGroup(bg, console_text)

# =================================================================
# BASE SCENE CLASS (PRE-CONFIGURED)
# =================================================================

class AcademicScene(MovingCameraScene):
    """
    A base class for all engineering and CS scenes that 
    automatically sets the white background and camera defaults.
    """
    def setup(self):
        self.camera.background_color = THEME["bg_color"]
        # Add a subtle footer if needed
        self.footer = Text("Scientific Visualization Suite", color=GRAY).scale(0.2).to_corner(DR)
        self.add(self.footer)

    def transition_section(self, title_text):
        """Standard animation for section headers."""
        title = Text(title_text, color=THEME["text_color"], weight=BOLD).scale(0.7).to_edge(UP)
        self.play(Write(title))
        self.wait()
        return title