#archivo de menu.py
#primero los import's
#por ahora no funciona nada por estar incompleto y los comentarios se actualizan a futuro
import pygame 
import sys
from puntuacion import Puntuacion #se importa de puntuacion la tabla de puntacion
from config import ANCHO, ALTO, FPS, COLORES # se usa para importar valores como la altura,ancho colores y mas
class Menu:
    def __init__(self, screen, puntuacion): #definicion de la pantalla principal del menu 
        self.screen = screen
        self.puntuacion = puntuacion
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('arial', 50, bold=True)
        self.font_subtitle = pygame.font.SysFont('arial', 24, bold=True)
        self.font_button = pygame.font.SysFont('arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
        self.colors = COLORES

         # Fondo
        try:
            self.background = pygame.image.load('fondo_menu.png')
            self.background = pygame.transform.scale(self.background, (ANCHO, ALTO))
        except pygame.error:
            self.background = None
        
        # Estados
        self.state = 'name_input'
        self.nombre = ''
        self.cursor_visible = True
        self.cursor_timer = 0
        self.modo_seleccionado = None
        self.dificultad = 'medio'
        
        self.rects = self._definir_rects()
        
        # Luna
        self.moon_pos = (ANCHO // 2 - 300, 50)
        self.moon_radius = 80
        
    def _definir_rects(self):#definicion de las posciones de las opciones del menu 
        rects = {}
        rects['input_nombre'] = pygame.Rect(ANCHO - 400, 50, 350, 40)
        rects['panel_modos'] = pygame.Rect(50, 200, 300, 250)
        rects['modo_escapa'] = pygame.Rect(55, 210, 290, 50)
        rects['modo_cazador'] = pygame.Rect(55, 270, 290, 50)
        rects['salir'] = pygame.Rect(55, 390, 290, 50)
        
        rects['dificil_facil'] = pygame.Rect(ANCHO // 2 - 75, 150, 150, 50)
        rects['dificil_medio'] = pygame.Rect(ANCHO // 2 + 75, 150, 150, 50)
        rects['dificil_dificil'] = pygame.Rect(ANCHO // 2 + 225, 150, 150, 50)
        
        rects['top_escapa'] = pygame.Rect(ANCHO // 2 - 75, 250, 150, 150)
        rects['top_cazador'] = pygame.Rect(ANCHO // 2 + 125, 250, 150, 150)
        return rects
    
    def handle_events(self, events): #definicion para los eventos o acciones segun el menu
        pass
    
    def _iniciar_juego(self): # definicion para poder iniciar el juego segun el modo de juego y dificultad 
      pass
    
    def update(self, dt): #actualizar constantemente el cursor
        self.cursor_timer += dt
        if self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self):#define los valores de posicion,color y demas del menu 
       pass
    
    def _dibujar_top(self, modo, rect_bg): #dibuja la tabla de puntajes del top de ambos modos
       pass
    def run(self): #funcion para hacer andar el juego ,posiblemente tambien para definir un relog /ticks del juego usando los fps
        pass