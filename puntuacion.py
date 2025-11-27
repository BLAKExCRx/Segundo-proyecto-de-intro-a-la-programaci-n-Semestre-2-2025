# puntuacion.py el archivo deberia estar terminado, mas puede haber cambios a futuro 
#  debo copiar bien el codigo en la copia de seguridad por si acaso como la vez pasada
import json
import os
from config import ARCHIVOS_HIGHSCORES

class Puntuacion:
    
    #Clase para manejar puntuaciones altas en JSON, top 5 por modo.
    
    def __init__(self):
        self.archivos = ARCHIVOS_HIGHSCORES
        self.scores = {'escapa': [], 'cazador': []}
        self.cargar_todos()
    
    def cargar_todos(self):
        """Carga todos los highscores."""
        for modo, archivo in self.archivos.items():
            self.cargar(modo)
    
    def cargar(self, modo):
        """Carga highscore de un modo específico."""
        archivo = self.archivos[modo]
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.scores[modo] = [{'nombre': item['nombre'], 'puntaje': item['puntaje']} for item in data]
            except (json.JSONDecodeError, KeyError):
                self.scores[modo] = []
        else:
            self.scores[modo] = []
    
    def agregar(self, modo, nombre, puntaje):
        """Agrega puntaje y mantiene top 5 ordenado."""
        self.scores[modo].append({'nombre': nombre, 'puntaje': puntaje})
        self.scores[modo] = sorted(self.scores[modo], key=lambda x: x['puntaje'], reverse=True)[:5]
        self.guardar(modo)
    
    def guardar(self, modo):
        """Guarda highscore de un modo."""
        archivo = self.archivos[modo]
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(self.scores[modo], f, indent=4, ensure_ascii=False)
        except Exception:
            pass  # Silencioso si falla
    
    def get_top5(self, modo):
        """Retorna top 5 de un modo (lista de dicts)."""
        return self.scores.get(modo, [])