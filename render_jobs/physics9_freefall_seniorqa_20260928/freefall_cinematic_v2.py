#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHYSICS 9 — FREE FALL / WEIGHT / APPARENT WEIGHT / WEIGHTLESSNESS
CINEMATIC SENIOR QA V2
ManimCE 0.20.x | 1920x1080 | 30 fps

Design goals:
- phenomenon first, equations after visual evidence
- motion remains visible while vectors/graphs explain it
- explicit distinction W = mg vs apparent weight N
- vacuum vs air
- free-fall cabin and orbital microgravity
- synchronized y(t), v(t), a(t)
"""

from __future__ import annotations
import math, os
import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = "#07111F"

G = 9.81
H = 20.0
T_HIT = math.sqrt(2*H/G)
V_HIT = G*T_HIT
M = 60.0
A_E = 3.0
N_UP = M*(G+A_E)
N_DOWN = M*(G-A_E)
R_E = 6371.0
H_ORBIT = 400.0
G_ORBIT = G*(R_E/(R_E+H_ORBIT))**2
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE","1.0"))

BG = "#07111F"
FG = "#F4F7FB"
MUTED = "#95A4B8"
CYAN = "#35D0FF"
BLUE = "#5B8CFF"
YELLOW = "#FFD166"
RED = "#FF6B6B"
GREEN = "#62E6A7"
PANEL = "#0F1D2D"
GRID = "#24384E"
PURPLE = "#B891FF"


def verify():
    assert abs(0.5*G*T_HIT*T_HIT-H) < 1e-10
    assert abs(V_HIT-math.sqrt(2*G*H)) < 1e-10
    assert abs(N_UP-768.6) < 1e-8
    assert abs(N_DOWN-408.6) < 1e-8
    assert 0.88 < G_ORBIT/G < 0.89


class Physics9FreeFallCinematicV2(MovingCameraScene):
    def setup(self):
        verify()
        super().setup()
        self.camera.background_color = BG
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def play(self,*animations,**kwargs):
        kwargs["run_time"] = kwargs.get("run_time",1.0)*TIME_SCALE
        return super().play(*animations,**kwargs)

    def wait(self,duration=1.0,*args,**kwargs):
        return super().wait(duration*TIME_SCALE,*args,**kwargs)

    # ---------- typography / helpers ----------
    def txt(self,s,size=30,weight=NORMAL,color=FG):
        return Text(s,font_size=size,weight=weight,color=color,line_spacing=0.9)

    def eq(self,s,size=40,color=FG):
        return MathTex(s,font_size=size,color=color)

    def fit(self,m,w=14.5,h=7.3):
        if m.width>w: m.scale_to_fit_width(w)
        if m.height>h: m.scale_to_fit_height(h)
        return m

    def section(self,n,title,subtitle):
        num = self.txt(f"{n:02d}",22,BOLD,CYAN)
        ttl = self.txt(title,31,BOLD,FG)
        sub = self.txt(subtitle,20,NORMAL,MUTED)
        self.fit(sub,13.3,0.55)
        top = VGroup(num,ttl).arrange(RIGHT,buff=0.25)
        grp = VGroup(top,sub).arrange(DOWN,aligned_edge=LEFT,buff=0.10)
        grp.to_corner(UL,buff=0.42)
        rule = Line(LEFT*7.55,RIGHT*7.55,color=GRID,stroke_width=1.4).next_to(grp,DOWN,buff=0.13)
        self.add(grp,rule)
        return VGroup(grp,rule)

    def wipe(self):
        mobs=list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m,shift=DOWN*0.05) for m in mobs],run_time=0.45)

    def card(self,title,body,width=5.8,accent=CYAN):
        box = RoundedRectangle(width=width,height=1.55,corner_radius=0.14,
                               stroke_color=accent,stroke_width=1.8,
                               fill_color=PANEL,fill_opacity=0.95)
        ttl = self.txt(title,23,BOLD,accent)
        bd = self.txt(body,19,NORMAL,FG)
        self.fit(bd,width-0.55,0.55)
        g = VGroup(ttl,bd).arrange(DOWN,aligned_edge=LEFT,buff=0.12)
        g.move_to(box).align_to(box,LEFT).shift(RIGHT*0.30)
        return VGroup(box,g)

    def force(self,start,vec,label,color,side=RIGHT):
        arr=Arrow(start,start+vec,buff=0,color=color,stroke_width=5,
                  max_tip_length_to_length_ratio=0.19)
        lab=self.eq(label,25,color).next_to(arr,side,buff=0.09)
        return VGroup(arr,lab)

    def person(self,c,scale=1.0,color=FG):
        head=Circle(radius=0.18*scale,stroke_color=color,stroke_width=2.4).move_to(c+UP*0.68*scale)
        torso=Line(c+UP*0.48*scale,c+DOWN*0.20*scale,color=color,stroke_width=3.4)
        arms=VGroup(
            Line(c+UP*0.23*scale,c+LEFT*0.35*scale+UP*0.02*scale,color=color,stroke_width=2.8),
            Line(c+UP*0.23*scale,c+RIGHT*0.35*scale+UP*0.02*scale,color=color,stroke_width=2.8))
        legs=VGroup(
            Line(c+DOWN*0.20*scale,c+LEFT*0.24*scale+DOWN*0.70*scale,color=color,stroke_width=2.8),
            Line(c+DOWN*0.20*scale,c+RIGHT*0.24*scale+DOWN*0.70*scale,color=color,stroke_width=2.8))
        return VGroup(head,torso,arms,legs)

    def formula_chip(self,tex,color=CYAN,width=5.0):
        box=RoundedRectangle(width=width,height=0.82,corner_radius=0.12,
                             stroke_color=color,stroke_width=1.5,
                             fill_color=PANEL,fill_opacity=0.92)
        e=self.eq(tex,32,color)
        self.fit(e,width-0.4,0.58)
        e.move_to(box)
        return VGroup(box,e)

    def construct(self):
        self.hook()
        self.what_is_freefall()
        self.upward_throw()
        self.mass_and_air()
        self.apparent_weight()
        self.weightless_cabin()
        self.derive()
        self.twenty_meter_lab()
        self.synced_graphs()
        self.orbit()
        self.qa_final()

    # ---------- 0 hook ----------
    def hook(self):
        title=self.txt("¿CUÁNTO PESAS CUANDO CAES?",52,BOLD,FG)
        title.to_edge(UP,buff=0.60)
        sub=self.txt("La respuesta depende de qué llamemos “peso”.",26,NORMAL,MUTED).next_to(title,DOWN,buff=0.18)

        cabin=RoundedRectangle(width=5.0,height=5.2,corner_radius=0.14,
                               stroke_color=BLUE,stroke_width=2.5,
                               fill_color=PANEL,fill_opacity=0.72).move_to(LEFT*2.0+DOWN*0.25)
        floor=Line(cabin.get_corner(DL)+RIGHT*0.35,cabin.get_corner(DR)+LEFT*0.35,color=BLUE,stroke_width=3)
        p=self.person(cabin.get_center()+DOWN*0.55,1.05)
        scale=RoundedRectangle(width=1.45,height=0.22,corner_radius=0.04,stroke_color=YELLOW,stroke_width=2,
                               fill_color="#17283B",fill_opacity=1).next_to(p,DOWN,buff=0.06)
        read=self.eq(r"N=0",30,YELLOW).next_to(scale,DOWN,buff=0.08)

        apple=Circle(radius=0.16,stroke_color=GREEN,stroke_width=2,fill_color=GREEN,fill_opacity=0.25)
        apple.move_to(cabin.get_center()+RIGHT*1.45+UP*1.0)
        g1=self.force(cabin.get_center()+RIGHT*2.9+UP*1.45,DOWN*1.45,r"\vec g",RED)
        label=self.card("INGRAVIDEZ APARENTE","La gravedad sigue actuando. Lo que desaparece es el apoyo.",5.8,YELLOW)
        label.move_to(RIGHT*4.55+DOWN*0.2)

        self.play(FadeIn(title,shift=UP*0.15),FadeIn(sub))
        self.play(Create(cabin),Create(floor),FadeIn(p),FadeIn(scale),FadeIn(read))
        self.play(FadeIn(apple),GrowArrow(g1[0]),FadeIn(g1[1]))
        self.play(p.animate.shift(UP*0.45),apple.animate.shift(DOWN*0.55),scale.animate.shift(DOWN*0.12),run_time=1.8,rate_func=there_and_back)
        self.play(FadeIn(label))
        self.wait(2.6)
        self.wipe()

    # ---------- 1 ----------
    def what_is_freefall(self):
        self.section(1,"CAÍDA LIBRE = UNA CONDICIÓN DE FUERZAS",
                     "No significa “moverse hacia abajo”. Significa: después de soltar el objeto, solo la gravedad domina.")

        left=LEFT*3.5+DOWN*0.25
        ball=Circle(radius=0.26,stroke_color=FG,stroke_width=2.4,fill_color=BLUE,fill_opacity=0.25).move_to(left+UP*1.35)
        w=self.force(ball.get_center()+RIGHT*0.55,DOWN*1.45,r"\vec W=m\vec g",RED)
        acc=self.force(ball.get_center()+LEFT*0.55,DOWN*1.25,r"\vec a=\vec g",CYAN,LEFT)
        fbd=self.txt("DIAGRAMA DE CUERPO LIBRE",20,BOLD,MUTED).next_to(ball,UP,buff=0.55)
        self.play(FadeIn(ball),FadeIn(fbd))
        self.play(GrowArrow(w[0]),FadeIn(w[1]))
        self.play(GrowArrow(acc[0]),FadeIn(acc[1]))

        chips=VGroup(
            self.formula_chip(r"\sum \vec F = m\vec a",CYAN,5.2),
            self.formula_chip(r"m\vec g = m\vec a",YELLOW,5.2),
            self.formula_chip(r"\boxed{\vec a=\vec g}",GREEN,5.2)
        ).arrange(DOWN,buff=0.28).move_to(RIGHT*3.8+UP*0.45)
        for ch in chips:
            self.play(FadeIn(ch,shift=LEFT*0.12),run_time=0.55)
            self.wait(0.55)

        noN=self.card("NO HAY NORMAL","No existe una superficie sosteniendo el objeto.",5.4,RED).move_to(RIGHT*3.8+DOWN*2.10)
        self.play(FadeIn(noN))
        self.wait(2.4)
        self.wipe()

    # ---------- 2 ----------
    def upward_throw(self):
        self.section(2,"UNA PELOTA QUE SUBE TAMBIÉN ESTÁ EN CAÍDA LIBRE",
                     "Tras abandonar la mano, la aceleración apunta hacia abajo durante toda la trayectoria.")

        x=-3.55
        y0=-2.1
        ytop=2.05
        path=DashedLine([x,y0,0],[x,ytop,0],dash_length=0.09,color=GRID)
        ball=Dot([x,y0,0],radius=0.18,color=YELLOW)
        self.play(Create(path),FadeIn(ball))

        tracker=ValueTracker(0)
        v0=12.0
        ttop=v0/G
        ttotal=2*ttop
        scale_y=(ytop-y0)/(v0*ttop-0.5*G*ttop**2)
        ball.add_updater(lambda b: b.move_to([x,y0+scale_y*(v0*tracker.get_value()-0.5*G*tracker.get_value()**2),0]))

        v_arrow=always_redraw(lambda:
            Arrow(ball.get_center()+LEFT*0.45,
                  ball.get_center()+LEFT*0.45+UP*(np.clip((v0-G*tracker.get_value())/v0,-1,1)*1.55),
                  buff=0,color=GREEN,stroke_width=5,
                  max_tip_length_to_length_ratio=0.18)
            if abs(v0-G*tracker.get_value())>0.15 else Dot(ball.get_center()+LEFT*0.45,radius=0.04,color=GREEN))
        a_arrow=always_redraw(lambda:
            Arrow(ball.get_center()+RIGHT*0.48,ball.get_center()+RIGHT*0.48+DOWN*1.25,buff=0,color=RED,stroke_width=5,
                  max_tip_length_to_length_ratio=0.18))
        vlab=self.eq(r"\vec v",25,GREEN).move_to(LEFT*5.0+UP*2.35)
        alab=self.eq(r"\vec a=-g\hat y",25,RED).next_to(vlab,DOWN,buff=0.15)
        self.add(v_arrow,a_arrow)
        self.play(FadeIn(vlab),FadeIn(alab))

        status=self.txt("SUBE: v > 0, a < 0",25,BOLD,GREEN).move_to(RIGHT*3.5+UP*1.5)
        self.play(FadeIn(status))
        self.play(tracker.animate.set_value(ttop),run_time=2.5,rate_func=linear)
        topnote=self.card("PUNTO MÁS ALTO","v = 0 solo en ese instante. La aceleración sigue siendo −g.",6.1,YELLOW).move_to(RIGHT*3.45+DOWN*0.15)
        self.play(Transform(status,self.txt("CIMA: v = 0, a = −g",25,BOLD,YELLOW).move_to(status)),FadeIn(topnote))
        self.wait(1.7)
        self.play(FadeOut(topnote))
        self.play(Transform(status,self.txt("BAJA: v < 0, a < 0",25,BOLD,RED).move_to(status)))
        self.play(tracker.animate.set_value(ttotal),run_time=2.5,rate_func=linear)
        ball.clear_updaters()
        self.wait(1.8)
        self.wipe()

    # ---------- 3 ----------
    def mass_and_air(self):
        self.section(3,"¿MÁS PESADO = CAE MÁS RÁPIDO?",
                     "En vacío, no. En aire, las diferencias de forma y arrastre sí importan.")

        # vacuum chamber
        vac=RoundedRectangle(width=6.3,height=4.9,corner_radius=0.18,stroke_color=CYAN,stroke_width=2,
                             fill_color=PANEL,fill_opacity=0.55).move_to(LEFT*3.6+DOWN*0.30)
        air=RoundedRectangle(width=6.3,height=4.9,corner_radius=0.18,stroke_color=YELLOW,stroke_width=2,
                             fill_color=PANEL,fill_opacity=0.55).move_to(RIGHT*3.6+DOWN*0.30)
        tv=self.txt("VACÍO",23,BOLD,CYAN).next_to(vac.get_top(),DOWN,buff=0.20)
        ta=self.txt("AIRE",23,BOLD,YELLOW).next_to(air.get_top(),DOWN,buff=0.20)
        self.play(Create(vac),Create(air),FadeIn(tv),FadeIn(ta))

        def feather(center):
            shaft=Line(center+DOWN*0.35,center+UP*0.35,color=FG,stroke_width=2)
            vanes=VGroup(*[
                Line(center+UP*(0.27-i*0.09),center+UP*(0.18-i*0.09)+RIGHT*0.22,color=FG,stroke_width=1.4)
                for i in range(6)])
            vanes2=vanes.copy().flip(LEFT).move_to(vanes)
            return VGroup(shaft,vanes,vanes2)

        bv=Dot(vac.get_center()+LEFT*1.25+UP*1.3,radius=0.18,color=BLUE)
        fv=feather(vac.get_center()+RIGHT*1.15+UP*1.3)
        ba=Dot(air.get_center()+LEFT*1.25+UP*1.3,radius=0.18,color=BLUE)
        fa=feather(air.get_center()+RIGHT*1.15+UP*1.3)
        self.play(FadeIn(bv),FadeIn(fv),FadeIn(ba),FadeIn(fa))
        bottom_v=vac.get_bottom()[1]+0.55
        bottom_a=air.get_bottom()[1]+0.55
        self.play(
            bv.animate.set_y(bottom_v),fv.animate.set_y(bottom_v),
            ba.animate.set_y(bottom_a),fa.animate.set_y(air.get_center()[1]-0.10),
            run_time=2.5,rate_func=rate_functions.ease_in_quad
        )
        same=self.txt("MISMO g",22,BOLD,GREEN).next_to(vac,DOWN,buff=0.16)
        drag=self.txt("EL ARRASTRE CAMBIA EL MOVIMIENTO",20,BOLD,YELLOW).next_to(air,DOWN,buff=0.16)
        self.play(FadeIn(same),FadeIn(drag))
        eqc=self.formula_chip(r"a=\frac{mg}{m}=g",GREEN,4.4).move_to(LEFT*3.6+DOWN*2.95)
        self.play(FadeIn(eqc))
        self.wait(2.5)
        self.wipe()

    # ---------- 4 ----------
    def apparent_weight(self):
        self.section(4,"PESO REAL Y PESO APARENTE NO SON LO MISMO",
                     "W = mg es la fuerza gravitatoria. La báscula mide la fuerza normal N.")

        p=self.person(LEFT*4.6+DOWN*0.3,1.15)
        floor=Line(LEFT*6.2+DOWN*1.55,LEFT*3.0+DOWN*1.55,color=FG,stroke_width=3)
        scale=RoundedRectangle(width=1.5,height=0.22,corner_radius=0.04,stroke_color=YELLOW,stroke_width=2,
                               fill_color=PANEL,fill_opacity=1).move_to(LEFT*4.6+DOWN*1.42)
        Wf=self.force(LEFT*3.95+UP*0.25,DOWN*1.45,r"W=mg",RED)
        Nf=self.force(LEFT*5.25+DOWN*0.95,UP*1.45,r"N",CYAN,LEFT)
        self.play(FadeIn(p),Create(floor),FadeIn(scale))
        self.play(FadeIn(Wf),FadeIn(Nf))

        facts=VGroup(
            self.card("PESO REAL",r"W = mg. Depende de m y del campo gravitatorio.",5.8,RED),
            self.card("PESO APARENTE",r"Es la lectura del soporte: N.",5.8,CYAN),
            self.card("SEGUNDA LEY",r"N - mg = ma_y.",5.8,GREEN)
        ).arrange(DOWN,buff=0.22).move_to(RIGHT*3.65+DOWN*0.1)
        for c in facts:
            self.play(FadeIn(c,shift=LEFT*0.10),run_time=0.5)
            self.wait(0.5)
        self.wait(2.0)
        self.wipe()

    # ---------- 5 ----------
    def weightless_cabin(self):
        self.section(5,"ASCENSOR: CÓMO APARECE LA INGRAVIDEZ",
                     "El mismo cuerpo puede tener el mismo W pero una lectura N distinta según la aceleración del soporte.")

        centers=[-4.8,0,4.8]
        titles=["SUBE ACELERANDO","BAJA ACELERANDO","CAÍDA LIBRE"]
        accs=[r"a_y=+3.0",r"a_y=-3.0",r"a_y=-g"]
        Ns=[N_UP,N_DOWN,0]
        accents=[GREEN,YELLOW,RED]

        groups=[]
        for x,title,a,n,accent in zip(centers,titles,accs,Ns,accents):
            box=RoundedRectangle(width=4.1,height=4.9,corner_radius=0.15,stroke_color=accent,stroke_width=2,
                                 fill_color=PANEL,fill_opacity=0.58).move_to([x,-0.2,0])
            tt=self.txt(title,20,BOLD,accent).next_to(box.get_top(),DOWN,buff=0.20)
            av=self.eq(a+r"\,\mathrm{m/s^2}" if title!="CAÍDA LIBRE" else a,26,FG).next_to(tt,DOWN,buff=0.11)
            py=box.get_bottom()[1]+1.45
            person=self.person(np.array([x,py,0]),0.9)
            scale=RoundedRectangle(width=1.22,height=0.18,corner_radius=0.04,stroke_color=YELLOW,stroke_width=1.6,
                                   fill_color="#15283A",fill_opacity=1).move_to([x,box.get_bottom()[1]+0.57,0])
            reading=self.eq((rf"N={n:.0f}\,\mathrm{{N}}" if n>0 else r"N=0"),27,YELLOW).next_to(scale,DOWN,buff=0.10)
            wg=self.force(np.array([x+0.55,py+0.28,0]),DOWN*0.95,r"W",RED)
            if n>0:
                ng=self.force(np.array([x-0.55,py-0.45,0]),UP*(0.95*n/(M*G)),r"N",CYAN,LEFT)
            else:
                ng=self.eq(r"N=0",24,CYAN).move_to([x-0.7,py-0.05,0])
            g=VGroup(box,tt,av,person,scale,reading,wg,ng)
            groups.append(g)
        self.play(*[FadeIn(g) for g in groups])
        self.wait(2.2)

        eqs=VGroup(
            self.eq(r"N=m(g+3)",25,GREEN).move_to([-4.8,-3.0,0]),
            self.eq(r"N=m(g-3)",25,YELLOW).move_to([0,-3.0,0]),
            self.eq(r"N=m(g-g)=0",25,RED).move_to([4.8,-3.0,0])
        )
        self.play(FadeIn(eqs))
        key=self.txt("W NO DESAPARECE · N SÍ PUEDE SER CERO",26,BOLD,YELLOW).to_edge(DOWN,buff=0.18)
        self.play(FadeIn(key))
        self.wait(3.0)
        self.wipe()

    # ---------- 6 ----------
    def derive(self):
        self.section(6,"DE FUERZAS A MOVIMIENTO",
                     "Con +y hacia arriba, la gravedad da una aceleración constante. De ahí nacen las ecuaciones de caída libre.")

        axis=Arrow(LEFT*5.7+DOWN*2.0,LEFT*5.7+UP*2.1,buff=0,color=CYAN,stroke_width=3)
        plus=self.txt("+y",20,BOLD,CYAN).next_to(axis,UP,buff=0.06)
        self.play(GrowArrow(axis),FadeIn(plus))

        steps=[
            (r"\sum F_y=-mg=ma_y",RED),
            (r"a_y=-g",YELLOW),
            (r"\frac{dv}{dt}=-g\;\Rightarrow\;v=v_0-gt",CYAN),
            (r"\frac{dy}{dt}=v\;\Rightarrow\;y=y_0+v_0t-\frac12gt^2",GREEN)
        ]
        ys=[1.8,0.55,-0.75,-2.05]
        prev=None
        for (tex,col),y in zip(steps,ys):
            ch=self.formula_chip(tex,col,8.3).move_to(RIGHT*1.55+UP*y)
            self.play(FadeIn(ch,shift=LEFT*0.15),run_time=0.65)
            if prev is not None:
                connector=Arrow(prev.get_bottom(),ch.get_top(),buff=0.08,color=MUTED,stroke_width=2,
                                max_tip_length_to_length_ratio=0.18)
                self.play(Create(connector),run_time=0.3)
            prev=ch
            self.wait(0.55)
        self.wait(2.3)
        self.wipe()

    # ---------- 7 ----------
    def twenty_meter_lab(self):
        self.section(7,"EXPERIMENTO IDEAL: SOLTAR DESDE 20 m",
                     "La separación entre posiciones iguales en tiempo crece: evidencia visual de que la rapidez aumenta.")

        x=-4.8
        ground_y=-2.35
        top_y=2.15
        wall=Line([x-0.85,ground_y,0],[x-0.85,top_y+0.35,0],color=GRID,stroke_width=4)
        ground=Line([x-1.6,ground_y,0],[x+1.3,ground_y,0],color=FG,stroke_width=2.4)
        self.play(Create(wall),Create(ground))

        marks=VGroup()
        for h in [0,5,10,15,20]:
            yy=ground_y+(h/H)*(top_y-ground_y)
            tick=Line([x-1.0,yy,0],[x-0.70,yy,0],color=MUTED,stroke_width=1.4)
            lab=self.txt(f"{h} m",17,NORMAL,MUTED).next_to(tick,LEFT,buff=0.08)
            marks.add(tick,lab)
        self.play(FadeIn(marks))

        ball=Dot([x,top_y,0],radius=0.17,color=YELLOW)
        self.play(FadeIn(ball))
        tracker=ValueTracker(0)
        clock=DecimalNumber(0,num_decimal_places=2,font_size=34,color=CYAN)
        speed=DecimalNumber(0,num_decimal_places=2,font_size=34,color=GREEN)
        height=DecimalNumber(H,num_decimal_places=2,font_size=34,color=YELLOW)
        read=VGroup(
            VGroup(self.txt("t",21,BOLD,CYAN),clock,self.txt("s",18,NORMAL,CYAN)).arrange(RIGHT,buff=0.10),
            VGroup(self.txt("|v|",21,BOLD,GREEN),speed,self.txt("m/s",18,NORMAL,GREEN)).arrange(RIGHT,buff=0.10),
            VGroup(self.txt("y",21,BOLD,YELLOW),height,self.txt("m",18,NORMAL,YELLOW)).arrange(RIGHT,buff=0.10)
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.16).move_to(LEFT*1.2+DOWN*0.1)

        ball.add_updater(lambda b:b.move_to([x,top_y-(top_y-ground_y)*(tracker.get_value()/T_HIT)**2,0]))
        clock.add_updater(lambda d:d.set_value(tracker.get_value()))
        speed.add_updater(lambda d:d.set_value(G*tracker.get_value()))
        height.add_updater(lambda d:d.set_value(max(0,H-0.5*G*tracker.get_value()**2)))
        self.play(FadeIn(read))

        ghosts=VGroup()
        for frac in [0.25,0.50,0.75]:
            tt=T_HIT*frac
            yy=top_y-(top_y-ground_y)*(tt/T_HIT)**2
            ghost=Dot([x,yy,0],radius=0.09,color=MUTED).set_opacity(0.55)
            ghosts.add(ghost)
        self.play(FadeIn(ghosts))
        self.play(tracker.animate.set_value(T_HIT),run_time=3.5,rate_func=linear)
        ball.clear_updaters(); clock.clear_updaters(); speed.clear_updaters(); height.clear_updaters()

        solve=VGroup(
            self.formula_chip(r"0=20-\frac12gt^2",CYAN,6.2),
            self.formula_chip(r"t=\sqrt{\frac{40}{9.81}}\approx 2.02\,\mathrm{s}",YELLOW,6.2),
            self.formula_chip(r"|v|=gt\approx 19.81\,\mathrm{m/s}",GREEN,6.2)
        ).arrange(DOWN,buff=0.22).move_to(RIGHT*3.75+DOWN*0.10)
        for s in solve:
            self.play(FadeIn(s),run_time=0.45)
        self.wait(2.6)
        self.wipe()

    # ---------- 8 ----------
    def synced_graphs(self):
        self.section(8,"LA MISMA CAÍDA EN TRES GRÁFICAS SINCRONIZADAS",
                     "Un solo reloj mueve simultáneamente el objeto, y(t), v(t) y a(t).")

        # three stacked mini-axes
        axes=[]
        configs=[
            ([0,T_HIT,1],[0,20,5],YELLOW,r"y(t)"),
            ([0,T_HIT,1],[-20,0,5],GREEN,r"v(t)"),
            ([0,T_HIT,1],[-12,0,3],RED,r"a(t)")
        ]
        ys=[1.65,-0.15,-1.95]
        for (xr,yr,col,name),yy in zip(configs,ys):
            ax=Axes(x_range=xr,y_range=yr,x_length=6.4,y_length=1.45,
                    axis_config={"color":GRID,"stroke_width":1.5,"include_tip":False})
            ax.move_to(RIGHT*2.9+UP*yy)
            label=self.eq(name,23,col).next_to(ax,LEFT,buff=0.18)
            axes.append((ax,label,col))
        self.play(*[FadeIn(a),FadeIn(l) for a,l,c in axes])

        ax_y,_,_=axes[0]; ax_v,_,_=axes[1]; ax_a,_,_=axes[2]
        curve_y=ax_y.plot(lambda t:H-0.5*G*t*t,x_range=[0,T_HIT],color=YELLOW,stroke_width=3)
        curve_v=ax_v.plot(lambda t:-G*t,x_range=[0,T_HIT],color=GREEN,stroke_width=3)
        curve_a=ax_a.plot(lambda t:-G,x_range=[0,T_HIT],color=RED,stroke_width=3)
        self.play(Create(curve_y),Create(curve_v),Create(curve_a),run_time=1.8)

        # object lane
        lane=Line(LEFT*5.2+UP*2.0,LEFT*5.2+DOWN*2.15,color=GRID,stroke_width=3)
        obj=Dot(LEFT*5.2+UP*2.0,radius=0.15,color=YELLOW)
        self.play(Create(lane),FadeIn(obj))

        tr=ValueTracker(0)
        obj.add_updater(lambda d:d.move_to(LEFT*5.2+UP*(2.0-4.15*(tr.get_value()/T_HIT)**2)))
        dy=always_redraw(lambda:Dot(ax_y.c2p(tr.get_value(),H-0.5*G*tr.get_value()**2),radius=0.065,color=YELLOW))
        dv=always_redraw(lambda:Dot(ax_v.c2p(tr.get_value(),-G*tr.get_value()),radius=0.065,color=GREEN))
        da=always_redraw(lambda:Dot(ax_a.c2p(tr.get_value(),-G),radius=0.065,color=RED))
        time=DecimalNumber(0,num_decimal_places=2,font_size=31,color=CYAN)
        time.add_updater(lambda d:d.set_value(tr.get_value()))
        tlabel=VGroup(self.txt("t =",21,BOLD,CYAN),time,self.txt("s",19,NORMAL,CYAN)).arrange(RIGHT,buff=0.08)
        tlabel.move_to(LEFT*3.55+DOWN*2.65)
        self.add(dy,dv,da)
        self.play(FadeIn(tlabel))
        self.play(tr.animate.set_value(T_HIT),run_time=4.0,rate_func=linear)
        obj.clear_updaters(); time.clear_updaters()
        logic=self.txt("PARÁBOLA EN y  →  RECTA EN v  →  CONSTANTE EN a",22,BOLD,FG).to_edge(DOWN,buff=0.15)
        self.play(FadeIn(logic))
        self.wait(2.5)
        self.wipe()

    # ---------- 9 ----------
    def orbit(self):
        self.section(9,"MICROGRAVEDAD ORBITAL: ESTÁN CAYENDO ALREDEDOR DE LA TIERRA",
                     "Una nave en órbita no está fuera de la gravedad: nave y astronauta comparten prácticamente la misma aceleración.")

        earth=Circle(radius=1.65,stroke_color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=0.13).move_to(LEFT*3.7+DOWN*0.25)
        inner=Circle(radius=1.30,stroke_color=GRID,stroke_width=1).move_to(earth)
        orbit=Circle(radius=2.45,stroke_color=GRID,stroke_width=1.5).move_to(earth)
        globe=self.txt("TIERRA",21,BOLD,BLUE).move_to(earth)
        self.play(FadeIn(earth),FadeIn(inner),Create(orbit),FadeIn(globe))

        theta=ValueTracker(20*DEGREES)
        sat=always_redraw(lambda:Square(side_length=0.34,stroke_color=YELLOW,stroke_width=2,fill_color=YELLOW,fill_opacity=0.15)
                          .move_to(earth.get_center()+2.45*np.array([math.cos(theta.get_value()),math.sin(theta.get_value()),0])))
        gvec=always_redraw(lambda:
            Arrow(sat.get_center(),sat.get_center()+0.95*(earth.get_center()-sat.get_center())/np.linalg.norm(earth.get_center()-sat.get_center()),
                  buff=0,color=RED,stroke_width=4,max_tip_length_to_length_ratio=0.18))
        self.add(sat,gvec)
        self.play(theta.animate.set_value(theta.get_value()+300*DEGREES),run_time=5.0,rate_func=linear)

        facts=VGroup(
            self.card("A 400 km DE ALTURA",f"g ≈ {G_ORBIT:.2f} m/s² ≈ {100*G_ORBIT/G:.1f}% de g en superficie.",6.3,RED),
            self.card("¿POR QUÉ FLOTAN?",r"Nave y astronauta caen juntos. No hay apoyo continuo: N ≈ 0.",6.3,YELLOW),
            self.card("IDEA CLAVE",r"Órbita = caída libre con velocidad horizontal suficiente.",6.3,CYAN)
        ).arrange(DOWN,buff=0.22).move_to(RIGHT*3.6+DOWN*0.25)
        self.play(FadeIn(facts[0]))
        self.play(FadeIn(facts[1]))
        self.play(FadeIn(facts[2]))
        self.wait(2.8)
        self.wipe()

    # ---------- 10 ----------
    def qa_final(self):
        self.section(10,"SENIOR QA · CINCO PRUEBAS DE COMPRENSIÓN",
                     "Si estas cinco relaciones quedan claras, el modelo conceptual de caída libre está bien construido.")

        rows=[
            ("CIMA DEL LANZAMIENTO","v = 0, pero a = −g",YELLOW),
            ("CAÍDA LIBRE IDEAL","solo gravedad → a = g",CYAN),
            ("PESO REAL","W = mg",RED),
            ("INGRAVIDEZ APARENTE","N = 0, pero W ≠ 0",GREEN),
            ("ÓRBITA","caída libre alrededor de la Tierra",PURPLE)
        ]
        cards=VGroup()
        for title,body,col in rows:
            c=self.card(title,body,11.3,col)
            cards.add(c)
        cards.arrange(DOWN,buff=0.20).move_to(DOWN*0.20)
        for c in cards:
            self.play(FadeIn(c,shift=RIGHT*0.12),run_time=0.38)
            self.wait(0.33)

        close=self.txt("FUERZAS → ACELERACIÓN → VELOCIDAD → POSICIÓN",31,BOLD,FG)
        close.to_edge(DOWN,buff=0.20)
        self.play(FadeIn(close))
        self.wait(3.4)
        self.wipe()
