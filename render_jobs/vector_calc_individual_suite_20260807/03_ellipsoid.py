from individual_base import *

class VC03Ellipsoid(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 03","ELIPSOIDE",r"Construcción de $x^2/9+y^2/4+z^2/3=1$","Semiejes → interceptos → familias de elipses → superficie")
        self.make_header(1,"ELIPSOIDE: TRES CUADRADOS POSITIVOS","Los denominadores determinan los semiejes y las trazas muestran cómo la superficie se contrae hasta sus interceptos.")
        f=self.formula_panel(r"\frac{x^2}{9}+\frac{y^2}{4}+\frac{z^2}{3}=1")
        s=self.math_step("PASO 1","LEER SEMIEJES",[r"a=3",r"b=2",r"c=\sqrt3"],["Tres términos cuadrados positivos y un lado derecho igual a 1 producen una superficie cerrada."])
        t=self.term_panel([(r"9=3^2","semieje x"),(r"4=2^2","semieje y"),(r"3=(\sqrt3)^2","semieje z")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_ellipsoid_progressive(ax,s)
        self.fade_to_outro(); self.outro("elipsoide",["Normalice la ecuación para que el lado derecho sea 1.","Lea los semiejes a, b, c desde los denominadores.","Marque los seis interceptos coordenados.","Construya z=k y observe la contracción de las elipses.","Verifique con trazas verticales y complete la superficie."])
