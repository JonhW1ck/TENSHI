class MenuComandos:
    def __init__(self):
        self.comandos = {
            '/tabla': self.mostrar_tabla,
            '/convertir': self.convertir_unidad,
            '/flashcard': self.mostrar_flashcard,
            '/agenda': self.mostrar_agenda,
            '/analizar': self.analizar_datos
        }

    def ejecutar_comando(self, texto):
        try:
            comando, *argumentos = texto.split()
            if comando in self.comandos:
                return self.comandos[comando](argumentos)
            else:
                return "Comando desconocido"
        except Exception as e:
            return f"Error: {str(e)}"

    def mostrar_tabla(self, argumentos):
        if len(argumentos) == 1:
            return f"Mostrar tabla de multiplicar con base {argumentos[0]}"
        else:
            return "Error: La tabla de multiplicar requiere un número como argumento"

    def convertir_unidad(self, argumentos):
        if len(argumentos) == 2:
            return f"Convertir {argumentos[0]} de {argumentos[1]} a otro sistema de unidades"
        else:
            return "Error: La conversión de unidades requiere dos argumentos (valor y unidad)"

    def mostrar_flashcard(self, argumentos):
        if not argumentos:
            return "Mostrar flashcard aleatoria"
        else:
            return "Error: La flashcard aleatoria no requiere argumentos"

    def mostrar_agenda(self, argumentos):
        if not argumentos or len(argumentos) == 1:
            return "Mostrar agenda de la semana"
        else:
            return "Error: La agenda de la semana no requiere argumentos"

    def analizar_datos(self, argumentos):
        if len(argumentos) > 1:
            return f"Analizar datos {', '.join(argumentos)}"
        else:
            return "Error: La análisis de datos requiere al menos dos argumentos separados por comas"

menu = MenuComandos()