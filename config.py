# config.py
# Constantes compartidas para todo el proyecto

ANCHO = 1280
ALTO = 720
FPS = 60
HUD_HEIGHT = 50  # Altura de la barra HUD superior en el juego

# Colores del menú
COLORES = {
    'bg_dark': (5, 15, 40),
    'bg_panel': (20, 40, 80),
    'bg_button': (40, 80, 140),
    'bg_button_hover': (60, 100, 160),
    'bg_button_selected': (0, 200, 255),
    'text_white': (255, 255, 255),
    'text_yellow': (255, 255, 0),
    'border': (100, 150, 255),
    'input_bg': (60, 60, 80),
}

# Tamaño del mapa y celdas (para después, en mapa.py y entidades.py)
FILAS_MAPA = 15
COLUMNAS_MAPA = 15
TAM_CELDA = 40

# Colores del juego mejorados según tu imagen
COLORES_JUEGO = {
    'camino': (180, 140, 130),      # Café rojizo claro
    'liana': (50, 205, 50),          # Verde lima (lianas)
    'tunel': (100, 100, 255),        # Azul claro (túneles)
    'muro': (80, 80, 80),            # Gris oscuro (muros)
    'jugador': (0, 150, 255),        # Azul (jugador)
    'enemigo': (255, 50, 50),        # Rojo (enemigos)
    'salida': (255, 255, 0),         # Amarillo (salida)
    'trampa': (200, 0, 200)          # Morado (trampas)
}
# Archivos highscores
ARCHIVOS_HIGHSCORES = {
    'escapa': 'highscores_escapa.json',
    'cazador': 'highscores_cazador.json'
}