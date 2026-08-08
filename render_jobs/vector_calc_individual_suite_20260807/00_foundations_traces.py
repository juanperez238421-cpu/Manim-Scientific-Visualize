from individual_base import *

class VC00FoundationsTraces(IndividualLessonBase):
    def construct(self):
        self.intro("CÁLCULO VECTORIAL · MICROCLASE 00","SUPERFICIES Y TRAZAS EN R³","Cómo leer una ecuación antes de intentar dibujarla","Punto → restricción → plano de corte → curva → superficie")
        self.make_header(1,"¿QUÉ ES UNA SUPERFICIE?","Una ecuación en x, y, z selecciona todos los puntos del espacio que cumplen simultáneamente una condición.")
        f=self.formula_panel(r"F(x,y,z)=0",title="FORMA IMPLÍCITA")
        s=self.math_step("IDEA 1","CONJUNTO DE NIVEL",[r"S=\{(x,y,z)\in\mathbb R^3:F(x,y,z)=0\}"],["La ecuación representa una colección continua de puntos en el espacio."])
        t=self.term_panel([(r"x,y,z","coordenadas"),(r"F","relación algebraica"),(r"F=0","condición geométrica")])
        self.paced_play(FadeIn(f),FadeIn(s),FadeIn(t),pause=2.0)
        self.set_stable_camera(); ax=self.axes3d(); lab=self.axis_labels(ax); self.paced_play(Create(ax),FadeIn(lab),run_time=1.2,pause=1.2)
        surf=Surface(lambda u,v:ax.c2p(3*np.sin(v)*np.cos(u),2*np.sin(v)*np.sin(u),1.7*np.cos(v)),u_range=[0,TAU],v_range=[0,PI],resolution=(32,20)); self.style_surface(surf,0.24)
        self.paced_play(FadeIn(surf),run_time=1.4,pause=1.5)
        s2=self.math_step("IDEA 2","TRAZA HORIZONTAL",[r"z=k",r"F(x,y,k)=0"],["Fijar z reduce el problema 3D a una curva 2D en un plano horizontal."]); s=self.replace_fixed_panel(s,s2,1.7)
        for k in [-1.0,0,1.0]:
            q=max(0,1-(k/1.7)**2); a=3*np.sqrt(q); b=2*np.sqrt(q)
            c=self.trace_curve(ax,lambda th,k=k,a=a,b=b:np.array([a*np.cos(th),b*np.sin(th),k]),width=2.4)
            self.paced_play(Create(c),run_time=0.9,pause=0.9)
        s3=self.math_step("IDEA 3","TRAZAS VERTICALES",[r"x=k\quad\text{o}\quad y=k"],["Tres familias de cortes permiten reconstruir la forma sin verla completa."]); s=self.replace_fixed_panel(s,s3,1.7)
        yz=self.trace_curve(ax,lambda th:np.array([0,2*np.cos(th),1.7*np.sin(th)]),width=2.7); xz=self.trace_curve(ax,lambda th:np.array([3*np.cos(th),0,1.7*np.sin(th)]),width=2.7)
        self.paced_play(Create(yz),run_time=1.0,pause=0.8); self.paced_play(Create(xz),run_time=1.0,pause=1.4)
        s4=self.math_step("IDEA 4","CLASIFICAR ANTES DE GRAFICAR",[r"\text{variable ausente}\Rightarrow\text{cilindro}",r"\text{cuadrados + signos}\Rightarrow\text{cuádrica}"],["La gráfica debe confirmar una clasificación algebraica previa."]); self.replace_fixed_panel(s,s4,2.0)
        self.fade_to_outro(); self.outro("superficies y trazas",["Escriba la ecuación en una forma reconocible.","Pruebe z=k, x=k y y=k.","Calcule qué curva aparece en cada corte.","Observe cómo cambian tamaño, orientación y existencia.","Solo entonces construya la superficie completa."])
