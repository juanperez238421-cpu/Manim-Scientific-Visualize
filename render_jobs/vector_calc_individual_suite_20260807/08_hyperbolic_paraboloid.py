from individual_base import *

class VC08HyperbolicParaboloid(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 08","PARABOLOIDE HIPERBÓLICO",r"Construcción de $z=(x^2-y^2)/4$","Rectas centrales → parábolas opuestas → hipérbolas horizontales")
        self.make_header(1,"PARABOLOIDE HIPERBÓLICO: LA SILLA","Los cuadrados tienen signos opuestos: una dirección se curva hacia arriba y la perpendicular hacia abajo.")
        f=self.formula_panel(r"z=\frac{x^2}{4}-\frac{y^2}{4}")
        s=self.math_step("PASO 1","LEER LOS SIGNOS",[r"+x^2,-y^2",r"z\ \text{es lineal}"],["Los signos opuestos generan curvaturas opuestas alrededor del punto silla."])
        t=self.term_panel([(r"+x^2","sube en x"),(r"-y^2","baja en y"),(r"(0,0,0)","punto silla")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_hyperbolic_paraboloid(ax,s)
        self.fade_to_outro(); self.outro("paraboloide hiperbólico",["Identifique la variable lineal y los cuadrados con signos opuestos.","Use z=0 para obtener las rectas y=±x.","Use y=0 y x=0 para ver parábolas opuestas.","Construya z=±k y observe hipérbolas con orientación alternante.","Una todas las trazas para reconocer la geometría de silla."])
