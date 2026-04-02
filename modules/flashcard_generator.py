import json
import os
import random
import shutil

class Flashcards:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.flashcards = []

    def crear_flashcard(self, pregunta, respuesta, tema):
        try:
            flashcard = {
                "pregunta": pregunta,
                "respuesta": respuesta,
                "tema": tema
            }
            self.flashcards.append(flashcard)
            self.guardar_flashcards()
            return flashcard
        except Exception as e:
            print(f"Error al crear flashcard: {e}")

    def guardar_flashcards(self):
        try:
            with open(self.ruta_archivo, "w") as archivo:
                json.dump(self.flashcards, archivo)
        except Exception as e:
            print(f"Error al guardar flashcards: {e}")

    def obtener_flashcard_aleatoria(self):
        try:
            if not self.flashcards:
                return None
            return random.choice(self.flashcards)
        except Exception as e:
            print(f"Error al obtener flashcard aleatoria: {e}")

    def obtener_flashcards_por_tema(self, tema):
        try:
            return [flashcard for flashcard in self.flashcards if flashcard["tema"] == tema]
        except Exception as e:
            print(f"Error al obtener flashcards por tema: {e}")

    def listar_temas(self):
        try:
            temas = set(flashcard["tema"] for flashcard in self.flashcards)
            return list(temas)
        except Exception as e:
            print(f"Error al listar temas: {e}")

def crear_archivo_json(ruta_archivo):
    try:
        if not os.path.exists(os.path.dirname(ruta_archivo)):
            os.makedirs(os.path.dirname(ruta_archivo))
        if not os.path.exists(ruta_archivo):
            with open(ruta_archivo, "w") as archivo:
                json.dump([], archivo)
    except Exception as e:
        print(f"Error al crear archivo JSON: {e}")

def self_coder():
    crear_archivo_json("memory/flashcards.json")
    flashcards = Flashcards("memory/flashcards.json")
    return flashcards