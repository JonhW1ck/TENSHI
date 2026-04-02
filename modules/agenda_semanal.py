import json
import os

class AgendaSemana:
    def __init__(self):
        self.agenda = []

    def agregar_evento(self, dia, hora, materia, tipo):
        try:
            evento = {
                'dia': dia,
                'hora': hora,
                'materia': materia,
                'tipo': tipo
            }
            self.agenda.append(evento)
            self.guardar_agenda()
            return True
        except Exception as e:
            print(f"Error al agregar evento: {str(e)}")
            return False

    def listar_eventos_dia(self, dia):
        try:
            eventos_dia = [evento for evento in self.agenda if evento['dia'] == dia]
            return eventos_dia
        except Exception as e:
            print(f"Error al listar eventos del día: {str(e)}")
            return []

    def listar_semana(self):
        try:
            self.agenda.sort(key=lambda x: (x['dia'], x['hora']))
            return self.agenda
        except Exception as e:
            print(f"Error al listar la semana: {str(e)}")
            return []

    def eliminar_evento(self, indice):
        try:
            if indice < len(self.agenda):
                del self.agenda[indice]
                self.guardar_agenda()
                return True
            else:
                print("Índice inválido")
                return False
        except Exception as e:
            print(f"Error al eliminar evento: {str(e)}")
            return False

    def guardar_agenda(self):
        try:
            if not os.path.exists('memory'):
                os.makedirs('memory')
            with open('memory/agenda.json', 'w') as f:
                json.dump(self.agenda, f)
        except Exception as e:
            print(f"Error al guardar la agenda: {str(e)}")

    def cargar_agenda(self):
        try:
            if os.path.exists('memory/agenda.json'):
                with open('memory/agenda.json', 'r') as f:
                    self.agenda = json.load(f)
        except Exception as e:
            print(f"Error al cargar la agenda: {str(e)}")

def self_coder():
    self_coder.agenda_semana = AgendaSemana()
    self_coder.agenda_semana.cargar_agenda()

    while True:
        print("\nOpciones:")
        print("1. Agregar evento")
        print("2. Listar eventos del día")
        print("3. Listar la semana")
        print("4. Eliminar evento")
        print("5. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            dia = input("Ingrese el día (lunes, martes, etc.): ")
            hora = input("Ingrese la hora (HH:MM): ")
            materia = input("Ingrese la materia o actividad: ")
            tipo = input("Ingrese el tipo (clase, tarea, examen): ")
            self_coder.agenda_semana.agregar_evento(dia, hora, materia, tipo)
        elif opcion == "2":
            dia = input("Ingrese el día (lunes, martes, etc.): ")
            eventos_dia = self_coder.agenda_semana.listar_eventos_dia(dia)
            for evento in eventos_dia:
                print(f"Día: {evento['dia']}, Hora: {evento['hora']}, Materia: {evento['materia']}, Tipo: {evento['tipo']}")
        elif opcion == "3":
            eventos = self_coder.agenda_semana.listar_semana()
            for evento in eventos:
                print(f"Día: {evento['dia']}, Hora: {evento['hora']}, Materia: {evento['materia']}, Tipo: {evento['tipo']}")
        elif opcion == "4":
            indice = int(input("Ingrese el índice del evento a eliminar: "))
            self_coder.agenda_semana.eliminar_evento(indice)
        elif opcion == "5":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    self_coder()