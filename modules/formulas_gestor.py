import json
import os

class GestorFormulas:
    def __init__(self, archivo='formulas.json'):
        self.archivo = archivo
        self.formulas = self.cargar_formulas()

    def cargar_formulas(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                return json.load(f)
        else:
            return {}

    def guardar_formulas(self):
        with open(self.archivo, 'w') as f:
            json.dump(self.formulas, f, indent=4)

    def agregar_formula(self, nombre, descripcion, categoria):
        try:
            if nombre in self.formulas:
                print("Error: La fórmula ya existe.")
                return
            self.formulas[nombre] = {'descripcion': descripcion, 'categoria': categoria}
            self.guardar_formulas()
            print("Fórmula agregada con éxito.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def buscar_formula(self, nombre=None, categoria=None):
        try:
            if nombre:
                return self.formulas.get(nombre)
            elif categoria:
                return {nombre: formula for nombre, formula in self.formulas.items() if formula['categoria'] == categoria}
            else:
                print("Error: Debes proporcionar un nombre o categoría para buscar.")
                return {}
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}

    def listar_formulas(self):
        try:
            return self.formulas
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}

    def eliminar_formula(self, nombre):
        try:
            if nombre in self.formulas:
                del self.formulas[nombre]
                self.guardar_formulas()
                print("Fórmula eliminada con éxito.")
            else:
                print("Error: La fórmula no existe.")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    gestor = GestorFormulas()
    while True:
        print("\n1. Agregar fórmula")
        print("2. Buscar fórmula")
        print("3. Listar fórmulas")
        print("4. Eliminar fórmula")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nombre = input("Ingrese el nombre de la fórmula: ")
            descripcion = input("Ingrese la descripción de la fórmula: ")
            categoria = input("Ingrese la categoría de la fórmula: ")
            gestor.agregar_formula(nombre, descripcion, categoria)
        elif opcion == "2":
            nombre = input("Ingrese el nombre de la fórmula (opcional): ")
            categoria = input("Ingrese la categoría de la fórmula (opcional): ")
            resultado = gestor.buscar_formula(nombre, categoria)
            if resultado:
                print(json.dumps(resultado, indent=4))
        elif opcion == "3":
            print(json.dumps(gestor.listar_formulas(), indent=4))
        elif opcion == "4":
            nombre = input("Ingrese el nombre de la fórmula a eliminar: ")
            gestor.eliminar_formula(nombre)
        elif opcion == "5":
            break
        else:
            print("Error: Opción inválida.")

if __name__ == "__main__":
    main()