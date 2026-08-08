from individual_base import *

class VC06EllipticCone(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 06","CONO ELÍPTICO",r"Construcción de $z^2-x^2-y^2=0$","Vértice → radio proporcional a |z| → generatrices")
        self.make_header(1,"CONO: CUÁDRICA IGUALADA A CERO","El cono comparte el patrón de signos de un hiperboloide, pero al igualarse a cero las dos partes se encuentran en un vértice.")
        f=self.formula_panel(r"z^2-x^2-y^2=0")
        s=self.math_step("PASO 1","REORDENAR",[r"z^2=x^2+y^2",r"r^2=x^2+y^2\Rightarrow r=|z|"],["El radio de cada sección horizontal es exactamente la distancia vertical al vértice."])
        t=self.term_panel([(r"z^2","altura al cuadrado"),(r"x^2+y^2","radio al cuadrado"),(r"=0","encuentro en el vértice")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_cone(ax,s)
        self.fade_to_outro(); self.outro("cono elíptico",["Reescriba la ecuación como radio² = altura².","Localice el vértice en el origen.","Construya z=±k y compruebe r=|k|.","Dibuje trazas verticales: rectas por el vértice.","Rote las generatrices para completar ambas nappes."])
