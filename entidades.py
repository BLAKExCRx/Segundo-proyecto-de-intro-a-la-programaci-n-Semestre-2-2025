# entidades.py 
import pygame
from config import TAM_CELDA, COLORES_JUEGO, HUD_HEIGHT


class Terreno:
    def __init__(self, tipo):
        self.tipo = tipo

    def es_accesible_jugador(self):
        return False

    def es_accesible_enemigo(self):
        return False

    def dibujar(self, screen, fila, col):
        x = col * TAM_CELDA
        y = fila * TAM_CELDA + HUD_HEIGHT
        rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(screen, COLORES_JUEGO[self.tipo], rect)
        # Borde de celda
        pygame.draw.rect(screen, (60, 60, 60), rect, 1)


class Camino(Terreno):
    def __init__(self):
        super().__init__('camino')

    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return True


class Liana(Terreno):
    def __init__(self):
        super().__init__('liana')

    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return True


class Tunel(Terreno):
    def __init__(self):
        super().__init__('tunel')

    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return False


class Muro(Terreno):
    def __init__(self):
        super().__init__('muro')

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

    def mover(self, mapa, df, dc):
        nueva_fila = self.fila + df
        nueva_col = self.col + dc
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.cols:
            terreno = mapa.matriz[nueva_fila][nueva_col]
            if self.puede_acceder(terreno):
                self.fila = nueva_fila
                self.col = nueva_col
                return True
        return False

    def puede_acceder(self, terreno):
        return False

    def dibujar(self, screen):
        x = self.col * TAM_CELDA
        y = self.fila * TAM_CELDA + HUD_HEIGHT
        rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
        # Dibujar círculo centrado
        center_x = x + TAM_CELDA // 2
        center_y = y + TAM_CELDA // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), TAM_CELDA // 3)
        # Borde negro
        pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), TAM_CELDA // 3, 2)


class Jugador(Entidad):
    def __init__(self, fila, col):
        super().__init__(fila, col, COLORES_JUEGO['jugador'])
        self.energia = 100
        self.max_energia = 100
        self.recuperacion = 0.15  # Más lento (era 0.5)
        self.consumo_correr = 2

    def puede_acceder(self, terreno):
        return terreno.es_accesible_jugador()

    def correr(self, mapa, df, dc):
        if self.energia >= self.consumo_correr:
            if self.mover(mapa, df, dc):
                self.energia -= self.consumo_correr
                return True
        return False

    def actualizar_energia(self):
        self.energia = min(self.max_energia, self.energia + self.recuperacion)


class Enemigo(Entidad):
    def __init__(self, fila, col):
        super().__init__(fila, col, COLORES_JUEGO['enemigo'])

    def puede_acceder(self, terreno):
        return terreno.es_accesible_enemigo()