# mapa.py
import random
from collections import deque
import pygame
from config import FILAS_MAPA, COLUMNAS_MAPA, TAM_CELDA, COLORES_JUEGO, ANCHO, ALTO, HUD_HEIGHT

from entidades import Camino, Liana, Tunel, Muro, Trampa 

class Mapa:
    def __init__(self, modo):
        self.modo = modo
        self.filas = FILAS_MAPA
        self.cols = COLUMNAS_MAPA
        self.matriz = []
        self.inicio = (1, 1)
        self.salida = (self.filas - 2, self.cols - 2)
        self.valid_spawn = [] # 🟢 CORRECCIÓN 1: Inicializar el atributo
        
        # Generar hasta asegurar que la salida es alcanzable
        self._generar_mapa()

    def _generar_mapa(self):
        """Genera el mapa asegurando camino válido para el rol de Presa."""
        intentos = 0
        max_intentos = 20
        
        while intentos < max_intentos:
            self.generar_laberinto_recursivo()
            
            # Generar múltiples atajos para asegurar la conectividad
            self._generar_atajos(num_lianas=8, num_tuneles=8) 
            
            # Validar camino para el rol de PRESA (es_jugador=True)
            if self.hay_camino(self.inicio, self.salida, es_jugador=True):
                print(f"✓ Mapa válido generado en intento {intentos + 1}")
                
                #  CORRECCIÓN 2: Llenar el atributo valid_spawn
                self.valid_spawn = []
                for r in range(1, self.filas - 1):
                    for c in range(1, self.cols - 1):
                        # Solo considera Caminos y excluye Inicio/Salida como puntos de spawn aleatorios
                        if isinstance(self.matriz[r][c], Camino) and \
                           (r, c) != self.inicio and (r, c) != self.salida:
                            self.valid_spawn.append((r, c))
                
                self._imprimir_estadisticas()
                break
            
            intentos += 1
        
        if intentos == max_intentos:
            print(" Advertencia: No se pudo generar un mapa con camino garantizado.")

    def generar_laberinto_recursivo(self):
        """Inicializa la matriz a Muros y crea el laberinto usando DFS."""
        self.matriz = [[Muro() for _ in range(self.cols)] for _ in range(self.filas)]
        self._dfs_laberinto(1, 1)
        self.matriz[self.inicio[0]][self.inicio[1]] = Camino() # Asegurar inicio como camino
        self.matriz[self.salida[0]][self.salida[1]] = Camino() # Asegurar salida como camino

    def _dfs_laberinto(self, r, c):
        """Algoritmo DFS para generar el laberinto."""
        self.matriz[r][c] = Camino()
        direcciones = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(direcciones)
        
        for dr, dc in direcciones:
            nr, nc = r + dr, c + dc
            if 0 < nr < self.filas - 1 and 0 < nc < self.cols - 1 and isinstance(self.matriz[nr][nc], Muro):
                # Derribar el muro intermedio
                self.matriz[r + dr // 2][c + dc // 2] = Camino()
                self._dfs_laberinto(nr, nc)

    def _generar_atajos(self, num_lianas, num_tuneles):
        """Reemplaza muros aleatorios por Lianas (Cazador) y Túneles (Presa) en zonas seguras."""
        muros_candidatos = []
        for r in range(1, self.filas - 1):
            for c in range(1, self.cols - 1):
                if isinstance(self.matriz[r][c], Muro):
                    muros_candidatos.append((r, c))
        
        random.shuffle(muros_candidatos)
        
        # 1. Colocar Lianas (para Cazadores)
        temp_candidatos = muros_candidatos[:]
        for i in range(min(num_lianas, len(temp_candidatos))):
            r, c = temp_candidatos.pop(random.randrange(len(temp_candidatos)))
            self.matriz[r][c] = Liana()
        
        # 2. Colocar Túneles (para Presas/Jugador)
        muros_restantes = [pos for pos in muros_candidatos if isinstance(self.matriz[pos[0]][pos[1]], Muro)]
        for i in range(min(num_tuneles, len(muros_restantes))):
            r, c = muros_restantes.pop(random.randrange(len(muros_restantes)))
            self.matriz[r][c] = Tunel()

    def _imprimir_estadisticas(self):
        """Imprime la cantidad de cada tipo de terreno."""
        tipos = {}
        for row in self.matriz:
            for cell in row:
                tipo = cell.tipo
                tipos[tipo] = tipos.get(tipo, 0) + 1
        # print("Estadísticas del mapa:", tipos) # Descomentar para debug

    def es_celda_accesible(self, fila, col, es_jugador):
        """Verifica si una celda es accesible por el rol dado, sin verificar límites."""
        if 0 <= fila < self.filas and 0 <= col < self.cols:
            terreno = self.matriz[fila][col]
            if es_jugador:
                return terreno.es_accesible_jugador()
            else:
                return terreno.es_accesible_enemigo()
        return False

    def hay_camino(self, inicio, fin, es_jugador): 
        """Verifica si existe un camino entre inicio y fin, considerando el rol (jugador o enemigo)."""
        # es_rol_cazador=True para Cazador (accede Lianas), False para Presa (accede Túneles)
        es_rol_cazador = not es_jugador
        path = self.encontrar_camino(inicio[0], inicio[1], fin[0], fin[1], es_rol_cazador)
        return bool(path) # Retorna True si la lista no está vacía

    def encontrar_camino(self, inicio_fila, inicio_col, fin_fila, fin_col, es_rol_cazador):
        """
        Encuentra el camino más corto (BFS).
        - es_rol_cazador=True: Accede a Lianas.
        - es_rol_cazador=False: Accede a Túneles (Presa).
        """
        queue = deque([(inicio_fila, inicio_col, [(inicio_fila, inicio_col)])])
        visitado = set([(inicio_fila, inicio_col)])
        
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        while queue:
            fila, col, path = queue.popleft()
            
            if fila == fin_fila and col == fin_col:
                return path
            
            for df, dc in direcciones:
                nf, nc = fila + df, col + dc
                
                if 0 <= nf < self.filas and 0 <= nc < self.cols and (nf, nc) not in visitado:
                    terreno = self.matriz[nf][nc]
                    
                    # Lógica de acceso basada en el rol
                    if es_rol_cazador:
                        accesible = terreno.es_accesible_enemigo() 
                    else:
                        accesible = terreno.es_accesible_jugador() # Presa
                        
                    if accesible:
                        visitado.add((nf, nc))
                        new_path = path + [(nf, nc)]
                        queue.append((nf, nc, new_path))
        
        return []

    def dibujar(self, screen):
        """Dibuja el mapa en la pantalla, considerando HUD superior"""
        for fila in range(self.filas):
            for col in range(self.cols):
                self.matriz[fila][col].dibujar(screen, fila, col)
                
        # Dibujar salida con color especial (por ejemplo, blanco)
        salida_x = self.salida[1] * TAM_CELDA
        salida_y = self.salida[0] * TAM_CELDA + HUD_HEIGHT
        salida_rect = pygame.Rect(salida_x, salida_y, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(screen, COLORES_JUEGO['salida'], salida_rect)