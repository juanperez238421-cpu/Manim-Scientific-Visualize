from __future__ import annotations
import os
from typing import Dict, List, Tuple
from manim import *

config.pixel_width=1920; config.pixel_height=1080; config.frame_width=16; config.frame_height=9; config.frame_rate=30; config.background_color=WHITE
TIME_SCALE=float(os.getenv('LESSON_TIME_SCALE','1.0')); GROUP='NOVENO B'
DARK='#303030'; LIGHT='#D7D7D7'; VL='#F2F2F2'; PAPER='#FAFAFA'
RQ=.50; RN=.82; RS=1.10; PS=.55; PR=1.25; PE=1.75; PF=3.50
STUDENTS:List[str]=[
'AGUDELO RESTREPO VALERIA','ARISTIZABAL CORREA SIMON','BADEL TAMAYO MARTIN','BALLESTEROS RIVERA ANTON...',
'CALVETE RINCONES MARIA P...','CATAÑO VILLEGAS LUCIANA','DO NASCIMIENTO ROMERO CA...','GUAL MARTELO MARIA JOSE',
'HERNANDEZ LOPEZ TOMAS','LOPEZ FLOREZ EMANUEL','MADRIGAL BEDOYA DIEGO AL...','MARTINEZ YEPES JERONIMO',
'OCAMPO RAMIREZ DANIEL','OTALVARO ECHEVERRI SALOM...','PALACIO VALLEJO SOFIA','RAMIREZ NAVARRO VIOLETA',
'TRUJILLO GAVIRIA MIGUEL','VILLA SIERRA MIGUEL ANGE...']
SEATS=('A','B','C'); USED=(1,2,3,4,5,6); BLOCKED=7; FREE=(8,9)
ORDER=[(pc,s) for pc in USED for s in SEATS]; ASSIGN=[(i,n,*ORDER[i-1]) for i,n in enumerate(STUDENTS,1)]
POS={9:(-2.75,1.55),6:(0,1.55),3:(2.75,1.55),8:(-2.75,0),5:(0,0),2:(2.75,0),7:(-2.75,-1.55),4:(0,-1.55),1:(2.75,-1.55)}

def validate():
    assert len(STUDENTS)==18 and len(ORDER)==18 and len(ASSIGN)==18
    assert all(pc!=BLOCKED and pc not in FREE for _,_,pc,_ in ASSIGN)
    assert ASSIGN[0][2:]==(1,'A') and ASSIGN[-1][2:]==(6,'C')

def by_pc(pc): return [(i,n,s) for i,n,p,s in ASSIGN if p==pc]

class Scaled(Scene):
    def play(self,*a,**kw):
        if kw.get('run_time') is not None: kw['run_time']*=TIME_SCALE
        return super().play(*a,**kw)
    def wait(self,duration=DEFAULT_WAIT_TIME,*a,**kw): return super().wait(duration*TIME_SCALE,*a,**kw)

class Lab9BFixedSeatingNoPC07(Scaled):
    def t(self,s,z=30,w=NORMAL,c=BLACK): return Text(s,font_size=z,weight=w,color=c)
    def fit(self,m,w,h):
        if m.width>w:m.scale_to_fit_width(w)
        if m.height>h:m.scale_to_fit_height(h)
        return m
    def clear(self):
        if self.mobjects:self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=RN)
    def panel(self,w,h,fill=PAPER): return RoundedRectangle(width=w,height=h,corner_radius=.14,stroke_color=BLACK,stroke_width=1.8,fill_color=fill,fill_opacity=1)
    def header(self,a,b):
        x=self.fit(self.t(a,37,BOLD),14.7,.62); y=self.fit(self.t(b,22,NORMAL,DARK),14.5,.48)
        return VGroup(x,y).arrange(DOWN,buff=.09).to_edge(UP,buff=.20)
    def wrap(self,name,maxw=4.28):
        s=self.t(name,23,MEDIUM)
        if s.width<=maxw:return s
        words=name.split(); best=min((max(len(' '.join(words[:k])),len(' '.join(words[k:])))+.22*abs(len(' '.join(words[:k]))-len(' '.join(words[k:]))),k) for k in range(1,len(words)))[1]
        g=VGroup(self.t(' '.join(words[:best]),21,MEDIUM),self.t(' '.join(words[best:]),21,MEDIUM)).arrange(DOWN,aligned_edge=LEFT,buff=.055)
        return self.fit(g,maxw,.70)
    def room(self,scale=.9,numbers=False):
        box=RoundedRectangle(width=8.85,height=5.65,corner_radius=.18,stroke_color=BLACK,stroke_width=2,fill_color=WHITE,fill_opacity=1)
        title=self.t('VISTA SUPERIOR DEL LABORATORIO',23,BOLD).next_to(box,UP,buff=.10)
        desks={}; circles={}; dg=VGroup(); lookup={(p,s):i for i,_,p,s in ASSIGN}
        for pc in range(1,10):
            x,y=POS[pc]; desk=RoundedRectangle(width=2.18,height=1.10,corner_radius=.10,stroke_color=BLACK,stroke_width=2.8 if pc==7 else 1.7,fill_color=VL if pc==7 else WHITE,fill_opacity=1).move_to([x,y,0])
            lab=self.t('PC07 · NO USAR' if pc==7 else f'PC{pc:02d}',16 if pc==7 else 18,BOLD); self.fit(lab,1.85,.30); lab.move_to(desk.get_center()+UP*.25)
            sg=VGroup()
            for j,s in enumerate(SEATS):
                c=Circle(radius=.19,stroke_color=BLACK,stroke_width=1.25,fill_color=WHITE,fill_opacity=1).move_to([x+(j-1)*.57,y-.27,0]); sg.add(c,self.t(s,13,BOLD).next_to(c,DOWN,buff=.018)); circles[(pc,s)]=c
                if numbers and (pc,s) in lookup: sg.add(self.t(str(lookup[(pc,s)]),16,BOLD).move_to(c))
            parts=VGroup(desk,lab,sg)
            if pc==7:
                parts.add(Line(desk.get_corner(UL)+RIGHT*.12+DOWN*.12,desk.get_corner(DR)+LEFT*.12+UP*.12,stroke_width=3.2,color=BLACK),Line(desk.get_corner(DL)+RIGHT*.12+UP*.12,desk.get_corner(UR)+LEFT*.12+DOWN*.12,stroke_width=3.2,color=BLACK))
            elif pc in FREE:
                f=self.fit(self.t('SIN ASIGNACIÓN',12,BOLD,DARK),1.70,.22); f.move_to(desk.get_center()+UP*.02); parts.add(f)
            desks[pc]=parts; dg.add(parts)
        g=VGroup(box,dg,title).scale(scale); return g,desks,circles
    def card(self,pc):
        box=self.panel(6.45,4.35); title=self.fit(self.t(f'PC{pc:02d} · ASIGNACIÓN',31,BOLD),5.55,.54); title.move_to(box.get_top()+DOWN*.46)
        rows=VGroup()
        for (i,name,s),y in zip(by_pc(pc),(.52,-.52,-1.56)):
            b=Circle(radius=.285,stroke_color=BLACK,stroke_width=1.6,fill_color=WHITE,fill_opacity=1).move_to([-2.68,y,0]); num=self.t(str(i),18,BOLD).move_to(b)
            sb=RoundedRectangle(width=.74,height=.52,corner_radius=.06,stroke_color=BLACK,stroke_width=1.3,fill_color=VL,fill_opacity=1).move_to([-1.86,y,0]); st=self.t(s,19,BOLD).move_to(sb)
            nm=self.wrap(name); nm.set_x(-1.30+nm.width/2); nm.set_y(y); rows.add(VGroup(VGroup(b,num),VGroup(sb,st),nm))
        for u,l in zip(rows[:-1],rows[1:]): assert u.get_bottom()[1]>l.get_top()[1]+.08
        assert title.get_bottom()[1]>rows[0].get_top()[1]+.12
        return VGroup(box,title,rows)
    def construct(self):
        validate(); self.opening(); self.rules(); self.orientation(); self.assign(); self.final()
    def opening(self):
        a=self.t(f'{GROUP} · ASIGNACIÓN DE SILLAS',44,BOLD); b=self.t('Laboratorio · orden oficial de lista',29,NORMAL,DARK); line=Line(LEFT*5.8,RIGHT*5.8,color=LIGHT,stroke_width=2); c=self.t('MESA 7: SIN ESTUDIANTES',33,BOLD); d=self.t('18 estudiantes · 6 mesas activas',25,MEDIUM,DARK)
        g=VGroup(a,b,line,c,d).arrange(DOWN,buff=.25); self.fit(g,14.4,4.8); self.play(FadeIn(a,shift=UP*.15),run_time=RS); self.play(FadeIn(b),Create(line),run_time=RN); self.play(FadeIn(c),FadeIn(d),run_time=RN); self.wait(PE); self.clear()
    def rules(self):
        h=self.header('CRITERIO DE ASIGNACIÓN','La ubicación depende únicamente del número de lista; las calificaciones no se utilizan.')
        lbox=self.panel(6.8,4.85); lt=self.t('REGLAS',31,BOLD); lines=VGroup(*[self.t(x,25,MEDIUM) for x in ['1. Seguir el orden oficial: 1 → 18','2. Tres estudiantes por mesa: A → B → C','3. PC01 a PC06 reciben el grupo','4. PC07 / mesa 7 queda completamente libre','5. PC08 y PC09 quedan sin asignación']]).arrange(DOWN,aligned_edge=LEFT,buff=.31); lg=VGroup(lt,lines).arrange(DOWN,aligned_edge=LEFT,buff=.30); self.fit(lg,6.05,4); lg.move_to(lbox); lg.align_to(lbox,LEFT).shift(RIGHT*.34)
        rbox=self.panel(6.25,4.85); rt=self.t('MAPA NUMÉRICO',31,BOLD); mapl=VGroup(*[self.t(x,z,BOLD) for x,z in [('PC01: 1–3     PC02: 4–6',25),('PC03: 7–9     PC04: 10–12',25),('PC05: 13–15   PC06: 16–18',25),('PC07: NO USAR',27),('PC08 / PC09: SIN ASIGNACIÓN',23)]]).arrange(DOWN,aligned_edge=LEFT,buff=.31); rg=VGroup(rt,mapl).arrange(DOWN,aligned_edge=LEFT,buff=.30); self.fit(rg,5.55,4); rg.move_to(rbox); rg.align_to(rbox,LEFT).shift(RIGHT*.34)
        body=VGroup(VGroup(lbox,lg),VGroup(rbox,rg)).arrange(RIGHT,buff=.55).move_to(DOWN*.45); self.play(FadeIn(h),run_time=RN); self.play(FadeIn(body[0]),run_time=RN); self.wait(PR); self.play(FadeIn(body[1]),run_time=RN); self.wait(PE); self.clear()
    def orientation(self):
        h=self.header('UBICACIÓN FÍSICA DEL LABORATORIO','PC07 se mantiene visible como referencia espacial, pero queda bloqueada.')
        room,desks,_=self.room(1.10); room.move_to(LEFT*2.70+DOWN*.45); nb=self.panel(4.65,4.85); nt=self.t('LECTURA DEL MAPA',27,BOLD); ls=VGroup(*[self.t(x,z,w) for x,z,w in [('Fila superior: PC09 · PC06 · PC03',21,MEDIUM),('Fila media: PC08 · PC05 · PC02',21,MEDIUM),('Fila inferior: PC07 · PC04 · PC01',21,MEDIUM),('PC07 = NO USAR',25,BOLD),('PC08 y PC09 = sin asignación',22,BOLD)]]).arrange(DOWN,aligned_edge=LEFT,buff=.30); ng=VGroup(nt,ls).arrange(DOWN,aligned_edge=LEFT,buff=.30); self.fit(ng,4.05,4); ng.move_to(nb); note=VGroup(nb,ng).move_to(RIGHT*5.25+DOWN*.45)
        self.play(FadeIn(h),run_time=RN); self.play(FadeIn(room),run_time=RN); self.play(FadeIn(note),run_time=RN); self.wait(PR); f=SurroundingRectangle(desks[7],buff=.08,stroke_width=3.2,color=BLACK); lab=self.t('MESA 7 · BLOQUEADA',23,BOLD).next_to(f,UP,buff=.08); self.play(Create(f),FadeIn(lab),run_time=RN); self.wait(PE); self.play(FadeOut(f),FadeOut(lab),run_time=RQ); self.clear()
    def assign(self):
        self.add(self.header(f'ASIGNACIÓN {GROUP} · ORDEN DE LISTA','Cada bloque muestra los tres estudiantes de la mesa activa.'))
        room,desks,circles=self.room(.90); room.move_to(LEFT*4.15+DOWN*.52); self.play(FadeIn(room),run_time=RN); current=None
        for pc in USED:
            card=self.card(pc).move_to(RIGHT*3.55+DOWN*.52); self.play(FadeIn(card) if current is None else ReplacementTransform(current,card),run_time=RN); current=card
            focus=SurroundingRectangle(desks[pc],buff=.06,stroke_width=2.6,color=BLACK); self.play(Create(focus),run_time=RQ)
            for i,_,s in by_pc(pc):
                c=circles[(pc,s)]; self.play(FadeIn(self.t(str(i),16,BOLD).move_to(c),scale=.85),Indicate(c,scale_factor=1.18),run_time=RQ)
            self.wait(PS); self.play(FadeOut(focus),run_time=RQ)
        self.wait(PR); self.play(FadeOut(current),run_time=RN)
        box=self.panel(6.45,2.55); g=VGroup(self.t('ASIGNACIÓN COMPLETA',31,BOLD),VGroup(self.t('18 estudiantes · 18 puestos usados',24,MEDIUM),self.t('PC07: 0 estudiantes',26,BOLD),self.t('PC08 y PC09: sin asignación',23,MEDIUM)).arrange(DOWN,buff=.20)).arrange(DOWN,buff=.25); g.move_to(box); fg=VGroup(box,g).move_to(RIGHT*3.55+DOWN*.52); self.play(FadeIn(fg),run_time=RN); self.wait(PE); self.clear()
    def final(self):
        h=self.header(f'MAPA FINAL · {GROUP}','Ubique su número de lista, luego identifique el PC y la silla A, B o C.')
        room,_,_=self.room(1.06,True); room.move_to(LEFT*2.75+DOWN*.45); lb=self.panel(4.75,5.45); lines=VGroup(*[self.t(x,z,BOLD) for x,z in [('PC01 → 1–3',22),('PC02 → 4–6',22),('PC03 → 7–9',22),('PC04 → 10–12',22),('PC05 → 13–15',22),('PC06 → 16–18',22),('PC07 → NO USAR',24),('PC08 → SIN ASIGNACIÓN',20),('PC09 → SIN ASIGNACIÓN',20)]]).arrange(DOWN,aligned_edge=LEFT,buff=.16); lg=VGroup(self.t('RESUMEN',29,BOLD),lines).arrange(DOWN,aligned_edge=LEFT,buff=.23); self.fit(lg,4.08,4.72); lg.move_to(lb); lg.align_to(lb,LEFT).shift(RIGHT*.34); legend=VGroup(lb,lg).move_to(RIGHT*5.20+DOWN*.45)
        self.play(FadeIn(h),run_time=RN); self.play(FadeIn(room),FadeIn(legend),run_time=RS); self.wait(PE); nb=RoundedRectangle(width=9.2,height=.80,corner_radius=.10,stroke_color=BLACK,stroke_width=1.8,fill_color=VL,fill_opacity=1); n=self.fit(self.t(f'IMPORTANTE: NINGÚN ESTUDIANTE DE {GROUP} SE UBICA EN LA MESA 7.',23,BOLD),8.65,.48); n.move_to(nb); note=VGroup(nb,n).to_edge(DOWN,buff=.20); self.play(FadeIn(note),run_time=RN); self.wait(PF)

if __name__=='__main__': validate()
