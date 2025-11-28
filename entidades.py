# entidades.py 
import pygame
from config import TAM_CELDA, COLORES_JUEGO, HUD_HEIGHT

class Terreno:
    def __init__(self, tipo):
        self.tipo = tipo

    def es_accesible_jugador(self): 
        """Define la accesibilidad para el rol de Presa (usa Túneles)"""
        return False

    def es_accesible_enemigo(self):
        """Define la accesibilidad para el rol de Cazador (usa Lianas)"""
        return False

    def dibujar(self, screen, fila, col):
        x = col * TAM_CELDA
        y = fila * TAM_CELDA + HUD_HEIGHT
        rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(screen, COLORES_JUEGO[self.tipo], rect)
        pygame.draw.rect(screen, (60, 60, 60), rect, 1)

class Camino(Terreno):
    def __init__(self): super().__init__('camino')
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return True

class Liana(Terreno):
    def __init__(self): super().__init__('liana')
    # Accesible solo para Cazadores (es_accesible_enemigo)
    def es_accesible_jugador(self): return False 
    def es_accesible_enemigo(self): return True

class Tunel(Terreno):
    def __init__(self): super().__init__('tunel')
    # Accesible solo para Presas (es_accesible_jugador)
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return False

class Muro(Terreno):
    def __init__(self): super().__init__('muro')
    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return False

class Trampa(Terreno):
    def __init__(self):
        super().__init__('trampa')
        self.activa = True
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return True

class Entidad:
    def __init__(self, fila, col, color):
        self.fila = fila
        self.col = col
        self.color = color

    # El método mover ahora recibe el modo de juego
    def mover(self, mapa, df, dc, modo):
        nueva_fila = self.fila + df
        nueva_col = self.col + dc
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.cols:
            terreno = mapa.matriz[nueva_fila][nueva_col]
            if self.puede_acceder(terreno, modo):
                self.fila = nueva_fila
                self.col = nueva_col
                return True
        return False

    # El método de acceso ahora recibe el modo de juego
    def puede_acceder(self, terreno, modo):
        return False

    def dibujar(self, screen):
        x = self.col * TAM_CELDA
        y = self.fila * TAM_CELDA + HUD_HEIGHT
        center_x = x + TAM_CELDA // 2
        center_y = y + TAM_CELDA // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), TAM_CELDA // 3)
        pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), TAM_CELDA // 3, 2)

class Jugador(Entidad):
    def __init__(self, fila, col):
        super().__init__(fila, col, COLORES_JUEGO['jugador'])
        self.energia = 100
        self.max_energia = 100
        self.recuperacion = 0.15
        self.consumo_correr = 2

    def puede_acceder(self, terreno, modo):
        # LÓGICA DE ROLES INVERTIDA:
        if modo == 'escapa':
            # Rol: PRESA (Usa las reglas de 'jugador': Túneles SI, Lianas NO)
            return terreno.es_accesible_jugador()
        else: # modo cazador
            # Rol: CAZADOR (Usa las reglas de 'enemigo': Lianas SI, Túneles NO)
            return terreno.es_accesible_enemigo()

    def correr(self, mapa, df, dc, modo):
        if self.energia >= self.consumo_correr:
            # Pasar modo al mover
            if self.mover(mapa, df, dc, modo):
                self.energia -= self.consumo_correr
                return True
        return False

    def actualizar_energia(self):
        self.energia = min(self.max_energia, self.energia + self.recuperacion)

class Enemigo(Entidad):
    def __init__(self, fila, col):
        super().__init__(fila, col, COLORES_JUEGO['enemigo'])

    def puede_acceder(self, terreno, modo):
        # LÓGICA DE ROLES INVERTIDA:
        if modo == 'escapa':
            # Rol: CAZADOR (Usa las reglas de 'enemigo': Lianas SI, Túneles NO)
            return terreno.es_accesible_enemigo()
        else: # modo cazador
            # Rol: PRESA (Usa las reglas de 'jugador': Túneles SI, Lianas NO)
            return terreno.es_accesible_jugador()