# main.py 
import pygame
import sys
from menu import Menu
from juego import Juego  
from puntuacion import Puntuacion
from config import ANCHO, ALTO

pygame.init()
pygame.mixer.init()  # Inicializar mixer para audio
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Escapa del Laberinto")
puntuacion = Puntuacion()

# Cargar y reproducir música de fondo en bucle
try:
    pygame.mixer.music.load('assets/musicadefondojuego.mp3')
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle infinito
except:
    print("No se pudo cargar la música de fondo")

# Loop principal del juego
while True:
    menu = Menu(screen, puntuacion)
    resultado = menu.run()

    if resultado:
        # Iniciar el juego con los parámetros 
        modo, dif, nombre = resultado
        print(f"Iniciando {modo} en {dif} con jugador {nombre}")
        
        # Crear y ejecutar el juego
        juego = Juego(modo, dif, nombre, screen, puntuacion)
        volver_menu = juego.run()
        
        # Si volver_menu es True, continúa al menú
        # Si es False, el juego terminó normalmente
        if volver_menu:
            print("Volviendo al menú...")
        else:
            print("Juego terminado, volviendo al menú...")
    else:
        # El usuario eligió salir
        print("Saliendo...")
        break

pygame.quit()
sys.exit()