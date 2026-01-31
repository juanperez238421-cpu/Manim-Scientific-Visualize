from manim import *

# =================================================================
# CONFIGURACIÓN DE ESTILO PARA SOFTWARE
# =================================================================
SOFT_THEME = {
    "uml_header": "#222222",
    "uml_body": "#f4f4f4",
    "node_fill": "#ffffff",
    "pointer_color": "#2979ff", # Azul para punteros/referencias
    "data_color": "#000000",
    "stroke_width": 2
}

# =================================================================
# MOTOR DE DIAGRAMAS UML
# =================================================================

def make_uml_class(name, attributes=None, methods=None, width=4.5):
    """
    Crea una tarjeta de clase UML con secciones dinámicas.
    Ajusta automáticamente la altura según la cantidad de miembros.
    """
    attributes = attributes or []
    methods = methods or []
    
    # Título (Header)
    title_text = Text(name, color=WHITE, weight=BOLD).scale(0.4)
    header_bg = Rectangle(
        width=width, height=0.6, 
        fill_color=SOFT_THEME["uml_header"], fill_opacity=1, 
        stroke_width=SOFT_THEME["stroke_width"]
    )
    header = VGroup(header_bg, title_text)
    
    # Atributos y Métodos
    attr_group = VGroup(*[Text(f" - {a}", color=BLACK).scale(0.35) for a in attributes])
    meth_group = VGroup(*[Text(f" + {m}()", color=BLACK).scale(0.35) for m in methods])
    
    for g in [attr_group, meth_group]:
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    
    # Cuerpo
    content = VGroup(attr_group, Line(width=width), meth_group).arrange(DOWN, buff=0.2)
    body_bg = RoundedRectangle(
        corner_radius=0.1, width=width, height=content.height + 0.5,
        fill_color=SOFT_THEME["uml_body"], fill_opacity=1, 
        stroke_color=BLACK, stroke_width=SOFT_THEME["stroke_width"]
    )
    
    content.move_to(body_bg.get_center())
    full_class = VGroup(body_bg, header.next_to(body_bg, UP, buff=0), content)
    
    return full_class

# =================================================================
# VISUALIZADORES DE ESTRUCTURAS DE DATOS
# =================================================================

def make_node_box(data_text, pointer_label="next", width=3.0):
    """
    Crea un nodo de estructura de datos (Pila/Cola/Lista) 
    dividido en campos de 'dato' y 'puntero'.
    """
    h = 1.0
    outer = Rectangle(width=width, height=h*2, color=BLACK, stroke_width=SOFT_THEME["stroke_width"])
    divider = Line(outer.get_left() + UP*0, outer.get_right() + UP*0)
    
    val_txt = Text(str(data_text), color=SOFT_THEME["data_color"]).scale(0.5)
    val_txt.move_to(outer.get_center() + UP*(h/2))
    
    ptr_txt = Text(pointer_label, color=SOFT_THEME["pointer_color"], slant=ITALIC).scale(0.4)
    ptr_txt.move_to(outer.get_center() + DOWN*(h/2))
    
    return VGroup(outer, divider, val_txt, ptr_txt)

def make_pointer_arrow(source_mobj, target_mobj, label=None):
    """
    Crea una flecha de puntero con estilo profesional entre dos objetos.
    """
    arrow = Arrow(
        source_mobj.get_right(), 
        target_mobj.get_left(), 
        buff=0.1, 
        color=SOFT_THEME["pointer_color"],
        stroke_width=3,
        max_tip_length_to_length_ratio=0.15
    )
    if label:
        arrow_label = Text(label, color=SOFT_THEME["pointer_color"]).scale(0.3).next_to(arrow, UP, buff=0.1)
        return VGroup(arrow, arrow_label)
    return arrow

# =================================================================
# MEMORIA Y GESTIÓN DE RECURSOS
# =================================================================

def make_memory_cell(address, value="", color=WHITE):
    """
    Representa una celda de memoria con su dirección física.
    """
    cell = Square(side_length=1.0, color=BLACK, fill_color=color, fill_opacity=0.5)
    addr_txt = Text(address, color=GRAY).scale(0.3).next_to(cell, DOWN, buff=0.1)
    val_txt = Text(str(value), color=BLACK, weight=BOLD).scale(0.5).move_to(cell.get_center())
    
    return VGroup(cell, addr_txt, val_txt)