# main.py 
#main se supone ya funcional posiblemente haya errores de posicion o otras cosas
import pygame
import sys
from menu import Menu
from puntuacion import Puntuacion
from config import ANCHO, ALTO  # Importar aquí

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Escapa del Laberinto")
puntuacion = Puntuacion()

menu = Menu(screen, puntuacion)
resultado = menu.run()

if resultado:
     # todo: Aquí integra el juego completo, e.g., from juego import Juego; Juego(modo, dif, nombre, screen, puntuacion).run()
    modo, dif, nombre = resultado
    print(f"Iniciando {modo} en {dif} con jugador {nombre}")
   
else:
    print("Saliendo...")

pygame.quit()
sys.exit()