# juego.py
import pygame
import sys
import random
from collections import deque
from config import ANCHO, ALTO, FPS, HUD_HEIGHT, COLORES, TAM_CELDA, COLORES_JUEGO
from mapa import Mapa
from entidades import Jugador, Enemigo, Trampa, Camino, Liana, Tunel 
from puntuacion import Puntuacion

class Juego:
    def __init__(self, modo, dificultad, nombre_jugador, screen, puntuacion):
        self.modo = modo
        self.dificultad = dificultad
        self.nombre_jugador = nombre_jugador
        self.screen = screen
        self.puntuacion = puntuacion
        self.clock = pygame.time.Clock()
        self.font_hud = pygame.font.SysFont('arial', 18, bold=True)
        self.font_pausa = pygame.font.SysFont('arial', 36, bold=True)
        self.font_menu_pausa = pygame.font.SysFont('arial', 24, bold=True)
        self.font_game_over = pygame.font.SysFont('arial', 48, bold=True)
        self.running = True
        self.pausado = False
        self.volver_menu = False
        self.game_over = False
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_limite = self._get_tiempo_limite()
        self.tiempo_actual = 0
        self.tiempo_pausado = 0
        
        # Sistema de puntuación actualizado
        if self.modo == 'escapa':
            self.puntaje = 3000  # Empieza con 3000 puntos
            self.puntaje_resta_timer = 0  # Timer para restar puntos cada 2 segundos
            self.puntaje_resta_delay = 2000  # 2 segundos en ms
            self.puntaje_resta_cantidad = self._get_puntaje_resta()
        else:
            self.puntaje = 0  # Empieza con 0 puntos en modo cazador
        
        self.mapa = Mapa(self.modo)
        self.inicio = self.mapa.inicio
        self.salida = self.mapa.salida
        self.jugador = Jugador(self.inicio[0], self.inicio[1])
        
        # Sistema de enemigos
        self.num_enemigos_total = 3
        self.enemigos = []
        self.enemigos_data = []
        self._inicializar_enemigos()
        
        # Sistema de trampas actualizado
        self.trampas_activas = []
        self.max_trampas_activas = 3
        self.trampas_disponibles = 0  # Empieza con 0 trampas
        self.trampa_recarga_timer = 0  # Timer para recargar trampas
        self.trampa_recarga_delay = 5000  # 5 segundos en ms
        
        # Timers de IA
        self.enemigo_timer = 0
        self.enemigo_delay = self._get_enemigo_delay()
        
        # Menú de pausa
        self.opciones_pausa = ['Continuar', 'Reiniciar', 'Salir al Menu']
        self.opcion_seleccionada = 0

    def _get_tiempo_limite(self):
        """Define el tiempo límite para ambos modos."""
        if self.dificultad == 'facil':
            return 240000  # 4 minutos
        elif self.dificultad == 'normal':
            return 180000  # 3 minutos
        else:
            return 120000  # 2 minutos

    def _get_puntaje_resta(self):
        """Retorna cuántos puntos se restan cada 2 segundos en modo escapa."""
        if self.dificultad == 'facil':
            return 10
        elif self.dificultad == 'normal':
            return 20
        else:
            return 30

    def _get_enemigo_delay(self):
        """Retorna el delay en ms entre movimientos de enemigos según dificultad."""
        if self.dificultad == 'facil':
            return 500
        elif self.dificultad == 'normal':
            return 300
        else:
            return 200

    def _posicion_aleatoria_valida(self, es_enemigo=False):
        """Busca una posición válida para entidades."""
        valid_pos = self.mapa.valid_spawn[:]
        random.shuffle(valid_pos)

        for r, c in valid_pos:
            if not any(e.fila == r and e.col == c for e in self.enemigos):
                if es_enemigo and self.modo == 'escapa':
                    distancia = self._distancia(self.jugador, Enemigo(r, c))
                    if distancia >= 6:
                        return r, c
                elif not es_enemigo:
                    return r, c
        
        if valid_pos:
            return random.choice(valid_pos)
            
        return 1, 1
    def _inicializar_enemigos(self):
        """Inicializa los 3 slots de enemigos."""
        self.enemigos.clear()
        self.enemigos_data.clear()
        
        posiciones_ocupadas = set()

        for i in range(self.num_enemigos_total):
            pos = self._posicion_aleatoria_valida(es_enemigo=True)
            r, c = pos
            
            if pos is not None and (r, c) not in posiciones_ocupadas:
                nuevo_enemigo = Enemigo(r, c)
                self.enemigos.append(nuevo_enemigo)
                self.enemigos_data.append({'id': i, 'enemigo': nuevo_enemigo, 'timer_activo': False})
                posiciones_ocupadas.add((r, c))
            else:
                self.enemigos_data.append({'id': i, 'enemigo': None, 'timer_activo': False})
                self._programar_reaparicion_enemigo(i, 3000)

    def _programar_reaparicion_enemigo(self, enemigo_id, tiempo=10000):
        """Programa la reaparición de un enemigo por su ID."""
        event_id = pygame.USEREVENT + 10 + enemigo_id
        pygame.time.set_timer(event_id, tiempo, 1)
        
        for data in self.enemigos_data:
            if data['id'] == enemigo_id:
                data['timer_activo'] = True
                break

    def _reaparecer_enemigo(self, enemigo_id):
        """Reaparece un enemigo en una posición válida."""
        enemigo_data = next((data for data in self.enemigos_data if data['id'] == enemigo_id), None)
        if not enemigo_data:
            return

        pos = self._posicion_aleatoria_valida(es_enemigo=True)
        if pos is None:
            return
        r, c = pos
        
        nuevo_enemigo = Enemigo(r, c)
        self.enemigos.append(nuevo_enemigo)
        enemigo_data['enemigo'] = nuevo_enemigo
        enemigo_data['timer_activo'] = False
    
    def _manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Eventos de reaparición de enemigos
            if event.type >= pygame.USEREVENT + 10 and event.type < pygame.USEREVENT + 10 + self.num_enemigos_total:
                enemigo_id = event.type - (pygame.USEREVENT + 10)
                self._reaparecer_enemigo(enemigo_id)
                pygame.time.set_timer(event.type, 0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.pausado and not self.game_over:
                        self.tiempo_pausado = pygame.time.get_ticks()
                        self.pausado = True
                        self.opcion_seleccionada = 0
                    elif self.pausado:
                        pausa_duracion = pygame.time.get_ticks() - self.tiempo_pausado
                        self.tiempo_inicio += pausa_duracion
                        self.pausado = False
                    elif self.game_over:
                        self.running = False
                        self.volver_menu = True
                
                if self.pausado:
                    if event.key == pygame.K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones_pausa)
                    elif event.key == pygame.K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones_pausa)
                    elif event.key == pygame.K_RETURN:
                        self._ejecutar_opcion_pausa()
                
                if not self.pausado and not self.game_over:
                    self._manejar_movimiento(event.key)
                    if event.key == pygame.K_SPACE and self.modo == 'escapa':
                        self._colocar_trampa()
    
    def _ejecutar_opcion_pausa(self):
        """Ejecuta la opción seleccionada en el menú de pausa."""
        if self.opcion_seleccionada == 0:  # Continuar
            pausa_duracion = pygame.time.get_ticks() - self.tiempo_pausado
            self.tiempo_inicio += pausa_duracion
            self.pausado = False
        elif self.opcion_seleccionada == 1:  # Reiniciar
            self.__init__(self.modo, self.dificultad, self.nombre_jugador, self.screen, self.puntuacion)
        elif self.opcion_seleccionada == 2:  # Salir al menú
            self.volver_menu = True
            self.running = False
    

    def _manejar_movimiento(self, key):
        direcciones = {pygame.K_UP: (-1, 0), pygame.K_DOWN: (1, 0), pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1)}
        
        keys = pygame.key.get_pressed()
        corriendo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        
        df, dc = direcciones.get(key, (0, 0))
        if df or dc:
            if corriendo:
                self.jugador.correr(self.mapa, df, dc, self.modo)
            else:
                self.jugador.mover(self.mapa, df, dc, self.modo)


    def _colocar_trampa(self):
        """Coloca una trampa si hay disponibles."""
        # Verificar que haya trampas disponibles
        if self.trampas_disponibles <= 0:
            print("No hay trampas disponibles")
            return
        
        # Verificar límite de trampas activas
        if len(self.trampas_activas) >= self.max_trampas_activas:
            print(f"Límite de {self.max_trampas_activas} trampas activas alcanzado.")
            return

        posicion = (self.jugador.fila, self.jugador.col)
        
        # Verificar que la posición actual sea válida
        terreno_actual = self.mapa.matriz[posicion[0]][posicion[1]]
        if not isinstance(terreno_actual, Camino) and not isinstance(terreno_actual, Tunel):
            return
        
        # Verificar que no bloquea el camino único
        if not self._bloquea_camino_unico(posicion):
            trampa = Trampa()
            self.mapa.matriz[self.jugador.fila][self.jugador.col] = trampa
            self.trampas_activas.append(posicion)
            self.trampas_disponibles -= 1  # Consumir una trampa
            print(f"Trampa colocada. Disponibles: {self.trampas_disponibles}, Activas: {len(self.trampas_activas)}")
        else:
            print("No se puede colocar trampa aquí - bloquea el camino")

    def _bloquea_camino_unico(self, posicion):
        """Verifica si colocar trampa en esta posición bloquea el único camino."""
        fila, col = posicion
        terreno_original = self.mapa.matriz[fila][col]
        
        self.mapa.matriz[fila][col] = Trampa()
        
        try:
            hay_camino = self.mapa.hay_camino(self.mapa.inicio, self.salida, es_jugador=True)
        except AttributeError:
            hay_camino = True
             
        self.mapa.matriz[fila][col] = terreno_original
        
        return not hay_camino

    def _actualizar(self, dt):
        keys = pygame.key.get_pressed()
        moviendo = any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]])
        
        if not moviendo:
            self.jugador.actualizar_energia()
        
        self._actualizar_tiempo(dt)
        self._actualizar_puntaje(dt)
        self._actualizar_recarga_trampas(dt)
        
        self.enemigo_timer += dt
        if self.enemigo_timer >= self.enemigo_delay:
            self._mover_enemigos()
            self.enemigo_timer = 0
        
        self._verificar_colisiones()
        self._verificar_victoria_derrota()

    def _actualizar_tiempo(self, dt):
        """Actualiza el tiempo según el modo."""
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_inicio
        
        if self.modo == 'escapa':
            # En modo escapa, el tiempo suma normalmente
            self.tiempo_actual = tiempo_transcurrido
        else:
            # En modo cazador, el tiempo resta desde el límite
            self.tiempo_actual = self.tiempo_limite - tiempo_transcurrido
            
            # Verificar si se acabó el tiempo
            if self.tiempo_actual <= 0:
                self.tiempo_actual = 0
                self._terminar_juego("¡TIEMPO AGOTADO!")

    def _actualizar_puntaje(self, dt):
        """Actualiza el sistema de puntuación."""
        if self.modo == 'escapa':
            # Restar puntos cada 2 segundos
            self.puntaje_resta_timer += dt
            if self.puntaje_resta_timer >= self.puntaje_resta_delay:
                self.puntaje = max(0, self.puntaje - self.puntaje_resta_cantidad)
                self.puntaje_resta_timer = 0
                
                # Si llega a 0 puntos, game over
                if self.puntaje <= 0:
                    self._terminar_juego("¡PUNTOS AGOTADOS!")



    def _actualizar_recarga_trampas(self, dt):
        """Recarga trampas cada 5 segundos hasta un máximo de 3."""
        if self.modo == 'escapa':
            self.trampa_recarga_timer += dt
            if self.trampa_recarga_timer >= self.trampa_recarga_delay:
                if self.trampas_disponibles < self.max_trampas_activas:
                    self.trampas_disponibles += 1
                    print(f"Trampa recargada. Disponibles: {self.trampas_disponibles}")
                self.trampa_recarga_timer = 0

    def _terminar_juego(self, mensaje):
        """Termina el juego mostrando un mensaje."""
        print(f"Juego terminado: {mensaje}")
        self.game_over = True
        self.mensaje_game_over = mensaje
        
        # Guardar puntuación solo si:
        # 1. En modo escapa: Solo si escapó exitosamente (no si fue atrapado)
        # 2. En modo cazador: Siempre guardar
        if self.puntaje > 0:
            if self.modo == 'escapa':
                # Solo guardar si NO fue atrapado
                if mensaje != "¡ATRAPADO!":
                    self.puntuacion.agregar(self.modo, self.nombre_jugador, self.puntaje)
            else:
                # En modo cazador siempre guardar
                self.puntuacion.agregar(self.modo, self.nombre_jugador, self.puntaje)

    def _mover_enemigos(self):
        """Maneja la IA de los enemigos."""
        enemigos_activos = [data['enemigo'] for data in self.enemigos_data if data['enemigo']]

        for enemigo in enemigos_activos[:]: 
            path = []
            
            if self.modo == 'escapa':
                path = self.mapa.encontrar_camino(
                    enemigo.fila, enemigo.col, 
                    self.jugador.fila, self.jugador.col, 
                    es_rol_cazador=True
                )
            else:
                distancia = self._distancia(enemigo, self.jugador)
                
                if distancia <= 4: 
                    max_dist = -1
                    best_move = (0, 0)
                    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nf, nc = enemigo.fila + df, enemigo.col + dc
                        if self.mapa.es_celda_accesible(nf, nc, es_jugador=True):
                            temp_dist = self._distancia(self.jugador, Enemigo(nf, nc))
                            if temp_dist > max_dist:
                                max_dist = temp_dist
                                best_move = (df, dc)
                    
                    if best_move != (0, 0):
                        enemigo.mover(self.mapa, best_move[0], best_move[1], self.modo)
                        continue
                
                path = self.mapa.encontrar_camino(
                    enemigo.fila, enemigo.col, 
                    self.salida[0], self.salida[1], 
                    es_rol_cazador=False
                )
            
            if path and len(path) > 1:
                next_fila, next_col = path[1]
                
                ocupada_enemigo = any(
                    e.fila == next_fila and e.col == next_col 
                    for e in enemigos_activos if e != enemigo
                )
                
                if ocupada_enemigo:
                    continue
                
                enemigo.mover(self.mapa, next_fila - enemigo.fila, next_col - enemigo.col, self.modo)
            
            # Verificar trampa
            if self.modo == 'escapa' and isinstance(self.mapa.matriz[enemigo.fila][enemigo.col], Trampa):
                print("¡Cazador atrapado en una trampa!")
                self.puntaje += 50  # Bonus por atrapar
                
                trampa_pos = (enemigo.fila, enemigo.col)
                
                self.mapa.matriz[enemigo.fila][enemigo.col] = Camino() 
                if trampa_pos in self.trampas_activas:
                    self.trampas_activas.remove(trampa_pos)
                
                if enemigo in self.enemigos:
                    self.enemigos.remove(enemigo)
                
                enemigo_data = next((data for data in self.enemigos_data if data.get('enemigo') == enemigo), None)
                if enemigo_data:
                    enemigo_data['enemigo'] = None
                    self._programar_reaparicion_enemigo(enemigo_data['id'])

    def _distancia(self, e1, e2):
        return abs(e1.fila - e2.fila) + abs(e1.col - e2.col)

    def _verificar_colisiones(self):
        """Verifica colisiones jugador-enemigo."""
        for enemigo in [data['enemigo'] for data in self.enemigos_data if data['enemigo']]:
            if (enemigo.fila, enemigo.col) == (self.jugador.fila, self.jugador.col):
                if self.modo == 'escapa':
                    self._terminar_juego("¡ATRAPADO!")
                else:
                    print("¡Presa atrapada!")
                    self.puntaje += 20
                    self.enemigos.remove(enemigo)
                    
                    enemigo_data = next((data for data in self.enemigos_data if data['enemigo'] == enemigo), None)
                    if enemigo_data:
                        enemigo_data['enemigo'] = None
                        self._programar_reaparicion_enemigo(enemigo_data['id'])
                    
                    break

    def _verificar_victoria_derrota(self):
        """Verifica condiciones de victoria y derrota."""
        if (self.jugador.fila, self.jugador.col) == self.mapa.salida:
            if self.modo == 'escapa':
                self._terminar_juego("¡ESCAPE EXITOSO!")
        
        if self.modo == 'cazador':
            for enemigo in [data['enemigo'] for data in self.enemigos_data if data['enemigo']]:
                if (enemigo.fila, enemigo.col) == self.mapa.salida:
                    print("¡Presa escapó!")
                    self.puntaje = max(0, self.puntaje - 10)
                    
                    self.enemigos.remove(enemigo)
                    
                    enemigo_data = next((data for data in self.enemigos_data if data['enemigo'] == enemigo), None)
                    if enemigo_data:
                        enemigo_data['enemigo'] = None
                        self._programar_reaparicion_enemigo(enemigo_data['id'])

    def _dibujar(self):
        self.screen.fill(COLORES['bg_dark'])
        self.mapa.dibujar(self.screen)
        
        for enemigo in [data['enemigo'] for data in self.enemigos_data if data['enemigo']]:
            enemigo.dibujar(self.screen)

        self.jugador.dibujar(self.screen)
        self._dibujar_hud()
        
        if self.pausado:
            self._dibujar_menu_pausa()
        
        if self.game_over:
            self._dibujar_game_over()


    def _dibujar_game_over(self):
        """Dibuja la pantalla de game over."""
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_game_over.render(self.mensaje_game_over, True, COLORES['text_yellow'])
        game_over_rect = game_over_text.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        # Solo mostrar puntaje si NO fue atrapado en modo escapa
        if not (self.modo == 'escapa' and self.mensaje_game_over == "¡ATRAPADO!"):
            puntaje_text = self.font_pausa.render(f"Puntaje Final: {self.puntaje}", True, COLORES['text_white'])
            puntaje_rect = puntaje_text.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
            self.screen.blit(puntaje_text, puntaje_rect)
            y_instruccion = ALTO // 2 + 80
        else:
            # Si fue atrapado, no mostrar puntaje
            y_instruccion = ALTO // 2 + 20

        instruccion_text = self.font_menu_pausa.render("Presiona ESC para volver al menú", True, COLORES['text_white'])
        instruccion_rect = instruccion_text.get_rect(center=(ANCHO // 2, y_instruccion))
        self.screen.blit(instruccion_text, instruccion_rect)

    def _dibujar_menu_pausa(self):
        """Dibuja el menú de pausa."""
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        menu_width = 300
        menu_height = 200
        menu_x = (ANCHO - menu_width) // 2
        menu_y = (ALTO - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, COLORES['bg_panel'], menu_rect)
        pygame.draw.rect(self.screen, COLORES['border'], menu_rect, 2)

        titulo_text = self.font_pausa.render("PAUSA", True, COLORES['text_white'])
        self.screen.blit(titulo_text, (menu_x + (menu_width - titulo_text.get_width()) // 2, menu_y + 20))

        for i, opcion in enumerate(self.opciones_pausa):
            color = COLORES['bg_button_selected'] if i == self.opcion_seleccionada else COLORES['text_white']
            opcion_text = self.font_menu_pausa.render(opcion, True, color)
            self.screen.blit(opcion_text, (menu_x + (menu_width - opcion_text.get_width()) // 2, menu_y + 80 + i * 40))
    def _dibujar_hud(self):
        """Dibuja el HUD actualizado."""
        hud_rect = pygame.Rect(0, 0, ANCHO, HUD_HEIGHT)
        pygame.draw.rect(self.screen, COLORES['bg_panel'], hud_rect)
        
        x_offset = 10
        spacing = 150
        
        # Energía
        energia_porcentaje = int((self.jugador.energia / self.jugador.max_energia) * 100)
        energia_text = self.font_hud.render(f"Energia: {energia_porcentaje}%", True, COLORES['text_white'])
        self.screen.blit(energia_text, (x_offset, 18))
        x_offset += spacing + 20
        
        # Trampas (solo modo escapa)
        if self.modo == 'escapa':
            trampas_text = self.font_hud.render(f"Trampas: {self.trampas_disponibles}/3", True, COLORES['text_white'])
            self.screen.blit(trampas_text, (x_offset, 18))
            x_offset += spacing
        else:
            x_offset += 50
        
        # Tiempo (siempre suma ahora)
        tiempo_seg = self.tiempo_actual // 1000
        minutos = tiempo_seg // 60
        segundos = tiempo_seg % 60
        tiempo_text = self.font_hud.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, COLORES['text_white'])
        self.screen.blit(tiempo_text, (x_offset, 18))
        x_offset += spacing + 20
        
        # Puntaje
        puntaje_text = self.font_hud.render(f"Puntaje: {self.puntaje}", True, COLORES['text_white'])
        self.screen.blit(puntaje_text, (x_offset, 18))
        x_offset += spacing + 30
        
        # ESC=Menu
        esc_text = self.font_hud.render("ESC=Menu", True, COLORES['text_yellow'])
        self.screen.blit(esc_text, (x_offset, 18))
        
        # Jugador
        jugador_text = self.font_hud.render(f"Jugador: {self.nombre_jugador}", True, COLORES['text_white'])
        self.screen.blit(jugador_text, (ANCHO - 200, 18))

    def run(self):
        """Loop principal del juego."""
        while self.running:
            dt = self.clock.tick(FPS)
            self._manejar_eventos()

            if not self.pausado and not self.game_over:
                self._actualizar(dt)
            
            self._dibujar()
            pygame.display.flip()
            
        return self.volver_menu