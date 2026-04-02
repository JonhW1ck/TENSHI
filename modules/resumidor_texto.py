import json
import os

class Resumidor:
    def __init__(self):
        self.conocimiento = {}

    def resumir_texto(self, texto):
        try:
            oraciones = texto.split('.')
            oraciones = [oracion.strip() for oracion in oraciones]
            oraciones = [oracion for oracion in oraciones if oracion]
            resumen = [oracion for oracion in oraciones[:5]]
            return '\n'.join(resumen)
        except Exception as e:
            print(f"Error resumiendo texto: {e}")

    def guardar_resumen(self, resumen, tema, categoria):
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            if tema not in self.conocimiento:
                self.conocimiento[tema] = {}
            if categoria not in self.conocimiento[tema]:
                self.conocimiento[tema][categoria] = []
            self.conocimiento[tema][categoria].append({
                'fecha': fecha,
                'resumen': resumen
            })
            self.guardar_conocimiento()
            return True
        except Exception as e:
            print(f"Error guardando resumen: {e}")
            return False

    def guardar_conocimiento(self):
        try:
            with open('memory/conocimiento.json', 'w') as f:
                json.dump(self.conocimiento, f)
        except Exception as e:
            print(f"Error guardando conocimiento: {e}")

    def listar_conocimiento(self):
        try:
            if os.path.exists('memory/conocimiento.json'):
                with open('memory/conocimiento.json', 'r') as f:
                    conocimiento = json.load(f)
                    for tema in conocimiento:
                        print(f"Tema: {tema}")
                        for categoria in conocimiento[tema]:
                            print(f"Categoria: {categoria}")
                            for resumen in conocimiento[tema][categoria]:
                                print(f"Fecha: {resumen['fecha']}, Resumen: {resumen['resumen']}")
                            print()
        except Exception as e:
            print(f"Error listando conocimiento: {e}")

    def buscar_conocimiento(self, tema=None, categoria=None):
        try:
            if os.path.exists('memory/conocimiento.json'):
                with open('memory/conocimiento.json', 'r') as f:
                    conocimiento = json.load(f)
                    resultados = []
                    if tema:
                        if tema in conocimiento:
                            resultados.extend(conocimiento[tema])
                    if categoria:
                        for tema in conocimiento:
                            if categoria in conocimiento[tema]:
                                resultados.extend(conocimiento[tema][categoria])
                    return resultados
        except Exception as e:
            print(f"Error buscando conocimiento: {e}")
        return []

import datetime
self_coder = Resumidor()