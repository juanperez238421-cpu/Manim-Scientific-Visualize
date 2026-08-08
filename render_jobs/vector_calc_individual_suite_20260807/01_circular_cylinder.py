from individual_base import *

class VC01CircularCylinder(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 01","CILINDRO CIRCULAR",r"Construcción completa de $x^2+y^2=4$","Variable ausente → trazas → generatrices → parametrización")
        self.make_header(1,"CILINDRO CIRCULAR: DE LA ECUACIÓN 2D A LA SUPERFICIE 3D","La clave no es memorizar la figura: es reconocer que z no aparece y por tanto queda completamente libre.")
        f=self.formula_panel(r"x^2+y^2=4")
        s=self.math_step("PASO 1","RECONOCER LA CURVA BASE",[r"x^2+y^2=2^2",r"z=0\Rightarrow x^2+y^2=4"],["En el plano xy aparece un círculo centrado en el origen y de radio 2."])
        t=self.term_panel([(r"x^2+y^2","distancia radial"),(r"4=2^2","radio al cuadrado"),(r"z","variable ausente")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        self.build_circular_cylinder(ax,s)
        self.fade_to_outro(); self.outro("cilindro circular",["Identifique la variable ausente: z.","Dibuje la curva generatriz x²+y²=4.","Repita la curva para varios planos z=k.","Una puntos correspondientes con generatrices paralelas a z.","Parametrice y complete el barrido continuo."])
