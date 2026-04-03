import json
import os

def crear_perfil(nombre, carrera, semestre, materias, proyectos, notas):
    try:
        perfil = {
            "nombre": nombre,
            "carrera": carrera,
            "semestre": semestre,
            "materias": materias,
            "proyectos": proyectos,
            "notas": notas
        }
        with open("memory/perfil.json", "w") as archivo:
            json.dump(perfil, archivo)
    except Exception as e:
        print(f"Error al crear perfil: {e}")

def cargar_perfil():
    try:
        if os.path.exists("memory/perfil.json"):
            with open("memory/perfil.json", "r") as archivo:
                return json.load(archivo)
        else:
            return None
    except Exception as e:
        print(f"Error al cargar perfil: {e}")
        return None

def actualizar_campo(campo, valor):
    try:
        perfil = cargar_perfil()
        if perfil:
            perfil[campo] = valor
            with open("memory/perfil.json", "w") as archivo:
                json.dump(perfil, archivo)
        else:
            print("No hay perfil cargado")
    except Exception as e:
        print(f"Error al actualizar campo: {e}")

if __name__ == "__main__":
    crear_perfil("Juan Pérez", "Ingeniería en Sistemas", 5, ["Matemáticas", "Física", "Química"], ["Proyecto 1", "Proyecto 2"], [8, 9, 7])
    perfil = cargar_perfil()
    print(perfil)
    actualizar_campo("nombre", "Juanito Pérez")
    perfil = cargar_perfil()
    print(perfil)