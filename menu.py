#archivo de menu.py
#primero los import's
#por ahora no funciona nada por estar incompleto
import pygame 
import sys
from puntuacion import Puntuacion #se importa de puntuacion la tabla de puntacion
from config import ANCHO, ALTO, FPS, COLORES # se usa para importar valores como la altura,ancho colores y mas
class Menu:
    def __init__(self, screen, puntuacion): #definicion de la pantalla principal del menu 
      pass
        
    def _definir_rects(self):#definicion de las posciones de las opciones del menu 
      pass
    
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