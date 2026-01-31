from manim import *
import numpy as np

# =================================================================
# CONFIGURACIÓN DE ESTILO PARA INGENIERÍA
# =================================================================
ENG_THEME = {
    "force_color": "#ff5252",    # Rojo para cargas y fuerzas
    "reaction_color": "#2979ff", # Azul para reacciones
    "beam_color": "#000000",
    "velocity_color": "#4caf50", # Verde para flujos/fluidos
    "stroke_width": 4
}

# =================================================================
# DINÁMICA DE FLUIDOS (INVESTIGACIÓN PIV)
# =================================================================

def create_piv_streamlines(npy_path: str, density=2.0, stroke_width=2):
    """
    Genera líneas de corriente animadas a partir de un campo de velocidades 
    experimental (Particle Image Velocimetry) cargado desde un archivo .npy.
    Ideal para visualización de Turbinas de Vórtice Gravitacional (GWVT).
    """
    try:
        # El archivo .npy debe contener un array de (ny, nx, 2)
        vel_field = np.load(npy_path)
        ny, nx, _ = vel_field.shape

        def field_func(p):
            x, y = p[:2]
            # Mapeo de coordenadas de Manim (-config.frame_width/2 a +config.frame_width/2)
            # a índices de la matriz de datos
            ix = int(np.clip((x / config.frame_width + 0.5) * (nx - 1), 0, nx - 1))
            iy = int(np.clip((y / config.frame_height + 0.5) * (ny - 1), 0, ny - 1))
            
            u, v = vel_field[iy, ix]
            return np.array([u, v, 0])

        return StreamLines(
            field_func,
            stroke_width=stroke_width,
            color=ENG_THEME["velocity_color"],
            virtual_time=3,
            max_anchors_per_line=30,
            padding=1
        )
    except Exception as e:
        return Text(f"Error loading PIV data: {str(e)}", color=RED).scale(0.5)

# =================================================================
# INGENIERÍA ESTRUCTURAL (VIGAS Y DIAGRAMAS)
# =================================================================

def draw_point_load(position_point, magnitude, label_text=None, direction=DOWN):
    """
    Dibuja una flecha de carga puntual con etiqueta de magnitud.
    """
    start = position_point + (direction * -1.5)
    end = position_point
    arrow = Arrow(start, end, buff=0, color=ENG_THEME["force_color"], stroke_width=5)
    
    if label_text:
        label = MathTex(label_text, color=ENG_THEME["force_color"]).scale(0.6)
        label.next_to(start, direction * -1, buff=0.1)
        return VGroup(arrow, label)
    return arrow

def make_beam_support(point, type="pin"):
    """
    Crea apoyos de ingeniería: 'pin' (triángulo) o 'roller' (círculo).
    """
    if type == "pin":
        support = Triangle(color=ENG_THEME["reaction_color"], fill_opacity=1).scale(0.2)
        support.next_to(point, DOWN, buff=0)
    else:
        support = Circle(color=ENG_THEME["reaction_color"], fill_opacity=1).scale(0.12)
        support.next_to(point, DOWN, buff=0.05)
    return support

# =================================================================
# ESTÁTICA Y MECÁNICA VECTORIAL (3D)
# =================================================================

def create_3d_force_vector(axes, start_coords, vector_vals, color=RED):
    """
    Crea un vector de fuerza en el espacio 3D basado en coordenadas de ejes.
    """
    start = axes.c2p(*start_coords)
    end = axes.c2p(*(np.array(start_coords) + np.array(vector_vals)))
    
    # Arrow3D no existe nativamente en todas las versiones, se usa Line + Tip
    arrow = Arrow(start, end, color=color, buff=0, stroke_width=4)
    return arrow

def make_dimension_line(start, end, text, offset=UP*0.5, color=GRAY_D):
    """
    Crea una línea de cota con flechas en ambos extremos y etiqueta de medida.
    """
    line = DoubleArrow(start, end, buff=0, color=color, tip_length=0.15, stroke_width=2)
    line.shift(offset)
    label = Text(text, color=color).scale(0.35).next_to(line, UP, buff=0.05)
    return VGroup(line, label)