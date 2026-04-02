# self_coder: modulo_bienvenida.py

import random

class ModuloBienvenida:
    def __init__(self):
        self.mensajes_motivacionales = [
            "¡Hoy es un nuevo día, llena de oportunidades!",
            "No te rindas, cada obstáculo es una oportunidad para crecer.",
            "La perseverancia es la clave para alcanzar tus metas.",
            "Cada pequeño paso lleva a un gran logro.",
            "No te dejes llevar por la duda, sigue adelante.",
            "La confianza en uno mismo es la base de todo éxito.",
            "No te compares con los demás, compara con tu propio potencial.",
            "La motivación es la fuerza que impulsa a hacer lo imposible.",
            "Cada error es una oportunidad para aprender y mejorar.",
            "La pasión y la dedicación son las claves para alcanzar tus objetivos."
        ]

    def obtener_mensaje_motivacional(self):
        try:
            mensaje = random.choice(self.mensajes_motivacionales)
            return mensaje
        except Exception as e:
            print(f"Error al obtener mensaje motivacional: {str(e)}")
            return None

def main():
    modulo = ModuloBienvenida()
    mensaje = modulo.obtener_mensaje_motivacional()
    if mensaje:
        print(f"Bienvenido, aquí tienes un mensaje motivacional: {mensaje}")

if __name__ == "__main__":
    main()