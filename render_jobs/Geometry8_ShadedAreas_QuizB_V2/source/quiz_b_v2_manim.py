# -*- coding: utf-8 -*-
"""I.J.R. | Geometría 8 | Quiz de Áreas Sombreadas | SOLO VERSIÓN B (V2).
Material ManimCE vectorial reproducible. La cuenta atrás de 2 x 1200 s se
genera con FFmpeg (1 lectura del contador por segundo, 30 fps de salida).
Este módulo NO revela las respuestas de los alumnos.
ManimCE v0.20.1+:
  G8_PROBLEM=1 manim -s -qh --fps 30 quiz_b_v2_manim.py QuizBCard
  G8_PROBLEM=2 manim -s -qh --fps 30 quiz_b_v2_manim.py QuizBCard
"""
import os
import numpy as np
from manim import *

config.background_color = "#FFFFFF"
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
INK = "#151515"
GRAY = "#D5D5D5"
FONT = "Noto Serif"
ROWS = {
1: [
 ("A","CUADRADO",r"A=l^2","l = 6 cm"),
 ("B","RECTANGULO",r"A=b\,h","b = 3; h = 4 cm"),
 ("C","TRAPECIO",r"A=\frac{(B+b)h}{2}","B = 3; b = 1; h = 3 cm"),
 ("D","TRIANGULO RECT.",r"A=\frac{c_1c_2}{2}","c1 = 4; c2 = 5 cm"),
 ("E","SEMICIRCULO",r"A=\frac{\pi r^2}{2}","r = 3 cm"),
 ("F","RECTANGULO",r"A=b\,h","b = 3; h = 2 cm"),
 ("G","TRIANGULO RECT.",r"A=\frac{c_1c_2}{2}","c1 = 3; c2 = 3 cm"),
],
2: [
 ("R","RECTANGULO EXT.",r"A=b\,h","b = 18; h = 10 cm"),
 ("A","CIRCULO",r"A=\pi r^2","r = 1,5 cm"),
 ("B","TRAPECIO",r"A=\frac{(B+b)h}{2}","B = 5; b = 3; h = 3 cm"),
 ("C","TRIANGULO RECT.",r"A=\frac{c_1c_2}{2}","c1 = 3; c2 = 3 cm"),
 ("D","CUADRADO",r"A=l^2","l = 3 cm"),
 ("E","SEMICIRCULO",r"A=\frac{\pi r^2}{2}","r = 2 cm"),
 ("F","ROMBO",r"A=\frac{Dd}{2}","D = 4; d = 3 cm"),
]
}

def xy(v): return np.array([float(v[0]), float(v[1]), 0.0])
def shape_poly(coords, fill):
    return Polygon(*[xy(p) for p in coords], stroke_width=2.7,
                   stroke_color=INK, fill_color=fill, fill_opacity=1)
def rect(a,b,c,d):
    return [(a,b),(c,b),(c,d),(a,d)]
def circ(x,y,r,fill):
    return Circle(radius=r,stroke_color=INK,stroke_width=2.7,
        fill_color=fill,fill_opacity=1).move_to(xy((x,y)))
def semi(x,y,r,start,fill):
    return Sector(arc_center=xy((x,y)),radius=r,angle=PI,
        start_angle=start,stroke_color=INK,stroke_width=2.7,
        fill_color=fill,fill_opacity=1)

def composite_figure(n):
    """Geometry matches LaTeX/Figura_B1.tex and Figura_B2.tex source."""
    if n == 1:
        parts = [
            shape_poly(rect(0,0,6,6),GRAY),
            shape_poly(rect(0,6,3,10),GRAY),
            shape_poly([(3,6),(6,6),(5,9),(4,9)],GRAY),
            shape_poly([(6,1),(10,1),(6,6)],GRAY),
            semi(0,3,3,PI/2,GRAY),
            shape_poly(rect(3,-2,6,0),GRAY),
            shape_poly([(0,0),(3,0),(0,-3)],GRAY)
        ]
        spots={"A":(3,3),"B":(1.5,8),"C":(4.5,7.15),
          "D":(7.32,2.54),"E":(-1.35,3),"F":(4.5,-1),"G":(.76,-.86)}
    else:
        parts=[
            shape_poly(rect(0,0,18,10),GRAY),
            circ(3,7.5,1.5,WHITE),
            shape_poly([(7,6),(12,6),(11,9),(8,9)],WHITE),
            shape_poly([(14,6),(17,6),(17,9)],WHITE),
            shape_poly(rect(2,1,5,4),WHITE),
            semi(9,2,2,0,WHITE),
            shape_poly([(15,4),(17,2.5),(15,1),(13,2.5)],WHITE)
        ]
        spots={"R":(1,5.15),"A":(3,7.5),"B":(9.5,7.45),
          "C":(16,7.02),"D":(3.5,2.5),"E":(9,2.65),"F":(15,2.5)}
    marks=[]
    for name,pos in spots.items():
        tag=Text(name,font=FONT,font_size=22,color=INK,weight=BOLD).move_to(xy(pos))
        marks.append(VGroup(BackgroundRectangle(tag,color=WHITE,
            fill_opacity=1,buff=.035),tag))
    return VGroup(*parts,*marks)

class QuizBCard(Scene):
    def construct(self):
        n=int(os.getenv("G8_PROBLEM","1"))
        assert n in (1,2)
        h=Text("GEOMETRIA 8 / AREAS SOMBREADAS",font=FONT,
               font_size=36,weight=BOLD,color=INK).move_to((-3.3,3.75,0))
        v=Text("VERSION B / V2",font=FONT,font_size=25,
               weight=BOLD,color=INK).move_to((5.9,3.82,0))
        title=Text("PROBLEMA "+str(n)+"  |  5 PUNTOS",
                   font=FONT,font_size=32,weight=BOLD,color=INK
                   ).move_to((-5.35,2.90,0))
        self.add(h,v,title,Line((-7.5,3.35,0),(7.5,3.35,0),color="#D6D6D6"))
        geo=composite_figure(n)
        geo.scale(.42 if n==1 else .32).move_to((-4.25,-.45,0))
        self.add(geo)
        for i,(letter,kind,formula,data) in enumerate(ROWS[n]):
            y=2.05-i*.72
            self.add(
                Text(letter,font=FONT,font_size=27,weight=BOLD,color=INK
                     ).move_to((.50,y,0)),
                Text(kind,font=FONT,font_size=21,weight=BOLD,color=INK
                     ).move_to((2.45,y+.17,0)),
                MathTex(formula,font_size=26,color=INK).move_to((2.85,y-.17,0)),
                Text(data,font=FONT,font_size=19,color=INK
                     ).move_to((6.13,y-.03,0))
            )
        note = ("A + B + C + D + E + F + G" if n==1
                else "R - (A + B + C + D + E + F)")
        self.add(Text("AREA SOMBREADA = "+note,font=FONT,
                      font_size=23,color=INK).move_to((0,-3.54,0)))
        self.wait(.2)
