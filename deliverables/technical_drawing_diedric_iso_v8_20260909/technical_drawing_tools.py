#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reusable engineering-graphics helpers for ManimCE 0.20.x.

This module centralizes geometry, line weights, orthographic view drawing,
projection symbols, dimensions, and fixed-frame UI primitives for technical-
drawing lessons. It intentionally avoids external assets so renders remain
reproducible in GitHub Actions / Docker.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence
import numpy as np
from manim import *

BG = "#F6F8FB"
PAPER = "#FFFFFF"
NAVY = "#0B1F33"
INK = "#14202B"
DARK = "#334155"
MID = "#64748B"
LIGHT = "#D6DEE8"
GRID = "#E8EDF3"
BLUE = "#1769AA"
CYAN = "#2C9FCC"
TEAL = "#158B80"
ORANGE = "#E88A17"
GREEN = "#2F8F5B"
RED = "#C85050"
PURPLE = "#7357B8"
PALE_BLUE = "#EAF4FB"
PALE_TEAL = "#E8F6F3"
PALE_ORANGE = "#FFF4E7"
FACE_BASE = "#DDE5ED"
FACE_SIDE = "#B8C7D6"
FACE_TOP = "#F9FBFD"
FACE_ACCENT = "#9FB3C6"
VISIBLE_W = 3.0
SECONDARY_W = 2.0
HIDDEN_W = 1.55
CENTER_W = 1.25
PROJECTION_W = 1.65

@dataclass(frozen=True)
class ViewSpec:
    key: str
    label: str
    accent: str

VIEW_SPECS = {
    "front": ViewSpec("front", "ALZADO / FRONT", BLUE),
    "top": ViewSpec("top", "PLANTA / TOP", TEAL),
    "right": ViewSpec("right", "LATERAL DERECHO", ORANGE),
    "left": ViewSpec("left", "LATERAL IZQUIERDO", PURPLE),
    "rear": ViewSpec("rear", "POSTERIOR / REAR", RED),
    "bottom": ViewSpec("bottom", "INFERIOR / BOTTOM", GREEN),
}

def safe_text(content: str, size: int = 28, color: str = INK, weight=NORMAL, max_width: float | None = None) -> Text:
    t = Text(content, font_size=size, color=color, weight=weight, line_spacing=0.92)
    if max_width is not None and t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t

def badge(text: str, color: str = BLUE, size: int = 18, fill: str = PAPER) -> VGroup:
    label = safe_text(text, size=size, color=color, weight=BOLD)
    box = RoundedRectangle(width=label.width + 0.44, height=label.height + 0.22, corner_radius=0.10, stroke_color=color, stroke_width=1.5, fill_color=fill, fill_opacity=1)
    label.move_to(box)
    return VGroup(box, label)

def section_header(number: int, title: str, subtitle: str = "") -> VGroup:
    bar = Rectangle(width=16, height=0.78, stroke_width=0, fill_color=NAVY, fill_opacity=1).to_edge(UP, buff=0)
    nbox = RoundedRectangle(width=0.52, height=0.42, corner_radius=0.08, stroke_color=CYAN, stroke_width=1.6, fill_color=NAVY, fill_opacity=1)
    ntext = safe_text(str(number), 19, CYAN, BOLD).move_to(nbox)
    title_m = safe_text(title, 30, PAPER, BOLD, max_width=12.6)
    row = VGroup(VGroup(nbox, ntext), title_m).arrange(RIGHT, buff=0.20)
    row.to_edge(LEFT, buff=0.42).to_edge(UP, buff=0.14)
    items = [bar, row]
    if subtitle:
        sub = safe_text(subtitle, 18, DARK, NORMAL, max_width=14.7)
        sub.to_edge(LEFT, buff=0.46).next_to(bar, DOWN, buff=0.10)
        items.append(sub)
    return VGroup(*items)

def step_chip(number: int, text: str, color: str = BLUE, width: float = 3.1) -> VGroup:
    box = RoundedRectangle(width=width, height=0.72, corner_radius=0.12, stroke_color=LIGHT, stroke_width=1.3, fill_color=PAPER, fill_opacity=1)
    c = Circle(radius=0.22, stroke_color=color, stroke_width=1.6, fill_color=PALE_BLUE if color == BLUE else PAPER, fill_opacity=1)
    n = safe_text(str(number), 17, color, BOLD).move_to(c)
    txt = safe_text(text, 18, INK, BOLD, max_width=width-0.85)
    row = VGroup(VGroup(c, n), txt).arrange(RIGHT, buff=0.16)
    row.move_to(box)
    return VGroup(box, row)

def callout(text: str, color: str = BLUE, width: float = 4.4, size: int = 21) -> VGroup:
    txt = safe_text(text, size, color, BOLD, max_width=width-0.55)
    box = RoundedRectangle(width=width, height=max(0.8, txt.height+0.34), corner_radius=0.12, stroke_color=color, stroke_width=1.7, fill_color=PAPER, fill_opacity=0.97)
    txt.move_to(box)
    return VGroup(box, txt)

def paper_panel(width: float = 5.0, height: float = 3.4, grid_spacing: float = 0.34) -> VGroup:
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=LIGHT, stroke_width=1.35, fill_color=PAPER, fill_opacity=1)
    lines = VGroup()
    x = -width/2 + grid_spacing
    while x < width/2:
        lines.add(Line([x,-height/2,0],[x,height/2,0], stroke_color=GRID, stroke_width=0.65)); x += grid_spacing
    y = -height/2 + grid_spacing
    while y < height/2:
        lines.add(Line([-width/2,y,0],[width/2,y,0], stroke_color=GRID, stroke_width=0.65)); y += grid_spacing
    return VGroup(frame, lines)

def _set_engineering_style(mob: Mobject, fill: str = FACE_BASE, stroke: str = INK, opacity: float = 1.0) -> Mobject:
    mob.set_fill(fill, opacity=opacity); mob.set_stroke(stroke, width=1.15, opacity=0.85)
    if hasattr(mob, "set_shade_in_3d"): mob.set_shade_in_3d(True)
    return mob

def box3d(width: float, depth: float, height: float, center: Sequence[float], fill: str = FACE_BASE) -> Cube:
    b = Cube(side_length=1.0); b.stretch(width, dim=0); b.stretch(depth, dim=1); b.stretch(height, dim=2); b.move_to(np.array(center, dtype=float))
    return _set_engineering_style(b, fill=fill)

def mechanical_bracket_3d() -> VGroup:
    base = box3d(6.4, 3.6, 0.42, (0, 0, 0.21), FACE_BASE)
    low = box3d(1.25, 1.35, 0.72, (-2.15, -0.35, 0.78), FACE_SIDE)
    mid = box3d(1.75, 2.15, 1.15, (-0.10, 0.15, 1.00), FACE_ACCENT)
    tower = box3d(1.18, 2.45, 3.35, (2.25, 0.10, 1.88), FACE_SIDE)
    rib = box3d(0.52, 2.75, 1.90, (1.35, 0.0, 1.16), FACE_ACCENT)
    boss = Cylinder(radius=0.62, height=0.35, direction=OUT, resolution=(24, 1)); _set_engineering_style(boss, fill=FACE_TOP); boss.move_to(np.array([-2.08, -0.35, 1.31]))
    top_hole = Circle(radius=0.29, stroke_color=TEAL, stroke_width=2.0, fill_color=BG, fill_opacity=1).move_to(np.array([-2.08, -0.35, 1.495]))
    top_center = VGroup(DashedLine([-2.50,-0.35,1.50],[-1.66,-0.35,1.50], dash_length=0.09, stroke_color=MID, stroke_width=1.1), DashedLine([-2.08,-0.77,1.50],[-2.08,0.07,1.50], dash_length=0.09, stroke_color=MID, stroke_width=1.1))
    tower_hole = Circle(radius=0.36, stroke_color=BLUE, stroke_width=2.0, fill_color=BG, fill_opacity=1); tower_hole.rotate(PI/2, axis=RIGHT); tower_hole.move_to(np.array([2.25, -1.135, 2.25]))
    tower_center = VGroup(DashedLine([1.72,-1.145,2.25],[2.78,-1.145,2.25], dash_length=0.10, stroke_color=MID, stroke_width=1.1), DashedLine([2.25,-1.145,1.72],[2.25,-1.145,2.78], dash_length=0.10, stroke_color=MID, stroke_width=1.1))
    return VGroup(base, low, mid, rib, tower, boss, top_hole, top_center, tower_hole, tower_center)

def vertical_projection_plane(y: float = -3.3, width: float = 7.2, height: float = 5.0, z0: float = 2.45, grid_step: float = 0.5) -> VGroup:
    plane = Rectangle(width=width, height=height, stroke_color=CYAN, stroke_width=1.7, fill_color=PALE_BLUE, fill_opacity=0.22); plane.rotate(PI/2, axis=RIGHT); plane.move_to(np.array([0.0, y, z0]))
    grid = VGroup(); xmin, xmax = -width/2, width/2; zmin, zmax = z0-height/2, z0+height/2
    x = xmin + grid_step
    while x < xmax:
        grid.add(Line([x,y,zmin],[x,y,zmax], stroke_color=CYAN, stroke_width=0.55, stroke_opacity=0.28)); x += grid_step
    z = zmin + grid_step
    while z < zmax:
        grid.add(Line([xmin,y,z],[xmax,y,z], stroke_color=CYAN, stroke_width=0.55, stroke_opacity=0.28)); z += grid_step
    return VGroup(plane, grid)

def dihedral_planes(size: float = 7.0) -> tuple[VGroup, VGroup, Line]:
    ph = Rectangle(width=size, height=size*0.68, stroke_color=TEAL, stroke_width=1.6, fill_color=PALE_TEAL, fill_opacity=0.25); ph.move_to(ORIGIN)
    pv = Rectangle(width=size, height=size*0.68, stroke_color=BLUE, stroke_width=1.6, fill_color=PALE_BLUE, fill_opacity=0.24); pv.rotate(PI/2, axis=RIGHT); pv.move_to(ORIGIN)
    lt = Line(LEFT*size/2, RIGHT*size/2, stroke_color=INK, stroke_width=2.6)
    return VGroup(pv), VGroup(ph), lt

def projection_ray(start: Sequence[float], end: Sequence[float], color: str = ORANGE) -> Line:
    return Line(np.array(start,dtype=float), np.array(end,dtype=float), stroke_color=color, stroke_width=PROJECTION_W, stroke_opacity=0.66)

def front_trace_3d(plane_y: float = -3.31, color: str = BLUE) -> VGroup:
    pts = [(-3.2,0.42),(-3.2,0.83),(-2.77,0.83),(-2.77,1.49),(-1.52,1.49),(-1.52,0.42),(-0.98,0.42),(-0.98,1.55),(0.78,1.55),(0.78,0.42),(1.66,0.42),(1.66,3.56),(2.84,3.56),(2.84,0.42),(3.2,0.42)]
    segs = VGroup()
    for a,b in zip(pts[:-1],pts[1:]): segs.add(Line([a[0],plane_y,a[1]],[b[0],plane_y,b[1]], stroke_color=color, stroke_width=3.0))
    segs.add(Line([pts[-1][0],plane_y,pts[-1][1]],[pts[0][0],plane_y,pts[0][1]], stroke_color=color, stroke_width=3.0))
    hole = Circle(radius=0.35, stroke_color=color, stroke_width=2.2, fill_opacity=0); hole.rotate(PI/2, axis=RIGHT).move_to([2.25,plane_y-0.005,2.25])
    return VGroup(segs, hole)

def _polyline(points, color: str = INK, width: float = VISIBLE_W, closed: bool = True) -> VGroup:
    pts = [np.array([x,y,0.0],dtype=float) for x,y in points]; lines = VGroup(); pairs = list(zip(pts[:-1],pts[1:]));
    if closed: pairs.append((pts[-1],pts[0]))
    for a,b in pairs: lines.add(Line(a,b, stroke_color=color, stroke_width=width))
    return lines

def center_mark(center, radius: float = 0.34, color: str = MID) -> VGroup:
    c = np.array([center[0],center[1],0.0]); return VGroup(DashedLine(c+LEFT*(radius+0.18), c+RIGHT*(radius+0.18), dash_length=0.08, stroke_color=color, stroke_width=CENTER_W), DashedLine(c+DOWN*(radius+0.18), c+UP*(radius+0.18), dash_length=0.08, stroke_color=color, stroke_width=CENTER_W))

def dimension_line(a, b, text: str, offset=(0,0,0), color: str = MID, size: int = 15) -> VGroup:
    a=np.array(a,dtype=float); b=np.array(b,dtype=float); off=np.array(offset,dtype=float); aa=a+off; bb=b+off
    line=DoubleArrow(aa,bb,buff=0,tip_length=0.10,stroke_color=color,stroke_width=1.1,max_tip_length_to_length_ratio=0.08); e1=Line(a,aa,stroke_color=color,stroke_width=0.9); e2=Line(b,bb,stroke_color=color,stroke_width=0.9); label=safe_text(text,size,color,BOLD).move_to((aa+bb)/2)
    if abs(bb[0]-aa[0]) >= abs(bb[1]-aa[1]): label.shift(UP*0.16)
    else: label.rotate(PI/2).shift(RIGHT*0.16)
    return VGroup(e1,e2,line,label)

def front_view(scale: float = 0.72, color: str = INK, dimensions: bool = False) -> VGroup:
    pts=[(-3.20,-1.05),(-3.20,-0.62),(-2.75,-0.62),(-2.75,0.05),(-1.50,0.05),(-1.50,-1.05),(-0.95,-1.05),(-0.95,0.10),(0.78,0.10),(0.78,-1.05),(1.65,-1.05),(1.65,2.10),(2.82,2.10),(2.82,-1.05)]
    outline=_polyline([(x*scale,y*scale) for x,y in pts],color); hole_c=np.array([2.24*scale,0.80*scale,0]); hole=Circle(radius=0.34*scale,stroke_color=BLUE,stroke_width=2.3,fill_opacity=0).move_to(hole_c); center=center_mark(hole_c[:2],0.34*scale)
    hidden=VGroup(DashedLine([-2.43*scale,-0.62*scale,0],[-2.43*scale,0.04*scale,0],dash_length=0.08,stroke_color=MID,stroke_width=HIDDEN_W), DashedLine([-1.82*scale,-0.62*scale,0],[-1.82*scale,0.04*scale,0],dash_length=0.08,stroke_color=MID,stroke_width=HIDDEN_W)); g=VGroup(outline,hidden,hole,center)
    if dimensions: g.add(dimension_line([-3.20*scale,-1.05*scale,0],[2.82*scale,-1.05*scale,0],"64",[0,-0.48,0])); g.add(dimension_line([2.82*scale,-1.05*scale,0],[2.82*scale,2.10*scale,0],"34",[0.44,0,0]))
    return g

def top_view(scale: float = 0.72, color: str = INK, dimensions: bool = False) -> VGroup:
    w,h=6.40*scale,3.60*scale; outer=Rectangle(width=w,height=h,stroke_color=color,stroke_width=VISIBLE_W,fill_opacity=0); low=Rectangle(width=1.25*scale,height=1.35*scale,stroke_color=color,stroke_width=SECONDARY_W,fill_opacity=0).move_to([-2.15*scale,-0.35*scale,0]); mid=Rectangle(width=1.75*scale,height=2.15*scale,stroke_color=color,stroke_width=SECONDARY_W,fill_opacity=0).move_to([-0.10*scale,0.15*scale,0]); tower=Rectangle(width=1.18*scale,height=2.45*scale,stroke_color=color,stroke_width=SECONDARY_W,fill_opacity=0).move_to([2.25*scale,0.10*scale,0]); boss=Circle(radius=0.62*scale,stroke_color=TEAL,stroke_width=2.1,fill_opacity=0).move_to([-2.08*scale,-0.35*scale,0]); bore=Circle(radius=0.29*scale,stroke_color=TEAL,stroke_width=2.1,fill_opacity=0).move_to(boss); center=center_mark(bore.get_center()[:2],0.29*scale); hidden=VGroup(DashedLine([1.90*scale,-1.13*scale,0],[1.90*scale,1.33*scale,0],dash_length=0.08,stroke_color=MID,stroke_width=HIDDEN_W), DashedLine([2.60*scale,-1.13*scale,0],[2.60*scale,1.33*scale,0],dash_length=0.08,stroke_color=MID,stroke_width=HIDDEN_W)); g=VGroup(outer,low,mid,tower,boss,bore,center,hidden)
    if dimensions: g.add(dimension_line([-3.2*scale,-1.8*scale,0],[3.2*scale,-1.8*scale,0],"64",[0,-0.42,0])); g.add(dimension_line([-3.2*scale,-1.8*scale,0],[-3.2*scale,1.8*scale,0],"36",[-0.42,0,0]))
    return g

def side_view(scale: float = 0.72, color: str = INK, mirror: bool = False, dimensions: bool = False) -> VGroup:
    pts=[(-1.80,-1.05),(-1.80,-0.62),(-1.23,-0.62),(-1.23,0.05),(-0.95,0.05),(-0.95,2.10),(0.95,2.10),(0.95,0.05),(1.22,0.05),(1.22,-0.62),(1.80,-0.62),(1.80,-1.05)];
    if mirror: pts=[(-x,y) for x,y in pts]
    outline=_polyline([(x*scale,y*scale) for x,y in pts],color); hidden=VGroup(DashedLine([-0.35*scale,0.20*scale,0],[-0.35*scale,1.40*scale,0],dash_length=0.08,stroke_color=MID,stroke_width=HIDDEN_W), DashedLine([0.35*scale,0.20*scale,0],[0.35*scale,1.40*scale,0],dash_length=0.08,stroke_color=MID,stroke_width=HIDDEN_W));
    if mirror: hidden.flip(axis=UP)
    g=VGroup(outline,hidden)
    if dimensions: g.add(dimension_line([-1.8*scale,-1.05*scale,0],[1.8*scale,-1.05*scale,0],"36",[0,-0.45,0]))
    return g

def rear_view(scale: float = 0.72, color: str = INK) -> VGroup:
    g=front_view(scale,color,False).copy(); g.flip(axis=UP); return g

def bottom_view(scale: float = 0.72, color: str = INK) -> VGroup:
    g=top_view(scale,color,False).copy(); g.flip(axis=RIGHT); return g

def orthographic_view(key: str, scale: float = 0.72, dimensions: bool = False) -> VGroup:
    if key == "front": return front_view(scale, INK, dimensions)
    if key == "top": return top_view(scale, INK, dimensions)
    if key == "right": return side_view(scale, INK, False, dimensions)
    if key == "left": return side_view(scale, INK, True, dimensions)
    if key == "rear": return rear_view(scale, INK)
    if key == "bottom": return bottom_view(scale, INK)
    raise ValueError(key)

def view_card(key: str, width: float = 4.3, height: float = 2.72, scale: float = 0.56, dimensions: bool = False) -> VGroup:
    spec=VIEW_SPECS[key]; panel=RoundedRectangle(width=width,height=height,corner_radius=0.12,stroke_color=LIGHT,stroke_width=1.25,fill_color=PAPER,fill_opacity=1); accent=Line(panel.get_corner(UL)+RIGHT*0.18,panel.get_corner(UR)+LEFT*0.18,stroke_color=spec.accent,stroke_width=4); title=safe_text(spec.label,18,spec.accent,BOLD,max_width=width-0.5).next_to(panel.get_top(),DOWN,buff=0.18); view=orthographic_view(key,scale,dimensions)
    if view.width > width-0.42: view.scale_to_fit_width(width-0.42)
    if view.height > height-0.76: view.scale_to_fit_height(height-0.76)
    view.move_to(panel).shift(DOWN*0.13); return VGroup(panel,accent,title,view)

def projection_symbol(first_angle: bool = True, scale: float = 1.0, show_axes: bool = True) -> VGroup:
    frustum = Polygon([-1.15,-0.70,0],[1.15,-0.42,0],[1.15,0.42,0],[-1.15,0.70,0],stroke_color=INK,stroke_width=2.4,fill_opacity=0); frustum.scale(scale); circle=Circle(radius=0.62*scale,stroke_color=INK,stroke_width=2.4,fill_opacity=0); circle.next_to(frustum, LEFT if first_angle else RIGHT, buff=0.48*scale); lines=VGroup()
    if show_axes:
        fc=frustum.get_center(); cc=circle.get_center(); lines.add(DashedLine(fc+LEFT*1.45*scale,fc+RIGHT*1.45*scale,dash_length=0.10*scale,stroke_color=MID,stroke_width=1.0)); lines.add(DashedLine(cc+LEFT*0.82*scale,cc+RIGHT*0.82*scale,dash_length=0.10*scale,stroke_color=MID,stroke_width=1.0)); lines.add(DashedLine(cc+DOWN*0.82*scale,cc+UP*0.82*scale,dash_length=0.10*scale,stroke_color=MID,stroke_width=1.0))
    return VGroup(frustum,circle,lines)

def observer_icon(color: str = BLUE, scale: float = 1.0) -> VGroup:
    eye=Ellipse(width=1.05,height=0.55,stroke_color=color,stroke_width=2.0,fill_color=PAPER,fill_opacity=1); pupil=Circle(radius=0.12,stroke_color=color,stroke_width=1.6,fill_color=color,fill_opacity=1).move_to(eye); glint=Circle(radius=0.035,stroke_width=0,fill_color=PAPER,fill_opacity=1).move_to(pupil.get_center()+UL*0.045); return VGroup(eye,pupil,glint).scale(scale)
