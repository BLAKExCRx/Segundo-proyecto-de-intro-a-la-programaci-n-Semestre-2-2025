#mapa.py en proceso
import random
from collections import deque
import pygame
from config import FILAS_MAPA, COLUMNAS_MAPA, TAM_CELDA, COLORES_JUEGO, ANCHO, ALTO, HUD_HEIGHT
from entidades import Camino, Liana, Tunel, Muro
#prueba de generacion de mapa primera parte , probablemente falle terriblemente XD
class Mapa:
    def __init__(self, modo):
        self.modo = modo
        self.filas = FILAS_MAPA
        self.cols = COLUMNAS_MAPA
        self.matriz = []
        self.inicio = (1, 1)
        self.salida = (self.filas - 2, self.cols - 2)
        
        # Lista de posibles puntos de aparición de entidades
        self.valid_spawn = [] 
        
        self._generar_mapa()

    def _generar_mapa(self):
        """Genera el mapa asegurando camino válido para el rol de Presa"""
        intentos = 0
        max_intentos = 20
        
        while intentos < max_intentos:
            self.generar_laberinto_recursivo()
            
            #  Validar camino para el rol de Presa (es_rol_cazador=False, usa Túneles)
            if self.hay_camino(self.inicio, self.salida, es_rol_cazador=False):
                print(f"✓ Mapa válido generado en intento {intentos + 1}")
                self._imprimir_estadisticas()
                break
            intentos += 1
        
        if intentos == max_intentos:
            print(" Error: No se pudo generar un mapa con camino válido después de 20 intentos.")
            # Solución de emergencia: asegurar Camino de inicio a fin
            self.matriz[self.inicio[0]][self.inicio[1]] = Camino()
            self.matriz[self.salida[0]][self.salida[1]] = Camino()
            
        self.agregar_terrenos_especiales()
        self.actualizar_valid_spawn()

    def _imprimir_estadisticas(self):
        """Calcula e imprime la proporción de cada tipo de terreno."""
        conteo = {'muro': 0, 'camino': 0, 'liana': 0, 'tunel': 0, 'trampa': 0}
        total = self.filas * self.cols
        for fila in range(self.filas):
            for col in range(self.cols):
                conteo[self.matriz[fila][col].tipo] += 1
        
        print(f"Estadísticas del mapa:")
        for tipo, count in conteo.items():
            print(f"  {tipo.capitalize()}: {count} ({count/total:.1%})")

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
        """Genera un laberinto usando el algoritmo de división recursiva."""
        # Inicializa la matriz como todo Muro
        self.matriz = [[Muro() for _ in range(self.cols)] for _ in range(self.filas)]
        
        # Marcar todo el interior como Camino (para empezar)
        for r in range(1, self.filas - 1):
            for c in range(1, self.cols - 1):
                self.matriz[r][c] = Camino()
                
        # Llamada inicial: el rectángulo a dividir va de (1, 1) a (filas-2, cols-2)
        self._dividir((1, 1, self.filas - 2, self.cols - 2))
        
        # Asegurar inicio y fin como Camino
        self.matriz[self.inicio[0]][self.inicio[1]] = Camino()
        self.matriz[self.salida[0]][self.salida[1]] = Camino())
        
        

    def agregar_terrenos_especiales(self):
        """Agrega Lianas y Túneles en caminos existentes, sin romper la conectividad."""
        num_lianas = random.randint(3, 5)
        num_tuneles = random.randint(3, 5)
        
        # Obtener todas las posiciones de Camino válidas (no inicio/salida)
        camino_pos = []
        for r in range(1, self.filas - 1):
            for c in range(1, self.cols - 1):
                if isinstance(self.matriz[r][c], Camino):
                    if (r, c) != self.inicio and (r, c) != self.salida:
                        camino_pos.append((r, c))
        
        random.shuffle(camino_pos)
        
        # 1. Agregar Lianas
        lianas_colocadas = 0
        for r, c in camino_pos:
            if lianas_colocadas >= num_lianas: break
            
            # Intentar cambiar Camino a Liana
            self.matriz[r][c] = Liana()
            
            # Verificar si el camino de la Presa (rol cazador=False) sigue existiendo
            if self.hay_camino(self.inicio, self.salida, es_rol_cazador=False):
                # El cambio es válido, la Presa aún puede escapar
                lianas_colocadas += 1
            else:
                # El cambio rompió el camino de la Presa, revertir
                self.matriz[r][c] = Camino()
        
        # 2. Agregar Túneles
        # Usar las posiciones restantes de Camino y las Lianas recién creadas
        tunel_posibles = [(r, c) for r in range(self.filas) for c in range(self.cols) 
                          if isinstance(self.matriz[r][c], Camino) or isinstance(self.matriz[r][c], Liana)]
        
        random.shuffle(tunel_posibles)
        
        tuneles_colocados = 0
        for r, c in tunel_posibles:
            if tuneles_colocados >= num_tuneles: break

            # Guardar el terreno original por si hay que revertir
            terreno_original = self.matriz[r][c]
            
            # Intentar cambiar a Túnel
            self.matriz[r][c] = Tunel()
            
            # Verificar si el camino del Cazador (rol cazador=True) sigue existiendo
            # NOTA: En modo Escapa, el jugador es Presa y la IA es Cazador. 
            # El Cazador (IA) necesita tener camino para empezar.
            if self.hay_camino(self.inicio, self.salida, es_rol_cazador=True):
                # El cambio es válido, el Cazador aún puede perseguir
                tuneles_colocados += 1
            else:
                # El cambio rompió el camino del Cazador, revertir
                self.matriz[r][c] = terreno_original


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
