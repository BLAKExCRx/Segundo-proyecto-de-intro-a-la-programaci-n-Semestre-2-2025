# mapa.py
import random
from collections import deque
import pygame
from config import FILAS_MAPA, COLUMNAS_MAPA, TAM_CELDA, COLORES_JUEGO, ANCHO, ALTO, HUD_HEIGHT
from entidades import Camino, Liana, Tunel, Muro

class Mapa:
    def __init__(self, modo):
        self.modo = modo
        self.filas = FILAS_MAPA
        self.cols = COLUMNAS_MAPA
        self.matriz = []
        self.inicio = (1, 1)
        self.salida = (self.filas - 2, self.cols - 2)
        self.valid_spawn = []
        
        self._generar_mapa()

    def _generar_mapa(self):
        """Genera el mapa asegurando camino válido"""
        intentos = 0
        max_intentos = 20
        
        while intentos < max_intentos:
            self.generar_laberinto_recursivo()
            
            if self.hay_camino(self.inicio, self.salida, es_jugador=True):
                print(f"✓ Mapa válido generado en intento {intentos + 1}")
                self._imprimir_estadisticas()
                break
            intentos += 1
            print(f"✗ Intento {intentos} falló, regenerando...")
        
        if intentos >= max_intentos:
            print("⚠ Advertencia: Generando mapa de emergencia")
            self._generar_mapa_emergencia()
        
        # Añadir terrenos especiales después de asegurar el camino
        self.agregar_terrenos_especiales()
        
        # Generar lista de spawns válidos
        self._generar_valid_spawn()
    
    def _generar_valid_spawn(self):
        """Genera lista de posiciones válidas para spawn de entidades"""
        self.valid_spawn = []
        for fila in range(1, self.filas - 1):
            for col in range(1, self.cols - 1):
                terreno = self.matriz[fila][col]
                if isinstance(terreno, (Camino, Tunel)):
                    if (fila, col) != self.inicio and (fila, col) != self.salida:
                        self.valid_spawn.append((fila, col))
        
        print(f"  Spawns válidos encontrados: {len(self.valid_spawn)}")
    
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
        
        while col_actual != col_meta:
            self.matriz[fila_actual][col_actual] = Camino()
            col_actual += 1 if col_actual < col_meta else -1
        
        while fila_actual != fila_meta:
            self.matriz[fila_actual][col_actual] = Camino()
            fila_actual += 1 if fila_actual < fila_meta else -1
        
        self.matriz[fila_meta][col_meta] = Camino()
    
    def _generar_mapa_emergencia(self):
        """Genera un mapa simple garantizado si todo falla"""
        print("Generando mapa de emergencia simple...")
        self.matriz = [[Muro() for _ in range(self.cols)] for _ in range(self.filas)]
        
        for fila in range(1, self.filas - 1, 2):
            for col in range(1, self.cols - 1):
                self.matriz[fila][col] = Camino()
        
        for col in range(1, self.cols - 1, 4):
            for fila in range(1, self.filas - 1):
                self.matriz[fila][col] = Camino()
        
        self.matriz[self.inicio[0]][self.inicio[1]] = Camino()
        self.matriz[self.salida[0]][self.salida[1]] = Camino()

    def generar_laberinto_recursivo(self):
        """Genera laberinto usando algoritmo mejorado de Prim - MÁS LABERÍNTICO"""
        # Llenar todo de muros
        self.matriz = [[Muro() for _ in range(self.cols)] for _ in range(self.filas)]
        
        # Empezar desde inicio
        inicio_fila, inicio_col = 1, 1
        self.matriz[inicio_fila][inicio_col] = Camino()
        
        # Lista de muros frontera
        muros = []
        
        def agregar_muros(fila, col):
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nf, nc = fila + df, col + dc
                if 0 < nf < self.filas - 1 and 0 < nc < self.cols - 1:
                    if isinstance(self.matriz[nf][nc], Muro):
                        if (nf, nc) not in muros:
                            muros.append((nf, nc))
        
        agregar_muros(inicio_fila, inicio_col)
        
        # Mientras haya muros en la frontera
        while muros:
            # Elegir un muro aleatorio
            muro_actual = random.choice(muros)
            muros.remove(muro_actual)
            muro_fila, muro_col = muro_actual
            
            # Contar vecinos que son camino
            vecinos_camino = []
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nf, nc = muro_fila + df, muro_col + dc
                if 0 <= nf < self.filas and 0 <= nc < self.cols:
                    if isinstance(self.matriz[nf][nc], Camino):
                        vecinos_camino.append((nf, nc))
            
            # Solo convertir en camino si tiene EXACTAMENTE un vecino camino
            # Esto hace el laberinto MÁS LABERÍNTICO
            if len(vecinos_camino) == 1:
                self.matriz[muro_fila][muro_col] = Camino()
                agregar_muros(muro_fila, muro_col)
        
        # Crear POCOS ciclos adicionales (solo 2-3% para mantener el laberinto difícil)
        num_ciclos = int((self.filas * self.cols) * 0.025)  # Reducido de 0.05 a 0.025
        for _ in range(num_ciclos):
            fila = random.randint(1, self.filas - 2)
            col = random.randint(1, self.cols - 2)
            if isinstance(self.matriz[fila][col], Muro):
                # Verificar que tiene al menos 2 vecinos camino
                vecinos_camino = 0
                for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nf, nc = fila + df, col + dc
                    if 0 <= nf < self.filas and 0 <= nc < self.cols:
                        if isinstance(self.matriz[nf][nc], Camino):
                            vecinos_camino += 1
                
                if vecinos_camino >= 2:
                    self.matriz[fila][col] = Camino()
        
        # Asegurar que inicio y salida son Camino
        self.matriz[self.inicio[0]][self.inicio[1]] = Camino()
        self.matriz[self.salida[0]][self.salida[1]] = Camino()
        
        # Asegurar camino directo a la salida si está bloqueada
        if not self.hay_camino(self.inicio, self.salida, es_jugador=True):
            self._crear_camino_emergencia()

    def agregar_terrenos_especiales(self):
        """Añade lianas y túneles entre muros sin bloquear el camino principal"""
        # REDUCIR cantidad de terrenos especiales para no saturar
        num_especiales = random.randint(2, 5)  # Reducido de (3, 8)
        agregados = 0
        intentos = 0
        max_intentos = 100
        
        while agregados < num_especiales and intentos < max_intentos:
            fila = random.randint(1, self.filas - 2)
            col = random.randint(1, self.cols - 2)
            
            # Solo reemplazar muros entre caminos
            if isinstance(self.matriz[fila][col], Muro):
                # Verificar que hay caminos adyacentes
                adyacentes = [
                    (fila-1, col), (fila+1, col), 
                    (fila, col-1), (fila, col+1)
                ]
                
                num_caminos_ady = sum(
                    1 for f, c in adyacentes 
                    if 0 <= f < self.filas and 0 <= c < self.cols 
                    and isinstance(self.matriz[f][c], Camino)
                )
                
                # Si tiene al menos 2 caminos adyacentes
                if num_caminos_ady >= 2:
                    # Elegir Liana o Túnel
                    tipo = random.choice([Liana, Tunel])
                    terreno_original = self.matriz[fila][col]
                    self.matriz[fila][col] = tipo()
                    
                    # Verificar que no rompe el camino del jugador
                    if tipo == Liana:
                        if not self.hay_camino(self.inicio, self.salida, es_jugador=True):
                            self.matriz[fila][col] = terreno_original
                        else:
                            agregados += 1
                    else:
                        agregados += 1
            
            intentos += 1

    def hay_camino(self, start, goal, es_jugador=True):
        """BFS para verificar si hay camino válido"""
        fila_start, col_start = start
        fila_goal, col_goal = goal
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
                    accesible = terreno.es_accesible_jugador() if es_jugador else terreno.es_accesible_enemigo()
                    if accesible:
                        visitado[nf][nc] = True
                        queue.append((nf, nc))
        
        return False

    def encontrar_camino(self, start_fila, start_col, goal_fila, goal_col, es_jugador=False, es_rol_cazador=False):
        """BFS para encontrar path más corto"""
        visitado = [[False] * self.cols for _ in range(self.filas)]
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

    def es_celda_accesible(self, fila, col, es_jugador=True):
        """Verifica si una celda es accesible"""
        if 0 <= fila < self.filas and 0 <= col < self.cols:
            terreno = self.matriz[fila][col]
            return terreno.es_accesible_jugador() if es_jugador else terreno.es_accesible_enemigo()
        return False

    def _es_terreno_especial(self, fila, col):
        """Verifica si una celda es Túnel o Liana"""
        if 0 <= fila < self.filas and 0 <= col < self.cols:
            terreno = self.matriz[fila][col]
            return isinstance(terreno, Tunel) or isinstance(terreno, Liana)
        return False

    def dibujar(self, screen):
        """Dibuja el mapa en la pantalla, considerando HUD superior"""
        for fila in range(self.filas):
            for col in range(self.cols):
                self.matriz[fila][col].dibujar(screen, fila, col)
                
        # Dibujar salida con color especial
        salida_x = self.salida[1] * TAM_CELDA
        salida_y = self.salida[0] * TAM_CELDA + HUD_HEIGHT
        salida_rect = pygame.Rect(salida_x, salida_y, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(screen, COLORES_JUEGO['salida'], salida_rect)
        pygame.draw.rect(screen, (0, 0, 0), salida_rect, 2)