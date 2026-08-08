from individual_base import *

class VC09ClassificationWorkshop(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 09","TALLER DE CLASIFICACIÓN",r"De ecuaciones generales a superficies reconocibles","Completar cuadrados → normalizar → signos → trazas → conclusión")
        self.make_header(1,"EJEMPLO A: ESFERA DESPLAZADA","Una ecuación general no debe clasificarse por intuición; primero hay que llevarla a una forma canónica.")
        f=self.formula_panel(r"x^2+y^2+z^2-4x+2y-6z=2")
        s=self.math_step("PASO 1","AGRUPAR",[r"(x^2-4x)+(y^2+2y)+(z^2-6z)=2"],["Cada grupo se completa como un cuadrado perfecto."])
        t=self.term_panel([(r"x^2-4x","(x-2)^2-4"),(r"y^2+2y","(y+1)^2-1"),(r"z^2-6z","(z-3)^2-9")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        s2=self.math_step("PASO 2","COMPLETAR CUADRADOS",[r"(x-2)^2-4+(y+1)^2-1+(z-3)^2-9=2",r"(x-2)^2+(y+1)^2+(z-3)^2=16"],["Tres cuadrados positivos con el mismo denominador: esfera de radio 4."]); s=self.replace_fixed_panel(s,s2,2.5)
        s3=self.math_step("PASO 3","INTERPRETAR",[r"C=(2,-1,3)",r"R=4"],["La forma canónica entrega centro, radio y familia geométrica directamente."]); self.replace_fixed_panel(s,s3,2.5)
        self.fade_to_outro()
        self.make_header(2,"EJEMPLO B: PARABOLOIDE DESPLAZADO","La posición cambia, pero la estructura algebraica permite reconocer la misma familia.")
        f=self.formula_panel(r"z=4-\frac{x^2}{4}-y^2")
        s=self.math_step("PASO 1","AISLAR LOS CUADRADOS",[r"4-z=\frac{x^2}{4}+y^2"],["El lado derecho es no negativo: necesariamente z≤4."])
        t=self.term_panel([(r"z=4","altura máxima"),(r"V=(0,0,4)","vértice"),(r"-x^2,-y^2","abre hacia −z")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        s2=self.math_step("PASO 2","TRAZA HORIZONTAL",[r"z=k",r"\frac{x^2}{4}+y^2=4-k"],["Para k<4 aparecen elipses; al acercarse k a 4 se contraen al vértice."]); s=self.replace_fixed_panel(s,s2,2.5)
        s3=self.math_step("PASO 3","CONCLUSIÓN",[r"\text{paraboloide elíptico}",r"V=(0,0,4)",r"\text{apertura }-z"],["Una clasificación completa incluye tipo, posición, eje y dirección de apertura."]); self.replace_fixed_panel(s,s3,2.5)
        self.fade_to_outro(); self.outro("clasificación",["Agrupe términos por variable.","Complete cuadrados cuando haya términos lineales.","Normalice la ecuación a =1 o =0 cuando corresponda.","Lea cuadrados, signos y variables ausentes o lineales.","Confirme la familia mediante una o más trazas."])
