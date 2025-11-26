# entidades.py 
import pygame
from config import TAM_CELDA, COLORES_JUEGO #importa variables desde config


class Terreno: #clse que define el terreno base y las celdas al llamar a config
    def __init__(self, tipo):
        self.tipo = tipo

    def es_accesible_jugador(self):
        return False

    def es_accesible_enemigo(self):
        return False

    def dibujar(self, screen, fila, col):
        rect = pygame.Rect(col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(screen, COLORES_JUEGO[self.tipo], rect)
#define interacciones de entidades con el mapa en las siguiente clase
class Camino(Terreno):
    def __init__(self):
        super().__init__('camino')

    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return True 