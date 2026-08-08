from individual_base import *

class VC07EllipticParaboloid(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 07","PARABOLOIDE ELÍPTICO",r"Construcción de $z=(x^2+y^2)/4$","Vértice → círculos crecientes → parábolas verticales")
        self.make_header(1,"PARABOLOIDE ELÍPTICO: UNA COPA EN R³","Una variable lineal y dos cuadrados del mismo signo producen una superficie con vértice y una única dirección de apertura.")
        f=self.formula_panel(r"z=\frac{x^2}{4}+\frac{y^2}{4}")
        s=self.math_step("PASO 1","IDENTIFICAR EJE Y VÉRTICE",[r"z\ge0",r"z=0\Leftrightarrow x=y=0"],["z es la variable lineal: marca el eje de apertura; el origen es el vértice."])
        t=self.term_panel([(r"z","variable lineal"),(r"+x^2,+y^2","misma curvatura"),(r"V=(0,0,0)","vértice")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_elliptic_paraboloid(ax,s)
        self.fade_to_outro(); self.outro("paraboloide elíptico",["Identifique la variable que aparece linealmente.","Determine el vértice y la dirección de apertura.","Fije z=k y calcule el radio de cada corte horizontal.","Use x=0 y y=0 para obtener parábolas verticales.","Conecte las trazas para formar la copa completa."])
