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
    # Asegúrate de que este archivo exista en la carpeta 'assets'
    pygame.mixer.music.load('assets/musicadefondojuego.mp3') 
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle infinito
except pygame.error:
    print("No se pudo cargar la música de fondo. Verifica la ruta 'assets/musicadefondojuego.mp3'")
except Exception as e:
    print(f"Error desconocido al cargar música: {e}")

# Loop principal del juego
while True:
    menu = Menu(screen, puntuacion)
    # Ejecuta el menú, devuelve (modo, dificultad, nombre) o None si sale.
    resultado = menu.run()

    if resultado:
        # Iniciar el juego con los parámetros 
        modo, dif, nombre = resultado
        print(f"Iniciando {modo} en {dif} con jugador {nombre}")
        
        # Crear y ejecutar el juego
        juego = Juego(modo, dif, nombre, screen, puntuacion)
        # El método .run() de Juego devuelve True si el usuario seleccionó "Salir al Menu" desde la pausa
        volver_menu = juego.run() 
        
        if volver_menu:
            print("Volviendo al menú por solicitud del usuario...")
        else:
            # Si el juego terminó (victoria, derrota o tiempo agotado)
            print(f"Juego terminado. Volviendo al menú.")
            
    else:
        # Si el menú devuelve None (por ejemplo, el usuario cerró la ventana)
        pygame.quit()
        sys.exit()