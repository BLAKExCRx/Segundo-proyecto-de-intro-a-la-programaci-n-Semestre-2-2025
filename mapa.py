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
        self.matriz[self.salida[0]][self.salida[1]] = Camino()
        
        

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
    def actualizar_valid_spawn(self):
        """Identifica posiciones válidas para reaparición de entidades (que no sean muros ni cerca del inicio/salida)."""
        self.valid_spawn.clear()
        for r in range(1, self.filas - 1):
            for c in range(1, self.cols - 1):
                terreno = self.matriz[r][c]
                # Posición válida si no es muro y no está en el área de inicio/salida
                if not isinstance(terreno, Muro) and \
                   abs(r - self.inicio[0]) + abs(c - self.inicio[1]) > 5 and \
                   abs(r - self.salida[0]) + abs(c - self.salida[1]) > 5:
                    self.valid_spawn.append((r, c))

    def hay_camino(self, start, goal, es_rol_cazador=False):
        """BFS para verificar si hay camino válido para el rol específico (Presa o Cazador)"""
        fila_start, col_start = start
        fila_goal, col_goal = goal
        # ... (Mantener la implementación de hay_camino con la lógica de es_rol_cazador)
        visitado = [[False] * self.cols for _ in range(self.filas)]
        queue = deque([(fila_start, col_start)])
        visitado[fila_start][col_start] = True
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            fila, col = queue.popleft()
            if (fila, col) == (fila_goal, col_goal):
                return True
            
            for df, dc in direcciones:
                nf, nc = fila + df, col + dc
                if 0 <= nf < self.filas and 0 <= nc < self.cols and not visitado[nf][nc]:
                    terreno = self.matriz[nf][nc]
                    
                    if es_rol_cazador:
                        # Si es Cazador, usa la regla de 'enemigo' (puede usar Lianas)
                        accesible = terreno.es_accesible_enemigo() 
                    else:
                        # Si es Presa, usa la regla de 'jugador' (puede usar Túneles)
                        accesible = terreno.es_accesible_jugador() 

                    if accesible:
                        visitado[nf][nc] = True
                        queue.append((nf, nc))
        return False
    
    def encontrar_camino(self, start_fila, start_col, goal_fila, goal_col, es_rol_cazador=True):
        """BFS para encontrar path más corto considerando el rol (Presa o Cazador)"""
        # ... (Mantener la implementación de encontrar_camino con la lógica de es_rol_cazador)
        visitado = [[False] * self.cols for _ in range(self.filas)]
        # Almacena (fila, col, path_lista)
        queue = deque([(start_fila, start_col, [])])
        visitado[start_fila][start_col] = True
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            fila, col, path = queue.popleft()
            current = (fila, col)
            path = path + [current]
            
            if current == (goal_fila, goal_col):
                return path
            
            for df, dc in direcciones:
                nf, nc = fila + df, col + dc
                if 0 <= nf < self.filas and 0 <= nc < self.cols and not visitado[nf][nc]:
                    terreno = self.matriz[nf][nc]
                    
                    if es_rol_cazador:
                        accesible = terreno.es_accesible_enemigo()
                    else:
                        accesible = terreno.es_accesible_jugador()
                        
                    if accesible:
                        visitado[nf][nc] = True
                        queue.append((nf, nc, path))
        return []
    
    def dibujar(self, screen):
        """Dibuja el mapa en la pantalla, considerando HUD superior"""
        for fila in range(self.filas):
            for col in range(self.cols):
                self.matriz[fila][col].dibujar(screen, fila, col)
                
        # Dibujar salida con color especial (por ejemplo, blanco)
        salida_x = self.salida[1] * TAM_CELDA
        salida_y = self.salida[0] * TAM_CELDA + HUD_HEIGHT
        pygame.draw.rect(screen, (255, 255, 255), (salida_x, salida_y, TAM_CELDA, TAM_CELDA), 3)
