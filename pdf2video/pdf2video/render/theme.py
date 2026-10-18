"""HYBRID-SCIANIM-v1 design tokens and text helpers (ManimCE, 1920x1080, frame 14.22 x 8)."""
from __future__ import annotations

import os

from manim import BOLD, ITALIC, NORMAL, MathTex, Tex, Text, TexTemplate

BG, INK, MUTED, RULE, FILL, STROKE = "#FFFFFF", "#151515", "#6E6E6E", "#D6D6D6", "#F3F3F3", "#3C3C3C"
C_ACC, C_VEL, C_POS, C_GAL = "#B03A2E", "#B7791F", "#2C6E9B", "#2F7D5B"
HILITE = "#F6E7B0"  # data highlight fill (amber, low opacity)
COLORS = {"ink": INK, "muted": MUTED, "acc": C_ACC, "vel": C_VEL, "pos": C_POS, "gal": C_GAL}
SERIF = "Noto Serif"

# frame safe area (margins >= 0.35)
FW, FH = 14.222, 8.0
XL, XR, YT, YB = -6.75, 6.75, 3.65, -3.65

TS = float(os.getenv("P2V_TIME_SCALE", "1.0"))
P_BEAT, P_SHORT, P_MED, P_LONG, P_READ = 0.8, 1.5, 2.5, 4.0, 6.0

TEMPLATE = TexTemplate()
TEMPLATE.add_to_preamble(r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{mathpazo}")


def color(name, default=INK):
    if not name:
        return default
    return COLORS.get(name, name if str(name).startswith("#") else default)


def T(s, size=24, col=INK, weight=NORMAL, slant=NORMAL):
    """Text built at 2x and scaled 0.5 (crisper outlines)"""
    return Text(str(s), font=SERIF, font_size=size * 2, color=col, weight=weight, slant=slant).scale(0.5)


def M(tex, size=34, col=INK, **kw):
    return MathTex(tex, font_size=size, color=col, tex_template=TEMPLATE, **kw)


def TX(tex, size=28, col=INK, **kw):
    return Tex(tex, font_size=size, color=col, tex_template=TEMPLATE, **kw)


def fit(m, w=None, h=None):
    if w is not None and m.width > w:
        m.scale_to_fit_width(w)
    if h is not None and m.height > h:
        m.scale_to_fit_height(h)
    return m


def read_time(text, base=1.6, per_word=0.28, cap=P_READ):
    return min(cap, max(base, per_word * len(str(text).split())))


__all__ = [n for n in dir() if not n.startswith("_")] + ["BOLD", "ITALIC", "NORMAL"]
