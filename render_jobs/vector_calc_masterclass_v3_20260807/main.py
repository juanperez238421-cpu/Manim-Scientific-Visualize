#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vector Calculus Class 02 — Masterclass V3.

This source extends the validated native ManimCE V2 scene but replaces its
layout and every 3D surface builder.  The new rule is strict:

    algebra -> explicit trace equation -> concrete trace -> trace family
    -> vertical trace / generator -> continuous surface.

Manim Community Edition 0.20.1
Final command:
  manim -pqh render_jobs/vector_calc_masterclass_v3_20260807/main.py \
      VectorCalculusSurfacesMasterclassV3 --format=mp4 --disable_caching
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from typing import Sequence

import numpy as np
from manim import *

# Reuse only the already validated lesson sequence and utility behavior.
BASE_FILE = Path(__file__).resolve().parents[1] / "vector_calc_class02_20260807" / "main.py"
spec = importlib.util.spec_from_file_location("vector_calc_v2", BASE_FILE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
BaseLesson = base.VectorCalculusSurfacesClass02Detailed

INFO_X = 4.35
INFO_W = 6.20


class VectorCalculusSurfacesMasterclassV3(BaseLesson):
    """Large-type, trace-first, detailed construction version."""

    # ------------------------------------------------------------------
    # Typography and safe layout
    # ------------------------------------------------------------------
    def text(self, content: str, size: int = 28, weight=NORMAL, **kwargs):
        # V2 was visually too small on a classroom projector.
        return Text(content, font_size=max(22, int(size * 1.13)), color=BLACK,
                    weight=weight, line_spacing=0.94, **kwargs)

    def math(self, expression: str, size: int = 38, **kwargs):
        return MathTex(expression, font_size=max(28, int(size * 1.10)), color=BLACK, **kwargs)

    def make_header(self, number: int, title: str, subtitle: str):
        chip = RoundedRectangle(width=0.78, height=0.54, corner_radius=0.08,
                                stroke_color=BLACK, stroke_width=2,
                                fill_color=WHITE, fill_opacity=1)
        n = self.text(f"{number:02d}", 22, BOLD).move_to(chip)
        tt = self.fit(self.text(title, 34, BOLD), 13.55, 0.60)
        row = VGroup(VGroup(chip, n), tt).arrange(RIGHT, buff=0.24)
        row.to_edge(UP, buff=0.13).to_edge(LEFT, buff=0.40)
        rule = Line(LEFT*7.55, RIGHT*7.55, color="#C8C8C8", stroke_width=1.7)
        rule.next_to(row, DOWN, buff=0.06)
        sub = self.fit(self.text(subtitle, 21), 14.75, 0.64)
        sub.next_to(rule, DOWN, buff=0.06).align_to(row, LEFT)
        g = VGroup(row, rule, sub)
        self.register_fixed(g); self.add(g)
        return g

    def formula_panel(self, expression: str, *, title="ECUACIÓN", y=2.30,
                      width=INFO_W, font_size=42):
        lab = self.text(title, 19, BOLD)
        eq = self.fit(self.math(expression, 44), width-0.55, 0.78)
        content = VGroup(lab, eq).arrange(DOWN, buff=0.12)
        box = RoundedRectangle(width=width, height=1.44, corner_radius=0.10,
                               stroke_color=BLACK, stroke_width=1.5,
                               fill_color="#F7F7F7", fill_opacity=1)
        content.move_to(box)
        g = VGroup(box, content).move_to([INFO_X, y, 0])
        self.register_fixed(g)
        return g

    def step_panel(self, step: str, title: str, lines: Sequence[str], *, y=-0.05,
                   width=INFO_W, body_size=22):
        chip = RoundedRectangle(width=1.18, height=0.42, corner_radius=0.07,
                                stroke_color=BLACK, stroke_width=1.3,
                                fill_color="#E9E9E9", fill_opacity=1)
        cn = self.text(step, 16, BOLD).move_to(chip)
        heading = self.fit(self.text(title, 25, BOLD), 4.55, 0.48)
        head = VGroup(VGroup(chip, cn), heading).arrange(RIGHT, buff=0.16)
        body = VGroup(*[self.fit(self.text(s, max(21, body_size)), width-0.65, 0.44) for s in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        self.fit(content, width-0.44, 2.15)
        box = RoundedRectangle(width=width, height=2.42, corner_radius=0.10,
                               stroke_color=BLACK, stroke_width=1.3,
                               fill_color=WHITE, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.22)
        g = VGroup(box, content).move_to([INFO_X, y, 0])
        self.register_fixed(g)
        return g

    def math_step(self, step: str, title: str, equations: Sequence[str], notes: Sequence[str] = ()):
        chip = RoundedRectangle(width=1.18, height=0.42, corner_radius=0.07,
                                stroke_color=BLACK, stroke_width=1.3,
                                fill_color="#E9E9E9", fill_opacity=1)
        cn = self.text(step, 16, BOLD).move_to(chip)
        heading = self.fit(self.text(title, 25, BOLD), 4.55, 0.48)
        head = VGroup(VGroup(chip, cn), heading).arrange(RIGHT, buff=0.16)
        eqs = VGroup(*[self.fit(self.math(e, 31), INFO_W-0.68, 0.49) for e in equations])
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        ns = VGroup(*[self.fit(self.text(n, 20), INFO_W-0.68, 0.41) for n in notes])
        if len(ns):
            ns.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            content = VGroup(head, eqs, ns).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        else:
            content = VGroup(head, eqs).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        self.fit(content, INFO_W-0.45, 2.14)
        box = RoundedRectangle(width=INFO_W, height=2.42, corner_radius=0.10,
                               stroke_color=BLACK, stroke_width=1.3,
                               fill_color=WHITE, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.22)
        g = VGroup(box, content).move_to([INFO_X, -0.05, 0])
        self.register_fixed(g)
        return g

    def term_panel(self, entries, *, y=-2.55, width=INFO_W):
        rows = VGroup()
        for symbol, meaning in entries:
            sm = self.fit(self.math(symbol, 27), 1.55, 0.42)
            tm = self.fit(self.text(meaning, 19), 4.15, 0.42)
            rows.add(VGroup(sm, tm).arrange(RIGHT, buff=0.18))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        self.fit(rows, width-0.45, 1.28)
        box = RoundedRectangle(width=width, height=1.53, corner_radius=0.10,
                               stroke_color="#C8C8C8", stroke_width=1.2,
                               fill_color=WHITE, fill_opacity=1)
        rows.move_to(box).align_to(box, LEFT).shift(RIGHT*0.22)
        g = VGroup(box, rows).move_to([INFO_X, y, 0])
        self.register_fixed(g)
        return g

    def replace_fixed_panel(self, old, new, pause=1.55):
        self.remove(new)
        self.paced_play(ReplacementTransform(old, new), run_time=0.55, pause=pause)
        return new

    def clear_section(self):
        # V2 inserted a perceptible empty hold. V3 keeps only the fade transition.
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.55)
        self.clear()

    # ------------------------------------------------------------------
    # Larger stable 3D viewport
    # ------------------------------------------------------------------
    def set_stable_camera(self):
        self.set_camera_orientation(phi=66*DEGREES, theta=-54*DEGREES, zoom=0.95)

    def axes3d(self):
        ax = ThreeDAxes(
            x_range=[-4,4,1], y_range=[-4,4,1], z_range=[-4,4,1],
            x_length=7.10, y_length=7.10, z_length=5.90,
            axis_config={"color": BLACK, "stroke_width": 1.55,
                         "include_ticks": False, "include_tip": True},
        )
        ax.shift(LEFT*3.05 + DOWN*0.35)
        return ax

    def trace_curve(self, axes, fn, t0=0, t1=TAU, width=3.0):
        return ParametricFunction(lambda t: axes.c2p(*fn(t)), t_range=[t0,t1],
                                  color=BLACK, stroke_width=width)

    def style_surface(self, surface, opacity=0.30):
        surface.set_style(fill_opacity=opacity, stroke_color="#686868", stroke_width=0.48)
        surface.set_fill("#C8C8C8", opacity=opacity)
        return surface

    def dim(self, *mobs):
        anims=[]
        for m in mobs:
            try: anims.append(m.animate.set_stroke("#777777", width=1.35, opacity=0.70))
            except Exception: pass
        if anims: self.play(*anims, run_time=0.45)

    # ------------------------------------------------------------------
    # Dedicated detailed builders
    # ------------------------------------------------------------------
    def build_circular_cylinder(self, axes, step):
        d=self.math_step("PASO 2","VARIABLE AUSENTE",
                         [r"x^2+y^2=4", r"z\ \text{no aparece}"],
                         ["La misma sección existe para cualquier altura z=k."])
        step=self.replace_fixed_panel(step,d,1.8)
        rings=VGroup()
        for i,z in enumerate([-2.6,-1.3,0,1.3,2.6],1):
            d=self.math_step(f"TRAZA {i}",f"FIJAR z={z:g}",
                             [rf"z={z:g}",r"x^2+y^2=4"],
                             ["La ecuación no cambia: radio 2 en cada plano."])
            step=self.replace_fixed_panel(step,d,0.9)
            c=self.trace_curve(axes,lambda t,z=z:np.array([2*np.cos(t),2*np.sin(t),z]),width=3.2 if z==0 else 2.0)
            if len(rings): self.dim(*rings)
            rings.add(c); self.paced_play(Create(c),run_time=1.05,pause=1.05)
        d=self.math_step("PASO 3","GENERATRICES",
                         [r"(x,y)=(2\cos\theta,2\sin\theta)",r"z\in\mathbb R"],
                         ["Fijar θ genera una recta paralela al eje z."])
        step=self.replace_fixed_panel(step,d,1.7)
        gens=VGroup()
        for a in np.linspace(0,TAU,9)[:-1]:
            x,y=2*np.cos(a),2*np.sin(a)
            l=Line3D(axes.c2p(x,y,-2.9),axes.c2p(x,y,2.9),color="#303030",thickness=0.013)
            gens.add(l); self.paced_play(Create(l),run_time=0.45,pause=0.30)
        d=self.math_step("PASO 4","BARRIDO CONTINUO",
                         [r"\mathbf r(\theta,z)=(2\cos\theta,2\sin\theta,z)"],
                         ["Infinitas generatrices llenan la pared del cilindro."])
        step=self.replace_fixed_panel(step,d,1.8)
        surf=Surface(lambda u,v:axes.c2p(2*np.cos(u),2*np.sin(u),v),u_range=[0,TAU],v_range=[-2.9,2.9],resolution=(36,18))
        self.style_surface(surf,0.28); self.paced_play(FadeIn(surf),run_time=1.45,pause=3.0)
        return VGroup(rings,gens,surf)

    def build_parabolic_cylinder(self, axes, step):
        d=self.math_step("PASO 2","TRAZA GENERATRIZ",
                         [r"z=0",r"y=\frac{x^2}{2.25}"],
                         ["Primero se dibuja una parábola completa en el plano xy."])
        step=self.replace_fixed_panel(step,d,1.7)
        basec=self.trace_curve(axes,lambda t:np.array([t,t*t/2.25,0]),-2.3,2.3,3.2)
        self.paced_play(Create(basec),run_time=1.4,pause=1.4)
        copies=VGroup(basec)
        for z in [-2.4,-1.2,1.2,2.4]:
            d=self.math_step("PASO 3",f"COPIA EN z={z:g}",
                             [rf"z={z:g}",r"y=\frac{x^2}{2.25}"],
                             ["z cambia, pero la parábola conserva forma y posición xy."])
            step=self.replace_fixed_panel(step,d,0.9)
            c=self.trace_curve(axes,lambda t,z=z:np.array([t,t*t/2.25,z]),-2.3,2.3,2.0)
            self.dim(*copies); copies.add(c); self.paced_play(Create(c),run_time=0.9,pause=0.8)
        d=self.math_step("PASO 4","PARAMETRIZAR LA EXTRUSIÓN",
                         [r"\mathbf r(u,v)=(u,\frac{u^2}{2.25},v)"],
                         ["u recorre la parábola y v recorre la dirección libre z."])
        step=self.replace_fixed_panel(step,d,1.8)
        surf=Surface(lambda u,v:axes.c2p(u,u*u/2.25,v),u_range=[-2.3,2.3],v_range=[-2.6,2.6],resolution=(28,18))
        self.style_surface(surf,0.28); self.paced_play(FadeIn(surf),run_time=1.45,pause=3.0)
        return VGroup(copies,surf)

    def build_ellipsoid_progressive(self, axes, step):
        d=self.math_step("PASO 2","INTERCEPTOS",
                         [r"(\pm3,0,0)",r"(0,\pm2,0)",r"(0,0,\pm\sqrt3)"],
                         ["Los denominadores son los cuadrados de los semiejes."])
        step=self.replace_fixed_panel(step,d,1.7)
        pts=VGroup(*[Dot3D(axes.c2p(*p),radius=0.07,color=BLACK) for p in [(3,0,0),(-3,0,0),(0,2,0),(0,-2,0),(0,0,math.sqrt(3)),(0,0,-math.sqrt(3))]])
        self.paced_play(LaggedStart(*[FadeIn(p) for p in pts],lag_ratio=0.12),run_time=1.3,pause=1.3)
        rings=VGroup()
        for k in [0,0.65,1.15,1.50]:
            q=max(0,1-k*k/3); a=3*math.sqrt(q); b=2*math.sqrt(q)
            d=self.math_step("PASO 3",f"TRAZA z=±{k:g}" if k else "TRAZA z=0",
                             [rf"\frac{{x^2}}{{9}}+\frac{{y^2}}{{4}}=1-\frac{{({k:g})^2}}{{3}}",rf"a_k={a:.2f},\ b_k={b:.2f}"],
                             ["Al aumentar |z|, la elipse horizontal se contrae."])
            step=self.replace_fixed_panel(step,d,0.9)
            vals=[k] if k==0 else [k,-k]
            for z in vals:
                c=self.trace_curve(axes,lambda t,z=z,a=a,b=b:np.array([a*np.cos(t),b*np.sin(t),z]),width=2.8 if k==0 else 1.9)
                rings.add(c); self.paced_play(Create(c),run_time=0.75,pause=0.55)
        d=self.math_step("PASO 4","TRAZAS VERTICALES",
                         [r"x=0:\ \frac{y^2}{4}+\frac{z^2}{3}=1",r"y=0:\ \frac{x^2}{9}+\frac{z^2}{3}=1"],
                         ["Las tres familias de cortes son cerradas y acotadas."])
        step=self.replace_fixed_panel(step,d,1.7)
        yz=self.trace_curve(axes,lambda t:np.array([0,2*np.cos(t),math.sqrt(3)*np.sin(t)]),width=2.8)
        xz=self.trace_curve(axes,lambda t:np.array([3*np.cos(t),0,math.sqrt(3)*np.sin(t)]),width=2.8)
        self.paced_play(Create(yz),run_time=1.1,pause=1.0); self.paced_play(Create(xz),run_time=1.1,pause=1.2)
        d=self.math_step("PASO 5","RELLENAR ENTRE TRAZAS",
                         [r"x=3\sin\phi\cos\theta",r"y=2\sin\phi\sin\theta",r"z=\sqrt3\cos\phi"],
                         ["Los parámetros recorren todas las secciones intermedias."])
        step=self.replace_fixed_panel(step,d,1.8)
        surf=Surface(lambda u,v:axes.c2p(3*np.sin(v)*np.cos(u),2*np.sin(v)*np.sin(u),math.sqrt(3)*np.cos(v)),u_range=[0,TAU],v_range=[0,PI],resolution=(36,22))
        self.style_surface(surf,0.29); self.paced_play(FadeIn(surf),run_time=1.5,pause=3.0)
        return VGroup(pts,rings,yz,xz,surf)

    def build_hyperboloid_one_sheet(self, axes, step):
        d=self.math_step("PASO 2","CINTURA z=0",
                         [r"\frac{x^2}{4}+\frac{y^2}{2}=1"],
                         ["Esta elipse es la sección mínima y mantiene conectada la superficie."])
        step=self.replace_fixed_panel(step,d,1.7)
        waist=self.trace_curve(axes,lambda t:np.array([2*np.cos(t),math.sqrt(2)*np.sin(t),0]),width=3.2)
        self.paced_play(Create(waist),run_time=1.2,pause=1.2)
        slices=VGroup(waist)
        for k in [0.8,1.6,2.4]:
            f=math.sqrt(1+k*k/4); a=2*f; b=math.sqrt(2)*f
            d=self.math_step("PASO 3",f"TRAZAS z=±{k:g}",
                             [rf"\frac{{x^2}}{{4}}+\frac{{y^2}}{{2}}=1+\frac{{({k:g})^2}}{{4}}",rf"a_k={a:.2f},\ b_k={b:.2f}"],
                             ["El lado derecho crece: las elipses se ensanchan."])
            step=self.replace_fixed_panel(step,d,0.9)
            for z in [k,-k]:
                c=self.trace_curve(axes,lambda t,z=z,a=a,b=b:np.array([a*np.cos(t),b*np.sin(t),z]),width=1.9)
                slices.add(c); self.paced_play(Create(c),run_time=0.65,pause=0.45)
        d=self.math_step("PASO 4","TRAZA VERTICAL",
                         [r"y=0:\ \frac{x^2}{4}-\frac{z^2}{4}=1"],
                         ["En xz aparece una hipérbola: confirma apertura en ±z."])
        step=self.replace_fixed_panel(step,d,1.7)
        b1=self.trace_curve(axes,lambda t:np.array([2*np.cosh(t),0,2*np.sinh(t)]),-1.05,1.05,2.7)
        b2=self.trace_curve(axes,lambda t:np.array([-2*np.cosh(t),0,2*np.sinh(t)]),-1.05,1.05,2.7)
        self.paced_play(Create(b1),Create(b2),run_time=1.3,pause=1.3)
        d=self.math_step("PASO 5","SUPERFICIE",
                         [r"x=2\cosh v\cos u",r"y=\sqrt2\cosh v\sin u",r"z=2\sinh v"],
                         ["Cada valor de v define una elipse de la familia."])
        step=self.replace_fixed_panel(step,d,1.8)
        surf=Surface(lambda u,v:axes.c2p(2*np.cosh(v)*np.cos(u),math.sqrt(2)*np.cosh(v)*np.sin(u),2*np.sinh(v)),u_range=[0,TAU],v_range=[-1.05,1.05],resolution=(36,22))
        self.style_surface(surf,0.28); self.paced_play(FadeIn(surf),run_time=1.5,pause=3.0)
        return VGroup(slices,b1,b2,surf)

    def build_two_sheet_hyperboloid(self, axes, step):
        d=self.math_step("PASO 2","PROBAR z=0",
                         [r"-\frac{x^2}{4}-\frac{y^2}{4}=1"],
                         ["No hay solución real: existe un hueco central."])
        step=self.replace_fixed_panel(step,d,1.8)
        d=self.math_step("PASO 3","UMBRAL DE EXISTENCIA",
                         [r"\frac{z^2}{4}=1+\frac{x^2+y^2}{4}\ge1",r"|z|\ge2"],
                         ["Los primeros puntos reales son (0,0,±2)."])
        step=self.replace_fixed_panel(step,d,1.8)
        p1=Dot3D(axes.c2p(0,0,2),radius=0.075,color=BLACK); p2=Dot3D(axes.c2p(0,0,-2),radius=0.075,color=BLACK)
        self.paced_play(FadeIn(p1),FadeIn(p2),run_time=0.8,pause=1.1)
        slices=VGroup()
        for k in [2.2,2.7,3.3]:
            r=2*math.sqrt(k*k/4-1)
            d=self.math_step("PASO 4",f"TRAZAS z=±{k:g}",
                             [rf"x^2+y^2=4\left(\frac{{({k:g})^2}}{{4}}-1\right)",rf"r_k={r:.2f}"],
                             ["El radio nace en 0 cuando |z|=2 y luego crece."])
            step=self.replace_fixed_panel(step,d,0.9)
            for z in [k,-k]:
                c=self.trace_curve(axes,lambda t,z=z,r=r:np.array([r*np.cos(t),r*np.sin(t),z]),width=1.9)
                slices.add(c); self.paced_play(Create(c),run_time=0.65,pause=0.45)
        d=self.math_step("PASO 5","TRAZA VERTICAL",
                         [r"y=0:\ \frac{z^2}{4}-\frac{x^2}{4}=1"],
                         ["La hipérbola vertical muestra dos ramas separadas."])
        step=self.replace_fixed_panel(step,d,1.7)
        b1=self.trace_curve(axes,lambda t:np.array([2*np.sinh(t),0,2*np.cosh(t)]),-1,1,2.7)
        b2=self.trace_curve(axes,lambda t:np.array([2*np.sinh(t),0,-2*np.cosh(t)]),-1,1,2.7)
        self.paced_play(Create(b1),Create(b2),run_time=1.3,pause=1.3)
        d=self.math_step("PASO 6","DOS HOJAS",
                         [r"z=\pm2\cosh v"],
                         ["El ± produce dos superficies que nunca se conectan."])
        step=self.replace_fixed_panel(step,d,1.8)
        top=Surface(lambda u,v:axes.c2p(2*np.sinh(v)*np.cos(u),2*np.sinh(v)*np.sin(u),2*np.cosh(v)),u_range=[0,TAU],v_range=[0,1],resolution=(34,18))
        bot=Surface(lambda u,v:axes.c2p(2*np.sinh(v)*np.cos(u),2*np.sinh(v)*np.sin(u),-2*np.cosh(v)),u_range=[0,TAU],v_range=[0,1],resolution=(34,18))
        self.style_surface(top,0.28); self.style_surface(bot,0.28)
        self.paced_play(FadeIn(top),FadeIn(bot),run_time=1.5,pause=3.0)
        return VGroup(p1,p2,slices,b1,b2,top,bot)

    def build_cone(self, axes, step):
        d=self.math_step("PASO 2","VÉRTICE",
                         [r"z^2=x^2+y^2",r"x=y=0\Rightarrow z=0"],
                         ["Las dos nappes se encuentran exactamente en el origen."])
        step=self.replace_fixed_panel(step,d,1.7)
        apex=Dot3D(axes.c2p(0,0,0),radius=0.075,color=BLACK); self.paced_play(FadeIn(apex),pause=1.0)
        slices=VGroup()
        for k in [0.8,1.6,2.4]:
            d=self.math_step("PASO 3",f"TRAZAS z=±{k:g}",
                             [rf"x^2+y^2=({k:g})^2",rf"r=|z|={k:g}"],
                             ["El radio crece linealmente con la distancia al vértice."])
            step=self.replace_fixed_panel(step,d,0.9)
            for z in [k,-k]:
                c=self.trace_curve(axes,lambda t,z=z,k=k:np.array([k*np.cos(t),k*np.sin(t),z]),width=1.9)
                slices.add(c); self.paced_play(Create(c),run_time=0.65,pause=0.45)
        d=self.math_step("PASO 4","TRAZAS VERTICALES",
                         [r"y=0:\ z=\pm x",r"x=0:\ z=\pm y"],
                         ["Los cortes verticales son rectas que pasan por el vértice."])
        step=self.replace_fixed_panel(step,d,1.7)
        lines=VGroup()
        for vec in [(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)]:
            v=np.array(vec,dtype=float); v=v/np.linalg.norm(v)*3.2
            l=Line3D(axes.c2p(*(-v)),axes.c2p(*v),color="#303030",thickness=0.013)
            lines.add(l); self.paced_play(Create(l),run_time=0.5,pause=0.3)
        d=self.math_step("PASO 5","BARRIDO ANGULAR",
                         [r"\mathbf r(\theta,z)=(|z|\cos\theta,|z|\sin\theta,z)"],
                         ["Rotar una generatriz alrededor de z forma el cono completo."])
        step=self.replace_fixed_panel(step,d,1.8)
        surf=Surface(lambda u,v:axes.c2p(abs(v)*np.cos(u),abs(v)*np.sin(u),v),u_range=[0,TAU],v_range=[-2.8,2.8],resolution=(36,20))
        self.style_surface(surf,0.27); self.paced_play(FadeIn(surf),run_time=1.5,pause=3.0)
        return VGroup(apex,slices,lines,surf)

    def build_elliptic_paraboloid(self, axes, step):
        d=self.math_step("PASO 2","VÉRTICE Y RANGO",
                         [r"z=\frac{x^2+y^2}{4}\ge0",r"V=(0,0,0)"],
                         ["Solo existe para z≥0 y abre hacia +z."])
        step=self.replace_fixed_panel(step,d,1.7)
        vertex=Dot3D(axes.c2p(0,0,0),radius=0.075,color=BLACK); self.paced_play(FadeIn(vertex),pause=1.0)
        rings=VGroup()
        for k in [0.25,1,2.25]:
            r=2*math.sqrt(k)
            d=self.math_step("PASO 3",f"TRAZA z={k:g}",
                             [rf"x^2+y^2=4({k:g})",rf"r=2\sqrt{{{k:g}}}={r:.2f}"],
                             ["Los círculos se expanden a medida que aumenta z."])
            step=self.replace_fixed_panel(step,d,0.9)
            c=self.trace_curve(axes,lambda t,k=k,r=r:np.array([r*np.cos(t),r*np.sin(t),k]),width=2.1)
            rings.add(c); self.paced_play(Create(c),run_time=0.85,pause=0.65)
        d=self.math_step("PASO 4","TRAZAS VERTICALES",
                         [r"y=0:\ z=\frac{x^2}{4}",r"x=0:\ z=\frac{y^2}{4}"],
                         ["Ambas parábolas comparten vértice y abren hacia +z."])
        step=self.replace_fixed_panel(step,d,1.7)
        px=self.trace_curve(axes,lambda t:np.array([t,0,t*t/4]),-3,3,2.8)
        py=self.trace_curve(axes,lambda t:np.array([0,t,t*t/4]),-3,3,2.8)
        self.paced_play(Create(px),run_time=1.2,pause=1.0); self.paced_play(Create(py),run_time=1.2,pause=1.1)
        d=self.math_step("PASO 5","SUPERFICIE",
                         [r"x=2r\cos\theta",r"y=2r\sin\theta",r"z=r^2"],
                         ["Aumentar r expande el círculo y eleva z cuadráticamente."])
        step=self.replace_fixed_panel(step,d,1.8)
        surf=Surface(lambda u,v:axes.c2p(2*v*np.cos(u),2*v*np.sin(u),v*v),u_range=[0,TAU],v_range=[0,1.72],resolution=(36,20))
        self.style_surface(surf,0.28); self.paced_play(FadeIn(surf),run_time=1.5,pause=3.0)
        return VGroup(vertex,rings,px,py,surf)

    def build_hyperbolic_paraboloid(self, axes, step):
        d=self.math_step("PASO 2","CORTE CENTRAL z=0",
                         [r"0=\frac{x^2-y^2}{4}",r"(x-y)(x+y)=0",r"y=\pm x"],
                         ["Dos rectas se cruzan en el punto silla."])
        step=self.replace_fixed_panel(step,d,1.8)
        l1=self.trace_curve(axes,lambda t:np.array([t,t,0]),-2.8,2.8,2.7)
        l2=self.trace_curve(axes,lambda t:np.array([t,-t,0]),-2.8,2.8,2.7)
        self.paced_play(Create(l1),Create(l2),run_time=1.2,pause=1.1)
        d=self.math_step("PASO 3","PARÁBOLAS OPUESTAS",
                         [r"y=0:\ z=\frac{x^2}{4}",r"x=0:\ z=-\frac{y^2}{4}"],
                         ["Una dirección sube y la otra baja: aparece la silla."])
        step=self.replace_fixed_panel(step,d,1.8)
        up=self.trace_curve(axes,lambda t:np.array([t,0,t*t/4]),-3,3,2.8)
        down=self.trace_curve(axes,lambda t:np.array([0,t,-t*t/4]),-3,3,2.8)
        self.paced_play(Create(up),run_time=1.2,pause=1.0); self.paced_play(Create(down),run_time=1.2,pause=1.1)
        hypers=VGroup()
        for k in [0.7,-0.7,1.4,-1.4]:
            a=math.sqrt(abs(4*k))
            d=self.math_step("PASO 4",f"TRAZA z={k:g}",
                             [rf"x^2-y^2=4({k:g})"],
                             ["k>0 abre en x; k<0 abre en y: son hipérbolas."])
            step=self.replace_fixed_panel(step,d,0.85)
            if k>0:
                b1=self.trace_curve(axes,lambda t,a=a,k=k:np.array([a*np.cosh(t),a*np.sinh(t),k]),-0.9,0.9,1.8)
                b2=self.trace_curve(axes,lambda t,a=a,k=k:np.array([-a*np.cosh(t),a*np.sinh(t),k]),-0.9,0.9,1.8)
            else:
                b1=self.trace_curve(axes,lambda t,a=a,k=k:np.array([a*np.sinh(t),a*np.cosh(t),k]),-0.9,0.9,1.8)
                b2=self.trace_curve(axes,lambda t,a=a,k=k:np.array([a*np.sinh(t),-a*np.cosh(t),k]),-0.9,0.9,1.8)
            hypers.add(b1,b2); self.paced_play(Create(b1),Create(b2),run_time=0.65,pause=0.55)
        d=self.math_step("PASO 5","RELLENAR ENTRE TRAZAS",
                         [r"z=\frac{x^2-y^2}{4}"],
                         ["La superficie conecta continuamente las parábolas e hipérbolas."])
        step=self.replace_fixed_panel(step,d,1.8)
        surf=Surface(lambda u,v:axes.c2p(u,v,(u*u-v*v)/4),u_range=[-2.8,2.8],v_range=[-2.8,2.8],resolution=(26,26))
        self.style_surface(surf,0.27); self.paced_play(FadeIn(surf),run_time=1.5,pause=3.0)
        return VGroup(l1,l2,up,down,hypers,surf)

    # ------------------------------------------------------------------
    # Replace simple worked examples with explicit algebra.
    # ------------------------------------------------------------------
    def worked_examples(self):
        self.make_header(11,"EJEMPLO A: COMPLETAR CUADRADOS ANTES DE CLASIFICAR",
                         "Una ecuación general debe transformarse antes de asociarla con una familia geométrica.")
        f=self.formula_panel(r"x^2+y^2+z^2-4x+2y-6z=2")
        s=self.math_step("PASO 1","AGRUPAR",
                         [r"(x^2-4x)+(y^2+2y)+(z^2-6z)=2"],
                         ["Complete un cuadrado perfecto en cada variable."])
        t=self.term_panel([(r"x^2-4x","(x-2)^2-4"),(r"y^2+2y","(y+1)^2-1"),(r"z^2-6z","(z-3)^2-9")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        s2=self.math_step("PASO 2","SUSTITUIR Y ORDENAR",
                          [r"(x-2)^2-4+(y+1)^2-1+(z-3)^2-9=2",r"(x-2)^2+(y+1)^2+(z-3)^2=16"],
                          ["Tres cuadrados positivos: esfera, caso particular de elipsoide."])
        s=self.replace_fixed_panel(s,s2,2.6)
        result=self.text("Centro (2,−1,3) · radio 4 · familia: esfera/elipsoide",27,BOLD).to_edge(DOWN,buff=0.50)
        self.register_fixed(result); self.paced_play(FadeIn(result),pause=3.5)
        self.clear_section()

        self.make_header(12,"EJEMPLO B: PARABOLOIDE DESPLAZADO",
                         "Después de clasificar, indique vértice, eje, dirección de apertura y una familia de trazas.")
        f=self.formula_panel(r"z=4-\frac{x^2}{4}-y^2")
        s=self.math_step("PASO 1","AISLAR LA PARTE CUADRÁTICA",
                         [r"4-z=\frac{x^2}{4}+y^2"],
                         ["El lado derecho es no negativo, por tanto z≤4."])
        t=self.term_panel([(r"V=(0,0,4)","vértice"),(r"-x^2,-y^2","apertura hacia −z"),(r"z\le4","rango vertical")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        s2=self.math_step("PASO 2","TRAZA HORIZONTAL z=k",
                          [r"\frac{x^2}{4}+y^2=4-k"],
                          ["Para k<4 aparecen elipses que crecen al descender."])
        s=self.replace_fixed_panel(s,s2,2.6)
        result=self.text("Paraboloide elíptico · vértice (0,0,4) · apertura −z",28,BOLD).to_edge(DOWN,buff=0.50)
        self.register_fixed(result); self.paced_play(FadeIn(result),pause=3.5)
        self.clear_section()


# The inherited construct() calls every overridden method above through dynamic dispatch.
