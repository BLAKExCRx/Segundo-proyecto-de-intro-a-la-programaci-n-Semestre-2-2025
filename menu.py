#archivo de menu.py
#primero los import's
#
import pygame 
import sys
from puntuacion import Puntuacion #se importa de puntuacion la tabla de puntacion
from config import ANCHO, ALTO, FPS, COLORES # se usa para importar valores como la altura,ancho colores y mas


class Menu:
    """Clase principal .Maneja la interfaz gráfica, 
    entrada de nombre, selección de modo y dificultad,y visualización de high scores"""
    def __init__(self, screen, puntuacion):
        """Inicia el menú con la pantalla y el objeto de puntuación.
    Carga fuentes, colores, fondo, estados iniciales y define rectángulos para elementos UI."""
        self.screen = screen
        self.puntuacion = puntuacion
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('arial', 50, bold=True)
        self.font_subtitle = pygame.font.SysFont('arial', 24, bold=True)
        self.font_button = pygame.font.SysFont('arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
        
        self.colors = COLORES
        
        # Fondo
        try:
            self.background = pygame.image.load('imagenes/fondo_menu.png')
            self.background = pygame.transform.scale(self.background, (ANCHO, ALTO))
        except pygame.error:
            self.background = None
        
        # Estados
        self.state = 'name_input'
        self.nombre = ''
        self.cursor_visible = True
        self.cursor_timer = 0
        self.modo_seleccionado = None
        self.dificultad = 'medio'
        
        self.rects = self._definir_rects()
        
       
    
    def _definir_rects(self):
      #Define las posiciones y tamaños para botones, inputs y paneles.
      #Retorna un diccionario con claves para cada elemento UI.
      #aclaracion del nombre: 'rects' es abreviatura en inglés de 'rectangles' que es lo mas corto de usar.
       
        rects = {}
        rects['input_nombre'] = pygame.Rect(ANCHO - 400, 50, 350, 40)
        rects['panel_modos'] = pygame.Rect(50, 200, 300, 250)
        rects['modo_escapa'] = pygame.Rect(55, 210, 290, 50)
        rects['modo_cazador'] = pygame.Rect(55, 270, 290, 50)
        rects['salir'] = pygame.Rect(55, 390, 290, 50)

        rects['dificil_facil'] = pygame.Rect(ANCHO // 2 - 75, 150, 150, 50)
        rects['dificil_medio'] = pygame.Rect(ANCHO // 2 + 75, 150, 150, 50)
        rects['dificil_dificil'] = pygame.Rect(ANCHO // 2 + 225, 150, 150, 50)

        rects['top_escapa'] = pygame.Rect(ANCHO // 2 - 75, 250, 150, 150)
        rects['top_cazador'] = pygame.Rect(ANCHO // 2 + 125, 250, 150, 150)
        return rects
    # se cambio handle_events por uno mas sencillo, eventos
    def eventos(self, events):
        """Procesa la lista de eventos de Pygame (clics, teclas, etc.).en el esta el cierre, entrada de texto para nombre,
         y clics en botones para modo/dificultad. Retorna True si debe salir o iniciar juego."""
        for event in events:
            if event.type == pygame.QUIT:
                self.state = 'exit'
                return True
            
            if event.type == pygame.KEYDOWN:
                if self.state == 'name_input':
                    if event.key == pygame.K_RETURN:
                        if self.nombre.strip():
                            self.state = 'main_menu'
                    elif event.key == pygame.K_BACKSPACE:
                        self.nombre = self.nombre[:-1]
                    elif len(self.nombre) < 15:
                        self.nombre += event.unicode
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'exit'
                        return True
            
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == 'main_menu':
                pos = pygame.mouse.get_pos()
                if self.rects['modo_escapa'].collidepoint(pos):
                    self.modo_seleccionado = 'escapa'
                    return self._iniciar_juego()
                elif self.rects['modo_cazador'].collidepoint(pos):
                    self.modo_seleccionado = 'cazador'
                    return self._iniciar_juego()
                elif self.rects['salir'].collidepoint(pos):
                    self.state = 'exit'
                    return True
                elif self.rects['dificil_facil'].collidepoint(pos):
                    self.dificultad = 'facil'
                elif self.rects['dificil_medio'].collidepoint(pos):
                    self.dificultad = 'medio'
                elif self.rects['dificil_dificil'].collidepoint(pos):
                    self.dificultad = 'dificil'
        
        return False
    
    def _iniciar_juego(self):
        """Prepara y retorna los datos para iniciar el juego: (modo, dificultad, nombre). Se llama cuando se selecciona un modo."""
        return (self.modo_seleccionado, self.dificultad, self.nombre.strip())
    
    def update(self, dt):
        """Actualiza el estado dinámico del menú, como el parpadeo del cursor.
    'update' en inglés = 'actualizar'"""
        self.cursor_timer += dt
        if self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self):
        """ Dibuja el menú completo en la pantalla: fondo, título, elementos UI, botones y tablas.Dependiendo del estado, 
        muestra input de nombre o menú principal.'draw' = 'dibujar', es mas corto en ingles asi que use ese."""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.colors['bg_dark'])
        
    
        
        # Título
        title_surf = self.font_title.render("ESCAPA DEL LABERINTO", True, self.colors['text_white'])
        self.screen.blit(title_surf, (50, 50))
        
        if self.state == 'name_input':
            prompt = self.font_subtitle.render("Nombre del jugador:", True, self.colors['text_white'])
            self.screen.blit(prompt, (self.rects['input_nombre'].x, self.rects['input_nombre'].y - 30))
            pygame.draw.rect(self.screen, self.colors['input_bg'], self.rects['input_nombre'])
            pygame.draw.rect(self.screen, self.colors['border'], self.rects['input_nombre'], 2)
            text_surf = self.font_button.render(self.nombre, True, self.colors['text_white'])
            self.screen.blit(text_surf, (self.rects['input_nombre'].x + 10, self.rects['input_nombre'].y + 5))
            if self.cursor_visible:
                cursor = self.font_button.render('|', True, self.colors['text_white'])
                self.screen.blit(cursor, (self.rects['input_nombre'].x + 10 + text_surf.get_width(), self.rects['input_nombre'].y + 5))
        
        elif self.state == 'main_menu':
            mouse_pos = pygame.mouse.get_pos()
            
            # Panel modos
            pygame.draw.rect(self.screen, self.colors['bg_panel'], self.rects['panel_modos'], border_radius=20)
            
            # Botones modos
            for btn_name in ['modo_escapa', 'modo_cazador', 'salir']:
                rect = self.rects[btn_name]
                color = self.colors['bg_button']
                if rect.collidepoint(mouse_pos):
                    color = self.colors['bg_button_hover']
                if btn_name == f'modo_{self.modo_seleccionado}':
                    color = self.colors['bg_button_selected']
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                text = {'modo_escapa': 'MODO ESCAPA', 'modo_cazador': 'MODO CAZADOR', 'salir': 'SALIR'}[btn_name]
                text_surf = self.font_button.render(text, True, self.colors['text_white'])
                text_rect = text_surf.get_rect(left=rect.left + 10, centery=rect.centery)
                self.screen.blit(text_surf, text_rect)
            
            # Label dificultad
            label_diff = self.font_subtitle.render("Seleccionar Dificultad", True, self.colors['text_white'])
            self.screen.blit(label_diff, (self.rects['dificil_facil'].x, self.rects['dificil_facil'].y - 30))
            
            # Botones dificultad
            diffs = ['facil', 'medio', 'dificil']
            for i, diff in enumerate(diffs):
                rect = [self.rects['dificil_facil'], self.rects['dificil_medio'], self.rects['dificil_dificil']][i]
                color = self.colors['bg_button'] if diff != self.dificultad else self.colors['bg_button_selected']
                if rect.collidepoint(mouse_pos):
                    color = self.colors['bg_button_hover'] if diff != self.dificultad else self.colors['bg_button_selected']
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                text_surf = self.font_button.render(diff.upper(), True, self.colors['text_white'])
                text_rect = text_surf.get_rect(center=rect.center)
                self.screen.blit(text_surf, text_rect)
            
            # Label mejores puntajes
            label_mejores = self.font_subtitle.render("Mejores Puntajes", True, self.colors['text_white'])
            self.screen.blit(label_mejores, (self.rects['top_escapa'].x, self.rects['top_escapa'].y - 30))
            
            # Tops
            for modo, rect in [('escapa', self.rects['top_escapa']), ('cazador', self.rects['top_cazador'])]:
                pygame.draw.rect(self.screen, self.colors['bg_panel'], rect)
                title = f"TOP 5 {modo.upper()}"
                title_surf = self.font_small.render(title, True, self.colors['text_white'])
                self.screen.blit(title_surf, (rect.x + 10, rect.y + 5))
                top5 = self.puntuacion.get_top5(modo)
                y_start = rect.y + 30
                for i in range(5):
                    score = top5[i] if i < len(top5) else {'nombre': '', 'puntaje': 0}
                    pos_text = self.font_small.render(f"{i+1}.", True, self.colors['text_white'])
                    score_text = self.font_small.render(str(score['puntaje']), True, self.colors['text_white'])
                    self.screen.blit(pos_text, (rect.x + 10, y_start + i*25))
                    self.screen.blit(score_text, (rect.x + 40, y_start + i*25))
    
    def run(self):
        """
    Ejecuta el loop principal del menú: procesa eventos, actualiza y dibuja.
    Continúa hasta seleccionar modo (inicia juego) o salir.
    'run' = 'ejecutar" es mas corto.
    """
        running = True
        while running:
            dt = self.clock.tick(FPS)
            events = pygame.event.get()
            
            if self.eventos(events):
                if self.state == 'exit':
                    return None
                else:
                    return self._iniciar_juego()
            
            self.update(dt)
            self.draw()
            pygame.display.flip()
        return None