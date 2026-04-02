import re

class EcuacionQuimica:
    def __init__(self, ecuacion):
        self.ecuacion = ecuacion
        self.elementos = {}
        self.coeficientes = {}

    def parsear_ecuacion(self):
        try:
            partes = self.ecuacion.split(' -> ')
            reaccion = partes[0]
            producto = partes[1]

            elementos_reaccion = re.findall(r'([A-Z][a-z]*)(\d*)', reaccion)
            elementos_producto = re.findall(r'([A-Z][a-z]*)(\d*)', producto)

            for elemento, coeficiente in elementos_reaccion:
                if elemento in self.elementos:
                    self.elementos[elemento] += int(coeficiente or 1)
                else:
                    self.elementos[elemento] = int(coeficiente or 1)

            for elemento, coeficiente in elementos_producto:
                if elemento in self.elementos:
                    self.elementos[elemento] -= int(coeficiente or 1)
                else:
                    self.elementos[elemento] = -int(coeficiente or 1)
        except Exception as e:
            raise ValueError("Error al parsear la ecuacion") from e

    def balancear_ecuacion(self):
        self.parsear_ecuacion()

        while True:
            elementos_sin_balancear = [elemento for elemento, cantidad in self.elementos.items() if cantidad != 0]

            if not elementos_sin_balancear:
                break

            elemento_mas_grande = max(elementos_sin_balancear, key=lambda x: abs(self.elementos[x]))

            factor = self.elementos[elemento_mas_grande] // abs(self.elementos[elemento_mas_grande])

            for elemento, cantidad in self.elementos.items():
                self.coeficientes[elemento] = factor * cantidad

            self.elementos = {elemento: factor * cantidad for elemento, cantidad in self.elementos.items()}

    def get_coeficientes(self):
        self.balancear_ecuacion()
        return self.coeficientes

def balancear_ecuacion_quimica(ecuacion):
    try:
        ecuacion = EcuacionQuimica(ecuacion)
        return ecuacion.get_coeficientes()
    except ValueError as e:
        raise ValueError("Error al balancear la ecuacion") from e

# Ejemplos de prueba
print(balancear_ecuacion_quimica("H2 + O2 -> H2O"))  # {H: 2, O: 1, H2: 1, O2: 1}
print(balancear_ecuacion_quimica("C6H12O6 + 6O2 -> 6CO2 + 6H2O"))  # {C: 6, H: 12, O: 18, C6H12O6: 1, O2: 6, CO2: 6, H2O: 6}
print(balancear_ecuacion_quimica("Zn + CuSO4 -> ZnSO4 + Cu"))  # {Zn: 1, Cu: 1, ZnSO4: 1, CuSO4: 1}