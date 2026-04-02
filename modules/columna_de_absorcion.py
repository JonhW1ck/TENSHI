import numpy as np

class ColumnaDeAbsorcion:
    def __init__(self, y_entrada, y_salida, y_estrella, L, m, G, KGa):
        self.y_entrada = y_entrada
        self.y_salida = y_salida
        self.y_estrella = y_estrella
        self.L = L
        self.m = m
        self.G = G
        self.KGa = KGa

    def calcular_htu(self):
        try:
            return self.G / self.KGa
        except ZeroDivisionError:
            raise ValueError("KGa no puede ser cero")

    def calcular_nog(self):
        try:
            y = np.linspace(self.y_entrada, self.y_salida, 100)
            return np.trapz(1 / (y - self.y_estrella), y)
        except Exception as e:
            raise ValueError("Error al calcular NOG") from e

    def calcular_zt(self):
        try:
            return self.calcular_nog() * self.calcular_htu()
        except Exception as e:
            raise ValueError("Error al calcular ZT") from e

    def calcular_razon_de_absorcion(self):
        try:
            return self.L / (self.m * self.G)
        except Exception as e:
            raise ValueError("Error al calcular la razón de absorción") from e

    def calcular_resultados(self):
        try:
            htu = self.calcular_htu()
            nog = self.calcular_nog()
            zt = self.calcular_zt()
            razon_de_absorcion = self.calcular_razon_de_absorcion()
            return {
                "HTU": htu,
                "NOG": nog,
                "ZT": zt,
                "Razón de absorción": razon_de_absorcion
            }
        except Exception as e:
            raise ValueError("Error al calcular resultados") from e

# self_coder
class self_coder:
    def __init__(self):
        self.modulo = ColumnaDeAbsorcion

    def generar_codigo(self):
        return """
class ColumnaDeAbsorcion:
    def __init__(self, y_entrada, y_salida, y_estrella, L, m, G, KGa):
        self.y_entrada = y_entrada
        self.y_salida = y_salida
        self.y_estrella = y_estrella
        self.L = L
        self.m = m
        self.G = G
        self.KGa = KGa

    def calcular_htu(self):
        try:
            return self.G / self.KGa
        except ZeroDivisionError:
            raise ValueError("KGa no puede ser cero")

    def calcular_nog(self):
        try:
            y = np.linspace(self.y_entrada, self.y_salida, 100)
            return np.trapz(1 / (y - self.y_estrella), y)
        except Exception as e:
            raise ValueError("Error al calcular NOG") from e

    def calcular_zt(self):
        try:
            return self.calcular_nog() * self.calcular_htu()
        except Exception as e:
            raise ValueError("Error al calcular ZT") from e

    def calcular_razon_de_absorcion(self):
        try:
            return self.L / (self.m * self.G)
        except Exception as e:
            raise ValueError("Error al calcular la razón de absorción") from e

    def calcular_resultados(self):
        try:
            htu = self.calcular_htu()
            nog = self.calcular_nog()
            zt = self.calcular_zt()
            razon_de_absorcion = self.calcular_razon_de_absorcion()
            return {
                "HTU": htu,
                "NOG": nog,
                "ZT": zt,
                "Razón de absorción": razon_de_absorcion
            }
        except Exception as e:
            raise ValueError("Error al calcular resultados") from e
"""

    def guardar_codigo(self):
        with open("columna_de_absorcion.py", "w") as f:
            f.write(self.generar_codigo())