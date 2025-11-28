# juego.py
import pygame
import sys
import random
from collections import deque # Necesario para el BFS en encontrar_camino
from config import ANCHO, ALTO, FPS, HUD_HEIGHT, COLORES, TAM_CELDA, COLORES_JUEGO
from mapa import Mapa
# Asegurar la importación de todas las clases necesarias
from entidades import Jugador, Enemigo, Trampa, Camino, Liana, Tunel 
from puntuacion import Puntuacion

class Juego:
    def __init__(self, modo, dificultad, nombre_jugador, screen, puntuacion):
        self.modo = modo
        self.dificultad = dificultad
        self.nombre_jugador = nombre_jugador
        self.screen = screen
        self.puntuacion = puntuacion
        self.clock = pygame.time.Clock()
        self.font_hud = pygame.font.SysFont('arial', 18, bold=True)
        self.font_pausa = pygame.font.SysFont('arial', 36, bold=True)
        self.font_menu_pausa = pygame.font.SysFont('arial', 24, bold=True)
        self.running = True
        self.pausado = False
        self.volver_menu = False
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_limite = self._get_tiempo_limite()
        self.tiempo_actual = 0
        self.tiempo_pausado = 0
        self.puntaje = 0
        
        self.mapa = Mapa(self.modo)
        self.inicio = self.mapa.inicio
        self.salida = self.mapa.salida
        self.jugador = Jugador(self.inicio[0], self.inicio[1])
        
        # Lógica de 3 enemigos individuales
        self.num_enemigos_total = 3
        self.enemigos = [] # Lista de objetos Enemigo activos
        self.enemigos_data = [] # Lista de diccionarios para rastrear ID y timer
        self._inicializar_enemigos()
        
        # Límite de 3 trampas activas (sin cooldown)
        self.trampas_activas = [] # Lista de posiciones (r, c) de trampas en el mapa
        self.max_trampas_activas = 3
        
        # Timers personalizados para control de IA
        self.enemigo_timer = 0
        self.enemigo_delay = self._get_enemigo_delay()
        
        # Opciones del menú de pausa
        self.opciones_pausa = ['Continuar', 'Reiniciar', 'Salir al Menu']
        self.opcion_seleccionada = 0