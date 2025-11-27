# config.py
# Constantes compartidas para todo el proyecto

ANCHO = 1280
ALTO = 720
FPS = 60

# Colores (posiblemente se cambien cuando ya vea el menu funcional )
COLORES = {
    'bg_dark': (5, 15, 40),
    'bg_panel': (20, 40, 80),
    'bg_button': (40, 80, 140),
    'bg_button_hover': (60, 100, 160),
    'bg_button_selected': (0, 200, 255),
    'text_white': (255, 255, 255),
    'text_yellow': (255, 255, 150),
    'border': (100, 150, 255),
    'input_bg': (60, 60, 80),
    'moon': (0, 220, 255)
}

# Tamaño del mapa y celdas (para después, en mapa.py y entidades.py)
FILAS_MAPA = 15
COLUMNAS_MAPA = 15
TAM_CELDA = 40

# Colores del juego para las futuras entidades y celdas
COLORES_JUEGO = {
    'camino': (200, 200, 200),
    'liana': (50, 205, 50),
    'tunel': (0, 0, 139),
    'muro': (0, 0, 0),
    'jugador': (255, 255, 0),
    'enemigo': (255, 165, 0),
    'salida': (0, 255, 0),
    'trampa': (255, 0, 0)
}
# Archivos highscores
ARCHIVOS_HIGHSCORES = {
    'escapa': 'highscores_escapa.json',
    'cazador': 'highscores_cazador.json'
}