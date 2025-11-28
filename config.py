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

# Tamaño del mapa - Ajustado para pantalla completa
FILAS_MAPA = 16
COLUMNAS_MAPA = 30
TAM_CELDA = 40

# Colores del juego mejorados
COLORES_JUEGO = {
    'camino': (180, 140, 130),      # Café rojizo claro
    'liana': (50, 150, 50),         # 🟢 Verde oscuro para Lianas (Accesible solo a Cazadores)
    'tunel': (100, 100, 100),       # ⚪ Gris para Túneles (Accesible solo al Jugador/Presa)
    'muro': (40, 40, 40),           # ⬛ Gris muy oscuro para Muros
    'trampa': (255, 69, 0),         # 🟠 Naranja brillante
    'jugador': (0, 0, 255),         # 🔵 Azul
    'enemigo': (255, 0, 0),         # 🔴 Rojo
    'inicio': (0, 255, 0),          # 🟢 Verde
    'salida': (255, 255, 0)         # 🟡 Amarillo
}
# Archivos highscores
ARCHIVOS_HIGHSCORES = {
    'escapa': 'highscores_escapa.json',
    'cazador': 'highscores_cazador.json'
}