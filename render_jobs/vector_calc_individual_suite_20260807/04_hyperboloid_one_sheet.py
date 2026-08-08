from individual_base import *

class VC04HyperboloidOneSheet(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 04","HIPERBOLOIDE DE UNA HOJA",r"Construcción de $x^2/4+y^2/2-z^2/4=1$","Signos → cintura → elipses crecientes → hipérbola vertical")
        self.make_header(1,"HIPERBOLOIDE DE UNA HOJA: SUPERFICIE CONECTADA","Dos cuadrados positivos y uno negativo igualados a 1 generan una cintura elíptica y apertura en la dirección del signo diferente.")
        f=self.formula_panel(r"\frac{x^2}{4}+\frac{y^2}{2}-\frac{z^2}{4}=1")
        s=self.math_step("PASO 1","LEER LOS SIGNOS",[r"+x^2,+y^2,-z^2",r"z\ \text{es el eje característico}"],["El término con signo diferente indica la dirección en la que la superficie se ensancha."])
        t=self.term_panel([(r"+,+,-","patrón de signos"),(r"z=0","cintura"),(r"-z^2/4","eje de apertura")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_hyperboloid_one_sheet(ax,s)
        self.fade_to_outro(); self.outro("hiperboloide de una hoja",["Identifique el único término cuadrado con signo diferente.","Use z=0 para encontrar la cintura elíptica.","Calcule z=±k y muestre que las elipses aumentan.","Use una traza vertical para revelar la hipérbola.","Una las familias de trazas en una superficie conectada."])
