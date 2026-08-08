from individual_base import *

class VC05HyperboloidTwoSheets(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 05","HIPERBOLOIDE DE DOS HOJAS",r"Construcción de $z^2/4-x^2/4-y^2/4=1$","No existencia central → umbral → dos familias separadas")
        self.make_header(1,"HIPERBOLOIDE DE DOS HOJAS: DOS RAMAS DESCONECTADAS","El término positivo aislado determina el eje; antes de dibujar debemos demostrar dónde comienzan a existir puntos reales.")
        f=self.formula_panel(r"\frac{z^2}{4}-\frac{x^2}{4}-\frac{y^2}{4}=1")
        s=self.math_step("PASO 1","LEER LOS SIGNOS",[r"+z^2,-x^2,-y^2",r"z\ \text{es el eje de las hojas}"],["Un término positivo aislado y dos negativos indican dos componentes separadas."])
        t=self.term_panel([(r"+,-,-","patrón de signos"),(r"|z|\ge2","zona de existencia"),(r"z","eje principal")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_two_sheet_hyperboloid(ax,s)
        self.fade_to_outro(); self.outro("hiperboloide de dos hojas",["Identifique el término positivo aislado.","Pruebe z=0 y demuestre que no hay puntos reales.","Obtenga el umbral |z|≥2.","Construya cortes z=±k por encima del umbral.","Use una hipérbola vertical para confirmar las dos ramas."])
