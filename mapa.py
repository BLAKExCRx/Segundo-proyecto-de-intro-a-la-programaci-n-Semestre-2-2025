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

    def _crear_camino_emergencia(self):
        """Crea un camino directo de inicio a salida si está bloqueado"""
        print("Creando camino de emergencia...")
        fila_actual, col_actual = self.inicio
        fila_meta, col_meta = self.salida
        
        # Crear camino horizontal hasta la columna de la salida
        while col_actual != col_meta:
            self.matriz[fila_actual][col_actual] = Camino()
            col_actual += 1 if col_actual < col_meta else -1
        
        # Crear camino vertical hasta la fila de la salida
        while fila_actual != fila_meta:
            self.matriz[fila_actual][col_actual] = Camino()
            fila_actual += 1 if fila_actual < fila_meta else -1
        
        # Asegurar salida
        self.matriz[fila_meta][col_meta] = Camino()

    def _generar_mapa_emergencia(self):
        """Genera un mapa simple garantizado si todo falla"""
        print("Generando mapa de emergencia simple...")
        self.matriz = [[Muro() for _ in range(self.cols)] for _ in range(self.filas)]
        
        # Crear caminos horizontales cada 2 filas
        for fila in range(1, self.filas - 1, 2):
            for col in range(1, self.cols - 1):
                self.matriz[fila][col] = Camino()
        
        # Crear caminos verticales cada 4 columnas
        for col in range(1, self.cols - 1, 4):
            for fila in range(1, self.filas - 1):
                self.matriz[fila][col] = Camino()
        
        # Asegurar inicio y salida
        self.matriz[self.inicio[0]][self.inicio[1]] = Camino()
        self.matriz[self.salida[0]][self.salida[1]] = Camino()

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
    def agregar_terrenos_especiales(self):
        pass

    def hay_camino(self, start, goal, es_jugador=True):
        pass

    def encontrar_camino(self, start_fila, start_col, goal_fila, goal_col, es_jugador=False):
        pass
    
    def _es_terreno_especial(self, fila, col):
        """Verifica si una celda es Túnel o Liana"""
        if 0 <= fila < self.filas and 0 <= col < self.cols:
            terreno = self.matriz[fila][col]
            return isinstance(terreno, Tunel) or isinstance(terreno, Liana)
        return False
    
    def dibujar(self, screen):
        pass
