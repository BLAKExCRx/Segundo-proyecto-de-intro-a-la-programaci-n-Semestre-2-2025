#mapa.py en proceso
import random
from collections import deque
import pygame
from config import FILAS_MAPA, COLUMNAS_MAPA, TAM_CELDA, COLORES_JUEGO, ANCHO, ALTO, HUD_HEIGHT
from entidades import Camino, Liana, Tunel, Muro
#prueba de generacion de mapa primera parte , probablemente falle terriblemente XD
class Mapa:
    def __init__(self):
        self.filas = FILAS_MAPA
        self.cols = COLUMNAS_MAPA
        self.matriz = [[Muro() for _ in range(self.cols)] for _ in range(self.filas)]
        self.inicio = (1, 1)
        self.salida = (self.filas - 2, self.cols - 2)
        self.generar_mapa()
    
    def generar_mapa(self):
        stack = []
        self.matriz[self.inicio[0]][self.inicio[1]] = Camino()
        stack.append(self.inicio)
        
        while stack:
            actual = stack[-1]
            vecinos = self._obtener_vecinos_validos(actual)
            if vecinos:
                vecino = random.choice(vecinos)
                self._conectar_celdas(actual, vecino)
                stack.append(vecino)
            else:
                stack.pop()
        
        self.matriz[self.salida[0]][self.salida[1]] = Camino()
        
        if not self.hay_camino(self.inicio, self.salida, es_jugador=True):
            self.generar_mapa()
        
        for i in range(self.filas):
            for j in range(self.cols):
                if isinstance(self.matriz[i][j], Camino) and random.random() < 0.2:
                    if random.random() < 0.5:
                        self.matriz[i][j] = Liana()
                    else:
                        self.matriz[i][j] = Tunel()
    def _obtener_vecinos_validos(self, pos):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        vecinos = []
        for d in dirs:
            ni, nj = pos[0] + d[0] * 2, pos[1] + d[1] * 2
            if 1 <= ni < self.filas - 1 and 1 <= nj < self.cols - 1 and isinstance(self.matriz[ni][nj], Muro):
                vecinos.append((ni, nj))
        return vecinos
    
    def _conectar_celdas(self, a, b):
        mid_i = (a[0] + b[0]) // 2
        mid_j = (a[1] + b[1]) // 2
        self.matriz[mid_i][mid_j] = Camino()
        self.matriz[b[0]][b[1]] = Camino()