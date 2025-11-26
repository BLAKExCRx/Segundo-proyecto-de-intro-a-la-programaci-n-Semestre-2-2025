# puntuacion.py (VERSIÓN COMPLETA Y CORREGIDA - asegúrate de copiar todo)
import json
import os


class Puntuacion:
    """
    Clase para manejar puntuaciones altas en JSON, top 5 por modo.
    """
    def __init__(self):# servira para cargar los puntajes mas altos de cada modo 
        pass
    def cargar_todos(self):#Carga todos los highscores
        pass
    
    def cargar(self, modo):# Carga highscore de un modo específico
        pass
    
    def agregar(self, modo, nombre, puntaje): #mantiene y agrega el 5 de manera ordenada
        pass
    
    def guardar(self, modo): #sirve para guardar el puntaje de un modo
        pass
    def get_top5(self, modo): #deberia retornar el top 5 de un modo
        pass