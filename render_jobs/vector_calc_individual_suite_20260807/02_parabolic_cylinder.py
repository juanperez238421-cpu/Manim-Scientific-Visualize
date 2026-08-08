from individual_base import *

class VC02ParabolicCylinder(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 02","CILINDRO PARABÓLICO",r"Construcción completa de $y=x^2/2.25$","Curva generatriz → variable libre → extrusión 3D")
        self.make_header(1,"CILINDRO PARABÓLICO: UNA PARÁBOLA EXTRUIDA","Una superficie cilíndrica no tiene que ser circular; cualquier curva plana puede repetirse en la dirección de una variable ausente.")
        f=self.formula_panel(r"y=\frac{x^2}{2.25}")
        s=self.math_step("PASO 1","LEER LA ECUACIÓN",[r"y=\frac{1}{2.25}x^2",r"z\ \text{no aparece}"],["En xy hay una parábola; z queda libre y genera la extrusión."])
        t=self.term_panel([(r"x^2","curvatura parabólica"),(r"y","dirección de apertura"),(r"z","dirección libre")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_parabolic_cylinder(ax,s)
        self.fade_to_outro(); self.outro("cilindro parabólico",["Reconozca la parábola en el plano xy.","Compruebe que z no participa en la ecuación.","Copie la misma parábola en varios valores z=k.","Interprete z como parámetro libre de extrusión.","Complete la superficie con r(u,v)=(u,u²/2.25,v)."])
