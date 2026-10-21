#!/usr/bin/env python3
"""Version B shaded-areas quiz, Instituto Jorge Robledo, 19 October 2026.
Faithfully presents the two exam statements and dimensions. No solutions.
40 minutes, one ManimCE ValueTracker countdown per problem.
"""
from __future__ import annotations
import os, math
import numpy as np
from manim import *
config.frame_width = 16
config.frame_height = 9
config.background_color = WHITE
INK="#191919"; GREY="#C9C9C9"; MUTED="#555555"; ACC="#19475F"
FONT="DejaVu Sans"; SPEED=float(os.getenv("EXAM_PREVIEW_SCALE","1"))
assert 0 < SPEED <= 1
P = [
 {"stem":"Siete regiones grises forman una única figura, sin superposición.",
  "data":[("A","Cuadrado: lado 6"),("B","Rectángulo: 3 × 4"),
  ("C","Trapecio: bases 3 y 1; altura 3"),
  ("D","Triángulo rectángulo: catetos 4 y 5"),
  ("E","Semicírculo: radio 3"),("F","Rectángulo: 3 × 2"),
  ("G","Triángulo rectángulo: catetos 3 y 3")]},
 {"stem":"El rectángulo gris contiene seis figuras blancas que se han retirado.",
  "data":[("R","Rectángulo exterior: 18 × 10"),("A","Círculo: radio 1,5"),
  ("B","Trapecio: bases 5 y 3; altura 3"),
  ("C","Triángulo rectángulo: catetos 3 y 3"),("D","Cuadrado: lado 3"),
  ("E","Semicírculo: radio 2"),("F","Rombo: diagonales 4 y 3")]}
]
def tx(s,n=22,b=False,c=INK):
 return Text(s,font=FONT,font_size=n,color=c,weight=BOLD if b else NORMAL)
def polygon(pts, shade=GREY):
 return Polygon(*pts,stroke_width=2.2,stroke_color=INK,fill_color=shade,fill_opacity=1)
def frame(w,h,x,y):
 return RoundedRectangle(corner_radius=.11,width=w,height=h,
     stroke_width=1.4,stroke_color="#C1C1C1",fill_color="#FCFCFC",fill_opacity=1).move_to([x,y,0])
def time_string(v):
 s=max(0,min(1200,int(math.ceil(v-1e-8))))
 return f"{s//60:02d}:{s%60:02d}"
class Geometry8ShadedQuizB(Scene):
 def shape1(self):
  # World units are centimeters; parts have no mutual area overlap.
  s=.445; o=np.array([-4.18,-.89,0])
  def v(x,y):return o+np.array([(x-3.5)*s,(y-3.5)*s,0])
  parts=[
    polygon([v(*p) for p in [(0,0),(6,0),(6,6),(0,6)]]),
    polygon([v(*p) for p in [(0,6),(3,6),(3,10),(0,10)]]),
    polygon([v(*p) for p in [(3,6),(6,6),(5,9),(4,9)]]),
    polygon([v(*p) for p in [(6,1),(10,1),(6,6)]]),
    Sector(radius=3*s,start_angle=PI/2,angle=PI,
      arc_center=v(0,3),stroke_width=2.2,stroke_color=INK,fill_color=GREY,fill_opacity=1),
    polygon([v(*p) for p in [(3,-2),(6,-2),(6,0),(3,0)]]),
    polygon([v(*p) for p in [(0,-3),(0,0),(3,0)]])
  ]
  labels=[("A",(3,3)),("B",(1.5,8)),("C",(4.5,7.2)),
          ("D",(7,2.6)),("E",(-1.5,3)),("F",(4.5,-1)),("G",(.85,-.85))]
  return VGroup(*parts,*[tx(l,25,True).move_to(v(*xy)) for l,xy in labels])
 def shape2(self):
  s=.378;o=np.array([-4.1,-.89,0])
  def v(x,y):return o+np.array([(x-9)*s,(y-5)*s,0])
  parts=[polygon([v(*p) for p in [(0,0),(18,0),(18,10),(0,10)]])]
  parts.append(Circle(radius=1.5*s,stroke_color=INK,stroke_width=2.2,
    fill_color=WHITE,fill_opacity=1).move_to(v(3,7.5)))
  for pts in [[(7,6),(12,6),(11,9),(8,9)],[(14,6),(17,6),(17,9)],
              [(2,1),(5,1),(5,4),(2,4)],[(13,2.5),(15,4),(17,2.5),(15,1)]]:
   parts.append(polygon([v(*p) for p in pts],WHITE))
  parts.append(Sector(radius=2*s,start_angle=0,angle=PI,
   arc_center=v(9,2),stroke_width=2.2,stroke_color=INK,fill_color=WHITE,fill_opacity=1))
  labels=[("R",(1,3.5)),("A",(3,7.5)),("B",(9.5,7.3)),
          ("C",(16,7)),("D",(3.5,2.5)),("E",(9,2.8)),("F",(15,2.5))]
  return VGroup(*parts,*[tx(l,24,True).move_to(v(*xy)) for l,xy in labels])
 def content(self,n):
  q=P[n-1]
  left=frame(8.55,5.85,-3.83,-.50)
  right=frame(6.05,5.85,4.45,-.50)
  fig=self.shape1() if n==1 else self.shape2()
  # Geometry area within left panel; on-screen dimensions remain explicit in data.
  title=tx(q["stem"],20).move_to([-2.11,2.54,0])
  heading=tx("DATOS DE LAS REGIONES",24,True,ACC).move_to([4.36,2.15,0])
  units=tx("Todas las medidas se dan en cm.",19,False,MUTED).move_to([4.36,1.77,0])
  rows=VGroup()
  for i,(letter,meaning) in enumerate(q["data"]):
   y=1.16-i*.67
   a=tx(letter,25,True).move_to([1.93,y,0])
   b=tx(meaning,20).move_to([2.37,y,0],aligned_edge=LEFT)
   b.align_to([2.4,y,0],LEFT)
   rows.add(a,b)
  return VGroup(left,right,fig,title,heading,units,rows)
 def header(self,n):
  return VGroup(
   tx("INSTITUTO JORGE ROBLEDO",24,True).move_to([-5.15,4.10,0]),
   tx("GEOMETRÍA 8.º  /  ÁREAS SOMBREADAS  /  VERSIÓN B",24,True).move_to([-2.13,3.53,0]),
   Line([-7.55,3.19,0],[7.55,3.19,0],color="#B7B7B7",stroke_width=2),
   tx(f"PROBLEMA {n} DE 2",26,True,ACC).move_to([-6.02,2.95,0]),
   tx("5 puntos",23,True,MUTED).move_to([-3.85,2.95,0])
  )
 def construct(self):
  opening=VGroup(tx("QUIZ DE ÁREAS SOMBREADAS",48,True),
    tx("GEOMETRÍA 8.º  ·  VERSIÓN B",30,True,ACC),
    tx("20 minutos por problema  ·  2 problemas",24,c=MUTED)).arrange(DOWN,buff=.4)
  self.add(opening);self.wait(max(3*SPEED,1/config.frame_rate));self.remove(opening)
  for n in [1,2]:
   progress=ValueTracker(1200)
   board=self.content(n)
   h=self.header(n)
   box=frame(1.82,.65,6.53,3.76)
   digits=always_redraw(lambda:tx(time_string(progress.get_value()),37,True,ACC).move_to([6.53,3.76,0]))
   foot=tx("Calcula solo el área sombreada  ·  π = 3,14  ·  No deduzcas medidas del dibujo",20,c=MUTED)
   foot.move_to([0,-4.13,0])
   self.add(board,h,box,digits,foot)
   self.play(progress.animate.set_value(0),run_time=1200*SPEED,rate_func=linear)
   self.remove(board,h,box,digits,foot,progress)
  self.add(tx("QUIZ FINALIZADO",45,True));self.wait(max(3*SPEED,1/config.frame_rate))
