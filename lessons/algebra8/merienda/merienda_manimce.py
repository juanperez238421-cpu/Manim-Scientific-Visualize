"""Proyecto educativo de fracciones algebraicas - motor nativo ManimCE.
15 capítulos, voz española sintetizada por capítulo, animaciones vectoriales.
"""
from manim import *
from pathlib import Path
import math, subprocess, wave, sys

ROOT=Path(__file__).resolve().parent
AUDIO=ROOT/"audio"
BG="#091225"; PANEL="#152542"; WHITE="#F3F6FF"
SKY="#75D5FF"; GOLD="#FFD16A"; ROSE="#FF809D"; MINT="#63EAC2"; MUTED="#B9C5DA"
# Cada capítulo: título, concepto clave, fórmula original verificable, narración
CHAPTERS=[
("¿ALCANZA PARA LA MERIENDA?","La vida cotidiana se puede modelar con álgebra.",
 r"\frac{\mathrm{GASTO}}{\mathrm{PRESUPUESTO}}",
 "Imagina una tarde de viernes. Un grupo de estudiantes compra pizza y bebidas. También tienen un presupuesto, pero ocurre un imprevisto. Cuando cambia la cantidad de personas que participan en cada compra, la distribución del dinero deja de ser tan sencilla. Hoy resolveremos este problema con fracciones complejas algebraicas, paso por paso."),
("DOS GRUPOS DIFERENTES","x representa el tamaño de un grupo de referencia.",
 r"\mathrm{Compra\ A}:\ x+1\qquad\mathrm{Compra\ B}:\ x-1",
 "Llamemos equis al número de estudiantes del grupo de referencia. Para la primera compra participa una persona más, por eso escribimos equis más uno. En la segunda compra participa una persona menos, por eso escribimos equis menos uno. Una estudiante participa en ambas compras. Vamos a calcular cuánto debe pagar y cuánto dinero tiene disponible."),
("PIZZA + BEBIDAS","El gasto total es una suma de fracciones.",
 r"G(x)=\frac{12}{x+1}+\frac{8}{x-1}",
 "La pizza cuesta doce mil pesos y la pagan entre equis más uno personas. Entonces a cada una le corresponde doce sobre equis más uno, medido en miles de pesos. Las bebidas cuestan ocho mil pesos y se dividen entre equis menos uno personas. Nuestra estudiante participa en ambas compras, así que sumamos los dos gastos individuales."),
("FONDO - IMPREVISTO","El presupuesto neto es una resta.",
 r"B(x)=\frac{30}{x+1}-\frac{5}{x-1}",
 "Ahora analicemos el presupuesto. Un fondo de treinta mil pesos se distribuye entre equis más uno estudiantes. Sin embargo, ocurre un gasto imprevisto de cinco mil pesos, repartido entre equis menos uno participantes. A cada estudiante le queda su parte del fondo menos su parte del gasto inesperado. Así aparece una resta entre fracciones algebraicas."),
("UNA FRACCIÓN DENTRO DE OTRA","Razón de gasto a presupuesto disponible.",
 r"R(x)=\frac{\dfrac{12}{x+1}+\dfrac{8}{x-1}}{\dfrac{30}{x+1}-\dfrac{5}{x-1}}",
 "Para saber si el dinero alcanza, debemos dividir el gasto individual entre el presupuesto neto individual. En el numerador aparece una suma; en el denominador, una resta. Esta estructura es una fracción compleja algebraica. Cuando la razón supera uno, gastamos más de lo disponible. Si es igual a uno, el dinero alcanza exactamente; y si es menor que uno, queda un excedente."),
("DOMINIO Y RESTRICCIONES","No podemos dividir entre cero.",
 r"x\neq-1,\quad x\neq1,\quad x\neq\frac75",
 "Antes de resolver la expresión, examinamos las restricciones. Equis más uno nunca puede ser cero, de modo que equis no puede valer menos uno. Equis menos uno tampoco puede ser cero, así que excluimos el uno. Además, el presupuesto neto no puede ser cero: eso sucede en siete quintos. En nuestra situación real, equis es un número entero de personas, mayor o igual que dos."),
("UN DENOMINADOR COMÚN","La diferencia de cuadrados crea un mismo denominador.",
 r"D=(x+1)(x-1)=x^2-1",
 "Para sumar o restar dos fracciones algebraicas necesitamos denominadores iguales. Usaremos el producto de equis más uno por equis menos uno, que también se expresa como equis al cuadrado menos uno. Multiplicamos arriba y abajo por el factor que hace falta. Hacemos esto por separado tanto en la suma del gasto como en la resta del presupuesto."),
("SIMPLIFICAMOS EL GASTO","Distributiva y reducción de términos semejantes.",
 r"\frac{12(x-1)+8(x+1)}D=\frac{20x-4}D",
 "Comencemos por el gasto. Multiplicamos doce por equis menos uno, lo que da doce equis menos doce. Sumamos ocho por equis más uno, obteniendo ocho equis más ocho. Agrupamos los términos semejantes: doce equis más ocho equis son veinte equis. Menos doce más ocho son menos cuatro. El resultado es veinte equis menos cuatro dividido por el denominador común."),
("SIMPLIFICAMOS EL PRESUPUESTO","El signo negativo afecta a todo el paréntesis.",
 r"\frac{30(x-1)-5(x+1)}D=\frac{25x-35}D",
 "Ahora el presupuesto. Multiplicamos treinta por equis menos uno, obteniendo treinta equis menos treinta. Después restamos cinco por equis más uno, lo que equivale a menos cinco equis menos cinco. Es importante distribuir el signo menos entre ambos términos. Finalmente agrupamos: treinta equis menos cinco equis son veinticinco equis, y menos treinta menos cinco son menos treinta y cinco."),
("DIVIDIR ES MULTIPLICAR POR EL RECÍPROCO","Ley de medios y extremos.",
 r"\frac{\dfrac{20x-4}D}{\dfrac{25x-35}D}=\frac{20x-4}D\cdot\frac D{25x-35}",
 "Ya hemos simplificado las fracciones internas. Ahora aplicamos la división de fracciones: multiplicar la primera fracción por el recíproco de la segunda. En nuestro caso, el denominador común aparece multiplicando arriba y abajo. Podemos cancelar ese factor porque hemos comprobado que no puede ser cero dentro del dominio válido."),
("RESULTADO ALGEBRAICO GENERAL","Sin factores comunes adicionales.",
 r"\boxed{R(x)=\frac{20x-4}{25x-35}}",
 "Después de cancelar correctamente el denominador común, obtenemos una expresión muy sencilla. La razón es veinte equis menos cuatro, dividido por veinticinco equis menos treinta y cinco. También es posible factorizar el numerador y el denominador, pero no aparece ningún factor común que pueda cancelarse. Conservamos las restricciones originales de la expresión."),
("PROBAMOS CON EQUIS IGUAL A CINCO","Pizza y bebidas: 4.000 pesos por estudiante.",
 r"G(5)=\frac{12}{6}+\frac84=4",
 "Probemos el modelo con equis igual a cinco. La pizza se comparte entre seis estudiantes, así que cada uno paga dos mil pesos. Las bebidas se comparten entre cuatro estudiantes; cada uno paga otros dos mil. El gasto total de nuestra estudiante es de cuatro mil pesos. Ahora evaluemos el dinero que efectivamente tiene disponible."),
("¿CUÁNTO DINERO FALTA?","Presupuesto: 3.750 pesos. Faltan 250.",
 r"B(5)=\frac{30}6-\frac54=3.75",
 "Del fondo inicial corresponden cinco mil pesos por persona. El gasto imprevisto es de mil doscientos cincuenta pesos por persona. Así, el presupuesto disponible es tres mil setecientos cincuenta pesos. Sin embargo, debemos gastar cuatro mil pesos. La diferencia es de doscientos cincuenta pesos: esa es la cantidad adicional que necesita nuestra estudiante."),
("LA RESPUESTA Y SU INTERPRETACIÓN","El gasto corresponde al 106,67 % del presupuesto.",
 r"R(5)=\frac4{3.75}=\frac{16}{15}\approx1.0667",
 "Dividimos cuatro mil entre tres mil setecientos cincuenta y obtenemos dieciséis quinceavos. En forma decimal es aproximadamente uno coma cero seis seis siete. Esto significa que el gasto representa ciento seis coma sesenta y siete por ciento del presupuesto. Por tanto, faltan doscientos cincuenta pesos, equivalentes a aproximadamente seis coma sesenta y siete por ciento de lo disponible."),
("COMPROBACIÓN Y CONCLUSIÓN","El álgebra también ayuda a tomar decisiones.",
 r"\frac{20(5)-4}{25(5)-35}=\frac{96}{90}=\frac{16}{15}",
 "Comprobamos el resultado sustituyendo equis igual a cinco en la fórmula simplificada. Obtenemos noventa y seis dividido por noventa, exactamente dieciséis quinceavos, igual que en la expresión original. Aprendimos a modelar una situación real, sumar y restar fracciones, manejar denominadores comunes, aplicar recíprocos y establecer restricciones. Las fracciones también sirven para tomar mejores decisiones financieras cotidianas. Muchas gracias.")
]
def make_audio():
    AUDIO.mkdir(parents=True,exist_ok=True)
    for i,(_,_,_,speech) in enumerate(CHAPTERS):
        outfile=AUDIO/f"voice_{i:02d}.wav"
        subprocess.run(["espeak-ng","-v","es","-s","146","-p","48","-w",str(outfile),speech],check=True)
    print("Audios preparados:",len(CHAPTERS))
def tx(s,size=28,color=WHITE):
    return Text(s,font="DejaVu Sans",font_size=size,color=color)
def fm(s,width=11.8):
    f=MathTex(s,color=WHITE)
    if f.width>width:f.scale_to_fit_width(width)
    return f
def pizza():
    sectors=VGroup()
    for k in range(8):
        sectors.add(Sector(outer_radius=.96,start_angle=k*TAU/8,
            angle=TAU/8-.018,fill_color=GOLD if k%2 else "#FFA95B",
            fill_opacity=1,stroke_color=BG,stroke_width=2))
    sectors.add(Circle(radius=.96,color="#EF8F4C",stroke_width=7))
    return sectors
def cups():
    cup=Polygon([-.45,.62,0],[.45,.62,0],[.33,-.65,0],[-.33,-.65,0],
        fill_color=SKY,fill_opacity=.8,stroke_color=WHITE,stroke_width=2)
    straw=Line([.15,.52,0],[.52,1.01,0],color=ROSE,stroke_width=5)
    return VGroup(cup,straw)
def persons(count=5):
    people=VGroup()
    for k in range(count):
        body=RoundedRectangle(width=.37,height=.48,corner_radius=.10,
            fill_color=MINT,fill_opacity=.85,stroke_width=0)
        head=Circle(radius=.16,fill_color=GOLD,fill_opacity=1,stroke_width=0).next_to(body,UP,buff=.02)
        people.add(VGroup(body,head))
    return people.arrange(RIGHT,buff=.19)
class MeriendaFraccionesAlgebra8(Scene):
    def construct(self):
        self.camera.background_color=BG
        total=len(CHAPTERS)
        for i,(title,explain,latex,_) in enumerate(CHAPTERS):
            t0=self.renderer.time
            header=tx("FRACCIONES · ÁLGEBRA 8°",19,SKY).to_corner(UL,buff=.34)
            index=tx(f"{i+1:02d} / {total:02d}",19,MUTED).to_corner(UR,buff=.34)
            rule=Line(LEFT*6.65+UP*2.92,RIGHT*6.65+UP*2.92,stroke_width=2,color="#314766")
            title_mob=tx(title,36,GOLD)
            if title_mob.width>12.3:title_mob.scale_to_fit_width(12.3)
            title_mob.move_to(UP*2.28)
            expl=tx(explain,24,MUTED)
            if expl.width>12.5:expl.scale_to_fit_width(12.5)
            expl.move_to(DOWN*1.98)
            outer=RoundedRectangle(width=11.9,height=3.15,corner_radius=.22,
                stroke_color="#31527C",stroke_width=2,
                fill_color=PANEL,fill_opacity=.95).move_to(UP*.15)
            math=fm(latex,10.9).scale(1.2)
            if math.width>10.7:math.scale_to_fit_width(10.7)
            math.move_to(UP*.15)
            bottom=tx("INSTITUTO JORGE ROBLEDO  ·  OCTUBRE 2026",17,MUTED).to_edge(DOWN,buff=.18)
            self.add_sound(str(AUDIO/f"voice_{i:02d}.wav"))
            self.play(FadeIn(header),FadeIn(index),Create(rule),run_time=.5)
            self.play(Write(title_mob),run_time=1.3)
            self.play(FadeIn(outer,scale=.97),run_time=.7)
            illustration=VGroup()
            if i in (0,2,11):
                illustration=VGroup(pizza().scale(.70).move_to(LEFT*4.3+UP*.2),
                    cups().scale(.55).move_to(RIGHT*4.4+UP*.2))
            elif i in (1,3):
                illustration=persons(5).scale(.85).move_to(DOWN*.6)
                math.shift(UP*.35)
            elif i==13:
                illustration=VGroup(
                    Rectangle(width=7.0,height=.25,fill_color=MINT,fill_opacity=.9,stroke_width=0),
                    Rectangle(width=.48,height=.25,fill_color=ROSE,fill_opacity=1,stroke_width=0)
                ).arrange(RIGHT,buff=.02).move_to(DOWN*.98)
                math.shift(UP*.50)
            elif i in (7,8,9):
                math.shift(UP*.33)
                illustration=tx("Paso a paso: distribuir → agrupar → simplificar",20,SKY).move_to(DOWN*.92)
            if len(illustration)>0:
                self.play(FadeIn(illustration,shift=UP*.16),run_time=1)
            self.play(Write(math),run_time=1.8)
            self.play(FadeIn(expl),FadeIn(bottom),run_time=.7)
            audio=AUDIO/f"voice_{i:02d}.wav"
            with wave.open(str(audio),"rb") as w:
                seconds=w.getnframes()/w.getframerate()
            elapsed=self.renderer.time-t0
            self.wait(max(1.0,seconds-elapsed+.40))
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.7)
if __name__=="__main__" and "--make-audio" in sys.argv:make_audio()
