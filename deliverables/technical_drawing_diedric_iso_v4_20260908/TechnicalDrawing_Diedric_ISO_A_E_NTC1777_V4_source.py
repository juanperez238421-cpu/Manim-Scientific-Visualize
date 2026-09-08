#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V4 Senior Total — Sistema diédrico, ISO E / ISO A, NTC 1777:2001.

True 3D camera motion + reusable engineering-graphics library + step-by-step
projection/unfolding + professional orthographic line hierarchy.
Target: ManimCE 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations
import os, sys
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from Core.technical_drawing_tools import *

config.pixel_width=1920; config.pixel_height=1080; config.frame_width=16; config.frame_height=9; config.frame_rate=30; config.background_color=BG
TIME_SCALE=float(os.getenv("LESSON_TIME_SCALE","1.0"))
RTF=.65; RT=1.0; RTS=1.45; RTH=2.0
PBEAT=.9; PREAD=2.1; PEXP=3.2; PLONG=4.5; PCH=9.0

class DiedricISOProjectionV4SeniorTotal(ThreeDScene):
    def play(self,*a,**k):
        if k.get("run_time") is not None: k["run_time"]*=TIME_SCALE
        return super().play(*a,**k)
    def wait(self,duration=DEFAULT_WAIT_TIME,*a,**k): return super().wait(duration*TIME_SCALE,*a,**k)
    def fadd(self,*m): self.add_fixed_in_frame_mobjects(*m); self.add(*m)
    def frem(self,*m):
        try: self.remove_fixed_in_frame_mobjects(*m)
        except Exception: pass
        self.remove(*m)
    def header(self,n,t,s):
        h=section_header(n,t,s); self.fadd(h); self.play(FadeIn(h,shift=DOWN*.08),run_time=RTF); return h
    def transition(self,n,t,s):
        veil=Rectangle(width=16,height=9,stroke_width=0,fill_color=NAVY,fill_opacity=1)
        block=VGroup(safe_text(f"{n:02d}",58,CYAN,BOLD),safe_text(t,48,PAPER,BOLD,13.2),safe_text(s,23,"#C9D6E3",NORMAL,12.5)).arrange(DOWN,buff=.20)
        self.fadd(veil,block); self.play(FadeIn(veil),FadeIn(block,shift=UP*.2),run_time=RT); self.wait(PBEAT); self.play(FadeOut(block),FadeOut(veil),run_time=RT); self.frem(veil,block)
    def note(self,text,color=BLUE,width=6):
        n=callout(text,color,width,20).to_edge(DOWN,buff=.38); self.fadd(n); self.play(FadeIn(n),run_time=RTF); return n
    def cleanup(self,*m):
        if m: self.play(*[FadeOut(x) for x in m],run_time=RT)
        self.frem(*m)

    def construct(self):
        self.camera.background_color=BG
        for fn in [self.opening,self.projection,self.directions,self.unfolding,self.angle_e,self.angle_a,self.compare,self.symbols,self.colombia,self.algorithm,self.challenge,self.closing]: fn()

    def opening(self):
        self.set_camera_orientation(phi=64*DEGREES,theta=-48*DEGREES,zoom=1)
        part=mechanical_bracket_3d().scale(.95); self.play(LaggedStart(*[FadeIn(x,scale=.96) for x in part[:6]],lag_ratio=.1),run_time=RTH); self.play(FadeIn(VGroup(*part[6:])),run_time=RT)
        self.begin_ambient_camera_rotation(rate=.10)
        intro=VGroup(safe_text("SISTEMA DIÉDRICO",52,NAVY,BOLD),safe_text("De una pieza 3D a vistas 2D sin ambigüedad",28,DARK),VGroup(badge("PRIMER DIEDRO · ISO E",ORANGE),badge("TERCER DIEDRO · ISO A",TEAL)).arrange(RIGHT,buff=.3)).arrange(DOWN,buff=.22).to_edge(UP,buff=.3)
        self.fadd(intro); self.play(Write(intro[0]),FadeIn(intro[1]),FadeIn(intro[2]),run_time=RTS); self.wait(PREAD)
        p=self.note("La pieza NO cambia. Cambia la dirección desde la que observamos.",BLUE,7.7); self.wait(PEXP); self.cleanup(p,intro); self.stop_ambient_camera_rotation(); self.play(FadeOut(part),run_time=RT)

    def projection(self):
        self.transition(1,"PROYECCIÓN ORTOGONAL","Observador → pieza → rayos paralelos → plano → vista 2D")
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=.88)
        h=self.header(1,"PROYECCIÓN ORTOGONAL","Sin perspectiva: cada vista registra la geometría desde una dirección exacta.")
        part=mechanical_bracket_3d().scale(.82); plane=vertical_projection_plane(-3.25,7.2,5.0,2.35)
        self.play(FadeIn(part),FadeIn(plane[0]),run_time=RTS); self.play(LaggedStart(*[Create(g) for g in plane[1]],lag_ratio=.02),run_time=RT)
        obs=VGroup(observer_icon(BLUE,.8),badge("OBSERVADOR",BLUE,16)).arrange(DOWN,buff=.12).to_edge(LEFT,buff=.5); self.fadd(obs); self.play(FadeIn(obs),run_time=RT)
        src=[[-3.2,-.2,.42],[-2.75,-.2,1.49],[-1.5,-.2,1.49],[-.95,-.2,1.55],[.78,-.2,1.55],[1.65,-.2,3.56],[2.84,-.2,3.56],[3.2,-.2,.42],[2.25,-.2,2.25]]
        rays=VGroup(*[projection_ray(p,[p[0],-3.25,p[2]],ORANGE) for p in src]); self.play(LaggedStart(*[Create(r) for r in rays],lag_ratio=.08),run_time=RTH)
        n=self.note("Rayos paralelos = no hay perspectiva.",ORANGE,5.4); self.wait(PREAD)
        trace=front_trace_3d(-3.255,BLUE); self.play(Create(trace),run_time=RTH); self.wait(PEXP); self.play(Indicate(trace,color=BLUE),run_time=RT)
        self.cleanup(n); n=self.note("Alineamos la cámara con la misma dirección.",TEAL,6.0); self.move_camera(phi=90*DEGREES,theta=-90*DEGREES,zoom=1.05,run_time=RTH); self.wait(PREAD); self.cleanup(n)
        self.play(FadeOut(rays),FadeOut(part),FadeOut(plane),FadeOut(trace),run_time=RT)
        card=view_card("front",6.0,4.4,.78,True).shift(DOWN*.2); eq=callout("1 dirección → 1 vista",GREEN,4.0,23).next_to(card,DOWN,buff=.22); self.fadd(card,eq); self.play(FadeIn(card),FadeIn(eq),run_time=RTS); self.wait(PEXP); self.cleanup(card,eq,obs,h)

    def directions(self):
        self.transition(2,"SEIS DIRECCIONES PRINCIPALES","La pieza permanece fija; la cámara cambia de eje")
        self.set_camera_orientation(phi=62*DEGREES,theta=-45*DEGREES,zoom=.9); h=self.header(2,"SEIS VISTAS PRINCIPALES","Alzado · planta · laterales · posterior · inferior.")
        part=mechanical_bracket_3d().scale(.82); self.play(FadeIn(part),run_time=RT); self.begin_ambient_camera_rotation(rate=.08); self.wait(PEXP); self.stop_ambient_camera_rotation()
        stops=[(90,-90,"ALZADO",BLUE),(0,-90,"PLANTA",TEAL),(90,0,"LATERAL DERECHO",ORANGE),(90,90,"POSTERIOR",RED),(90,180,"LATERAL IZQUIERDO",PURPLE),(180,-90,"INFERIOR",GREEN)]
        lab=None
        for ph,th,txt,col in stops:
            nl=callout(txt,col,4.1,19).to_edge(DOWN,buff=.38); self.fadd(nl)
            if lab: self.cleanup(lab)
            self.play(FadeIn(nl),run_time=RTF); self.move_camera(phi=ph*DEGREES,theta=th*DEGREES,zoom=1,run_time=RTS); self.wait(PBEAT); lab=nl
        if lab: self.cleanup(lab)
        self.play(FadeOut(part),run_time=RT)
        cards=VGroup(*[view_card(k,4.25,2.48,.48 if k in ["front","rear"] else .46) for k in ["front","top","right","left","rear","bottom"]]).arrange_in_grid(rows=2,cols=3,buff=(.35,.32)).scale(.93).shift(DOWN*.38)
        self.fadd(cards); self.play(LaggedStart(*[FadeIn(c,shift=UP*.08) for c in cards],lag_ratio=.12),run_time=RTH); self.wait(PLONG); self.cleanup(cards,h)

    def unfolding(self):
        self.transition(3,"EL SISTEMA DIÉDRICO","PV y PH son perpendiculares; PH se abate 90°")
        self.set_camera_orientation(phi=65*DEGREES,theta=-45*DEGREES,zoom=.92); h=self.header(3,"PLANOS DIÉDRICOS","PV = vertical · PH = horizontal · LT = línea de tierra.")
        pv,ph,lt=dihedral_planes(7.4); part=mechanical_bracket_3d().scale(.56)
        self.play(FadeIn(pv),FadeIn(ph),Create(lt),FadeIn(part),run_time=RTS)
        labs=VGroup(badge("PV · ALZADO",BLUE,16),badge("PH · PLANTA",TEAL,16),badge("LT",INK,15)).arrange(DOWN,buff=.15).to_corner(UL,buff=.55).shift(DOWN*1.0); self.fadd(labs); self.play(FadeIn(labs),run_time=RT); self.wait(PEXP)
        front=front_trace_3d(.015,BLUE).scale(.48).shift(UP*.2); top=orthographic_view("top",.40).shift(OUT*.03); self.play(Create(front),Create(top),run_time=RTH); self.wait(PREAD)
        n=self.note("ABATIMIENTO: PH gira 90° alrededor de LT.",ORANGE,6.2); self.play(Rotate(ph,PI/2,axis=RIGHT,about_point=ORIGIN),Rotate(top,PI/2,axis=RIGHT,about_point=ORIGIN),run_time=RTH); self.wait(PEXP); self.cleanup(n)
        self.play(FadeOut(pv),FadeOut(ph),FadeOut(lt),FadeOut(part),FadeOut(front),FadeOut(top),run_time=RT); self.cleanup(labs)
        sheet=paper_panel(10.8,5.8,.38).shift(DOWN*.4); fv=view_card("front",4.6,2.35,.47).move_to([-2.6,.55,0]); tv=view_card("top",4.6,2.35,.45).move_to([-2.6,-2.0,0]); line=Line([-5,-.75,0],[5,-.75,0],color=INK,stroke_width=2.4); rule=callout("Ambas vistas quedan en una sola lámina 2D.",GREEN,5.6,21).move_to([2.8,-.1,0]); g=VGroup(sheet,fv,tv,line,rule); self.fadd(g); self.play(FadeIn(sheet),Create(line),FadeIn(fv),FadeIn(tv),FadeIn(rule),run_time=RTH); self.wait(PLONG); self.cleanup(g,h)

    def angle_layout(self,first=True):
        n=4 if first else 5; col=ORANGE if first else TEAL; name="PRIMER DIEDRO · ISO E" if first else "TERCER DIEDRO · ISO A"; order="OBSERVADOR → OBJETO → PLANO" if first else "OBSERVADOR → PLANO → OBJETO"; rule="COLOCACIÓN OPUESTA" if first else "COLOCACIÓN DEL MISMO LADO"
        self.transition(n,name,order); h=self.header(n,name,"La posición física determina dónde aparece cada vista en la lámina.")
        obs=observer_icon(col,.75).move_to([-5.3,.25,0]); obj=orthographic_view("front",.43).move_to([-.1,.25,0] if first else [4,.25,0]); plane=Rectangle(width=.12,height=4.5,stroke_color=BLUE,fill_color=PALE_BLUE,fill_opacity=.65).move_to([4.7,.25,0] if first else [-.6,.25,0])
        seq=VGroup(obs,obj,plane); self.fadd(seq); self.play(FadeIn(obs),run_time=RT); self.play(FadeIn(obj if first else plane),run_time=RTS); self.play(FadeIn(plane if first else obj),run_time=RTS)
        ordc=callout(order,col,6.2,22).to_edge(DOWN,buff=.4); self.fadd(ordc); self.play(FadeIn(ordc),run_time=RT); self.wait(PEXP); self.cleanup(seq,ordc)
        f=view_card("front",4.25,2.45,.50); t=view_card("top",4.0,2.35,.46).scale(.9); r=view_card("right",4.0,2.35,.47).scale(.9); self.fadd(f,t,r); self.play(FadeIn(f),run_time=RT)
        if first: tp=[0,-2.65,0]; rp=[-5.0,0,0]; text="PLANTA abajo · lateral derecho a la izquierda"
        else: tp=[0,2.65,0]; rp=[5.0,0,0]; text="PLANTA arriba · lateral derecho a la derecha"
        self.play(t.animate.move_to(tp),r.animate.move_to(rp),run_time=RTH); c=callout(text,col,6.8,20).to_edge(DOWN,buff=.34); tag=callout(rule,col,4.8,23).to_edge(UP,buff=1.25); self.fadd(c,tag); self.play(FadeIn(c),FadeIn(tag),run_time=RT); self.wait(PLONG); self.cleanup(f,t,r,c,tag,h)
    def angle_e(self): self.angle_layout(True)
    def angle_a(self): self.angle_layout(False)

    def compare(self):
        self.transition(6,"MISMAS VISTAS · DISTINTA DISTRIBUCIÓN","Usa siempre el alzado como ancla")
        h=self.header(6,"COMPARACIÓN DIRECTA","Primer diedro = opuesto · tercer diedro = mismo lado.")
        div=Line([0,2.8,0],[0,-3.5,0],color=LIGHT); titles=VGroup(safe_text("PRIMER DIEDRO · ISO E",24,ORANGE,BOLD),safe_text("TERCER DIEDRO · ISO A",24,TEAL,BOLD)).arrange(RIGHT,buff=3.2).move_to([0,2.65,0]); self.fadd(div,titles); self.play(Create(div),FadeIn(titles),run_time=RT)
        cards=VGroup(view_card("front",2.8,1.8,.33).move_to([-3.9,0,0]),view_card("top",2.8,1.8,.31).move_to([-3.9,-2.05,0]),view_card("right",2.8,1.8,.33).move_to([-6,0,0]),view_card("front",2.8,1.8,.33).move_to([3.9,0,0]),view_card("top",2.8,1.8,.31).move_to([3.9,2.0,0]),view_card("right",2.8,1.8,.33).move_to([6,0,0])); self.fadd(cards); self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.1),run_time=RTH)
        labs=VGroup(callout("OPUESTO",ORANGE,2.8,19).move_to([-3.9,-3.35,0]),callout("MISMO LADO",TEAL,3.0,19).move_to([3.9,-3.35,0])); self.fadd(labs); self.play(FadeIn(labs),run_time=RT); self.wait(PLONG); self.cleanup(cards,labs,div,titles,h)

    def symbols(self):
        self.transition(7,"EL SÍMBOLO LO DECIDE","Identifica el método antes de leer la distribución")
        h=self.header(7,"SÍMBOLOS DE PROYECCIÓN","El tronco de cono + la vista circular codifican el método.")
        s1=projection_symbol(True,1.08).move_to([-3.8,.3,0]); s3=projection_symbol(False,1.08).move_to([3.8,.3,0]); g=VGroup(s1,s3,safe_text("PRIMER DIEDRO",27,ORANGE,BOLD).next_to(s1,UP,buff=.35),safe_text("TERCER DIEDRO",27,TEAL,BOLD).next_to(s3,UP,buff=.35),badge("First-angle · ISO E",ORANGE).next_to(s1,DOWN,buff=.4),badge("Third-angle · ISO A",TEAL).next_to(s3,DOWN,buff=.4)); self.fadd(g); self.play(LaggedStart(Create(s1),Create(s3),FadeIn(g[2]),FadeIn(g[3]),FadeIn(g[4]),FadeIn(g[5]),lag_ratio=.15),run_time=RTH); self.wait(PLONG); w=self.note("No memorices posiciones sin mirar primero el símbolo.",RED,7.0); self.wait(PEXP); self.cleanup(w,g,h)

    def colombia(self):
        self.transition(8,"COLOMBIA · NTC 1777:2001","Norma técnica para representación y métodos de proyección")
        h=self.header(8,"CONTEXTO COLOMBIANO","NTC 1777:2001 es una norma técnica; no es, por sí sola, una ley.")
        block=VGroup(safe_text("NTC 1777:2001",42,NAVY,BOLD),callout("Reconoce PRIMER DIEDRO",ORANGE,5.2,22),callout("Reconoce TERCER DIEDRO",TEAL,5.2,22),callout("Símbolo → método → posición correcta de vistas",BLUE,6.8,21)).arrange(DOWN,buff=.3).shift(DOWN*.2); self.fadd(block); self.play(LaggedStart(*[FadeIn(x,shift=UP*.08) for x in block],lag_ratio=.18),run_time=RTH); self.wait(PLONG); self.cleanup(block,h)

    def algorithm(self):
        self.transition(9,"MÉTODO DE LECTURA","Un algoritmo visual para cualquier lámina")
        h=self.header(9,"LEE UNA LÁMINA EN 6 PASOS","Primero sistema y alzado; después distribución y reconstrucción 3D.")
        steps=VGroup(step_chip(1,"IDENTIFICA EL SÍMBOLO",BLUE,4.5),step_chip(2,"DECIDE ISO E / ISO A",ORANGE,4.5),step_chip(3,"UBICA EL ALZADO",BLUE,4.5),step_chip(4,"LOCALIZA PLANTA Y LATERALES",TEAL,4.5),step_chip(5,"VERIFICA OPUESTO / MISMO",GREEN,4.5),step_chip(6,"RECONSTRUYE EL 3D",PURPLE,4.5)).arrange(DOWN,buff=.13).move_to([-4.1,-.25,0])
        sheet=paper_panel(7,5.8,.38).move_to([3.4,-.15,0]); f=view_card("front",2.7,1.65,.31).move_to([3.4,-.1,0]); t=view_card("top",2.7,1.65,.30).move_to([3.4,1.8,0]); r=view_card("right",2.7,1.65,.31).move_to([5.55,-.1,0]); sym=projection_symbol(False,.55).move_to([1.4,-2.25,0]); g=VGroup(sheet,f,t,r,sym); self.fadd(steps,g); self.play(FadeIn(sheet),run_time=RT)
        for i,s in enumerate(steps):
            self.play(FadeIn(s),run_time=RTF)
            if i==0:self.play(Create(sym),run_time=RT)
            if i==2:self.play(FadeIn(f),run_time=RT)
            if i==3:self.play(FadeIn(t),FadeIn(r),run_time=RT)
            if i==4:self.play(Circumscribe(VGroup(f,t,r),color=GREEN),run_time=RT)
        self.wait(PLONG); self.cleanup(steps,g,h)

    def challenge(self):
        self.transition(10,"DESAFÍO GUIADO","Predice primero; verifica después")
        h=self.header(10,"DESAFÍO DE LECTURA","Decide dónde deben ir la planta y el lateral derecho.")
        sym=projection_symbol(False,.85).move_to([-4.8,1,0]); q=badge("¿QUÉ MÉTODO ES?",BLUE,16).next_to(sym,UP,buff=.25); f=view_card("front",3.3,2.05,.39).move_to([.1,-.1,0]); ts=RoundedRectangle(width=3.3,height=2.05,corner_radius=.12,stroke_color=TEAL,fill_color=PALE_TEAL,fill_opacity=.18).move_to([.1,2.15,0]); ss=RoundedRectangle(width=3.3,height=2.05,corner_radius=.12,stroke_color=ORANGE,fill_color=PALE_ORANGE,fill_opacity=.18).move_to([4.4,-.1,0]); tq=safe_text("PLANTA ?",22,TEAL,BOLD).move_to(ts); sq=safe_text("LATERAL D. ?",22,ORANGE,BOLD).move_to(ss); prompt=callout("PIENSA ANTES DE REVELAR",INK,5.8,21).to_edge(DOWN,buff=.38); setup=VGroup(sym,q,f,ts,ss,tq,sq,prompt); self.fadd(setup); self.play(Create(sym),FadeIn(q),FadeIn(f),FadeIn(ts),FadeIn(ss),FadeIn(tq),FadeIn(sq),FadeIn(prompt),run_time=RTH)
        dots=VGroup(*[Dot(radius=.07,color=MID) for _ in range(5)]).arrange(RIGHT,buff=.12).next_to(prompt,UP,buff=.15); self.fadd(dots); self.play(FadeIn(dots),run_time=RTF)
        for d in dots: self.play(d.animate.set_color(BLUE).scale(1.35),run_time=.25); self.play(d.animate.set_color(MID).scale(1/1.35),run_time=.25)
        self.wait(PCH)
        method=callout("TERCER DIEDRO · ISO A",TEAL,4.2,22).move_to([-4.8,-1.6,0]); tv=view_card("top",3.3,2.05,.38).move_to(ts); rv=view_card("right",3.3,2.05,.39).move_to(ss); ans=callout("MISMO LADO: planta arriba · lateral derecho a la derecha",GREEN,7.4,21).to_edge(DOWN,buff=.38); self.fadd(method,tv,rv,ans); self.play(FadeOut(prompt),FadeOut(dots),FadeIn(method),run_time=RT); self.play(ReplacementTransform(ts,tv),FadeOut(tq),run_time=RTS); self.play(ReplacementTransform(ss,rv),FadeOut(sq),FadeIn(ans),run_time=RTS); self.wait(PLONG); self.cleanup(sym,q,f,method,tv,rv,ans,h)

    def closing(self):
        self.set_camera_orientation(phi=64*DEGREES,theta=-48*DEGREES,zoom=.95); part=mechanical_bracket_3d().scale(.72).shift(RIGHT*4.6); self.play(FadeIn(part),run_time=RTS); self.begin_ambient_camera_rotation(rate=.08)
        block=VGroup(safe_text("MÉTODO FINAL",28,BLUE,BOLD),safe_text("SÍMBOLO → ALZADO → POSICIÓN → 3D",38,NAVY,BOLD,9.8),step_chip(1,"IDENTIFICA EL MÉTODO",BLUE,4.2),step_chip(2,"ANCLA EN EL ALZADO",ORANGE,4.2),step_chip(3,"LEE PLANTA Y LATERALES",TEAL,4.2),step_chip(4,"VERIFICA Y RECONSTRUYE",GREEN,4.2)).arrange(DOWN,aligned_edge=LEFT,buff=.25).move_to([-2.7,-.05,0]); self.fadd(block); self.play(LaggedStart(*[FadeIn(x,shift=RIGHT*.08) for x in block],lag_ratio=.14),run_time=RTH); self.wait(PLONG); final=self.note("3D → 2D SIN AMBIGÜEDAD",GREEN,5.2); self.wait(PEXP); self.stop_ambient_camera_rotation(); self.cleanup(final,block); self.play(FadeOut(part),run_time=RTS)
