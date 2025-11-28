#mapa.py en proceso
import random
from collections import deque
import pygame
from config import FILAS_MAPA, COLUMNAS_MAPA, TAM_CELDA, COLORES_JUEGO, ANCHO, ALTO, HUD_HEIGHT
from entidades import Camino, Liana, Tunel, Muro
#prueba de generacion de mapa primera parte , probablemente falle terriblemente XD
class Mapa:
    def __init__(self, modo):  # <-- AGREGAR PARÁMETRO modo
        self.modo = modo
        self.filas = FILAS_MAPA
        self.cols = COLUMNAS_MAPA
        self.matriz = []
        self.inicio = (1, 1)  # Esquina superior izquierda
        self.salida = (self.filas - 2, self.cols - 2)  # Esquina opuesta
        
        # Generar hasta asegurar que la salida es alcanzable
        self._generar_mapa()

    def _generar_mapa(self):
        """Genera el mapa asegurando camino válido"""
        intentos = 0
        max_intentos = 20
        
        while intentos < max_intentos:
            self.generar_laberinto_recursivo()
            
            # Validar camino para jugador
            if self.hay_camino(self.inicio, self.salida, es_jugador=True):
                print(f"✓ Mapa válido generado en intento {intentos + 1}")
                self._imprimir_estadisticas()
                break
            intentos += 1
            print(f"✗ Intento {intentos} falló, regenerando...")
        
        if intentos >= max_intentos:
            print(" Advertencia: Generando mapa de emergencia")
            self._generar_mapa_emergencia()
        
        # Añadir terrenos especiales solo después de asegurar el camino
        self.agregar_terrenos_especiales()
        
    def _imprimir_estadisticas(self):
        """Imprime estadísticas del mapa generado"""
        total_celdas = self.filas * self.cols
        caminos = sum(1 for fila in self.matriz for celda in fila if isinstance(celda, Camino))
        muros = sum(1 for fila in self.matriz for celda in fila if isinstance(celda, Muro))
        
        print(f"  Celdas totales: {total_celdas}")
        print(f"  Caminos: {caminos} ({caminos*100//total_celdas}%)")
        print(f"  Muros: {muros} ({muros*100//total_celdas}%)")

    def generar_laberinto_recursivo(self):
        #  Llenar todo de muros
        self.matriz = [[Muro() for _ in range(self.cols)] for _ in range(self.filas)]
        
        #  Algoritmo Recursive Backtracker
        
        start_x, start_y = 1, 1
        self.matriz[start_y][start_x] = Camino()
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack[-1]
            vecinos = []

            # Buscar vecinos a 2 celdas de distancia (saltando pared)
            # Arriba, Abajo, Izquierda, Derecha
            direcciones = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                # Verificar límites (dejando borde de muro exterior)
                if 1 <= nx < self.cols - 1 and 1 <= ny < self.filas - 1:
                    # Si el destino es Muro, es un candidato válido no visitado
                    if isinstance(self.matriz[ny][nx], Muro):
                        vecinos.append((nx, ny, dx // 2, dy // 2))

            if vecinos:
                nx, ny, wall_x, wall_y = random.choice(vecinos)
                # Abrir la celda destino
                self.matriz[ny][nx] = Camino()
                # Abrir el muro intermedio
                self.matriz[y + wall_y][x + wall_x] = Camino()
                stack.append((nx, ny))
            else:
                stack.pop()
    def _es_terreno_especial(self, fila, col):
        """Verifica si una celda es Túnel o Liana."""
        if 0 <= fila < self.filas and 0 <= col < self.cols:
            terreno = self.matriz[fila][col]
            return isinstance(terreno, Tunel) or isinstance(terreno, Liana)
        return False
