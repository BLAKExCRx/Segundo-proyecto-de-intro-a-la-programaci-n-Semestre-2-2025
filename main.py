# main.py (actualizado: importar ANCHO, ALTO de config)
import pygame
import sys
from menu import Menu
#from puntuacion import Puntuacion #se usara para importar los valores de la tabla de puntuacion al menu  junto a un valor de puntuacion que no se crea todavia
from config import ANCHO, ALTO  # Importar las configuraciones 

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Escapa del Laberinto")
#puntuacion = Puntuacion()

#menu = Menu(screen, puntuacion)
#resultado = menu.run()

#pendiente de seguir avanzando 
pygame.quit()
sys.exit()