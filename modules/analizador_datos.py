import math

class AnalizadorDatos:
    def __init__(self, valores):
        self.valores = valores

    def calcular_promedio(self):
        try:
            return sum(self.valores) / len(self.valores)
        except ZeroDivisionError:
            return None

    def calcular_mediana(self):
        valores_ordenados = sorted(self.valores)
        n = len(valores_ordenados)
        if n % 2 == 0:
            return (valores_ordenados[n // 2 - 1] + valores_ordenados[n // 2]) / 2
        else:
            return valores_ordenados[n // 2]

    def calcular_desviacion_estandar(self):
        try:
            promedio = self.calcular_promedio()
            suma = sum((x - promedio) ** 2 for x in self.valores)
            return math.sqrt(suma / (len(self.valores) - 1))
        except TypeError:
            return None

    def calcular_varianza(self):
        try:
            promedio = self.calcular_promedio()
            suma = sum((x - promedio) ** 2 for x in self.valores)
            return suma / (len(self.valores) - 1)
        except TypeError:
            return None

    def calcular_valor_maximo(self):
        return max(self.valores)

    def calcular_valor_minimo(self):
        return min(self.valores)

    def calcular_rango(self):
        return self.calcular_valor_maximo() - self.calcular_valor_minimo()

    def calcular_regresion_lineal_simple(self, x, y):
        try:
            n = len(x)
            suma_x = sum(x)
            suma_y = sum(y)
            suma_xy = sum(x[i] * y[i] for i in range(n))
            suma_x2 = sum(x[i] ** 2 for i in range(n))
            pendiente = (n * suma_xy - suma_x * suma_y) / (n * suma_x2 - suma_x ** 2)
            intercepto = (suma_y - pendiente * suma_x) / n
            coeficiente_r2 = 1 - (sum((y[i] - pendiente * x[i] - intercepto) ** 2 for i in range(n)) / sum((y[i] - suma_y / n) ** 2 for i in range(n)))
            return pendiente, intercepto, coeficiente_r2
        except ZeroDivisionError:
            return None

def self_coder():
    return """
import math

class AnalizadorDatos:
    def __init__(self, valores):
        self.valores = valores

    def calcular_promedio(self):
        try:
            return sum(self.valores) / len(self.valores)
        except ZeroDivisionError:
            return None

    def calcular_mediana(self):
        valores_ordenados = sorted(self.valores)
        n = len(valores_ordenados)
        if n % 2 == 0:
            return (valores_ordenados[n // 2 - 1] + valores_ordenados[n // 2]) / 2
        else:
            return valores_ordenados[n // 2]

    def calcular_desviacion_estandar(self):
        try:
            promedio = self.calcular_promedio()
            suma = sum((x - promedio) ** 2 for x in self.valores)
            return math.sqrt(suma / (len(self.valores) - 1))
        except TypeError:
            return None

    def calcular_varianza(self):
        try:
            promedio = self.calcular_promedio()
            suma = sum((x - promedio) ** 2 for x in self.valores)
            return suma / (len(self.valores) - 1)
        except TypeError:
            return None

    def calcular_valor_maximo(self):
        return max(self.valores)

    def calcular_valor_minimo(self):
        return min(self.valores)

    def calcular_rango(self):
        return self.calcular_valor_maximo() - self.calcular_valor_minimo()

    def calcular_regresion_lineal_simple(self, x, y):
        try:
            n = len(x)
            suma_x = sum(x)
            suma_y = sum(y)
            suma_xy = sum(x[i] * y[i] for i in range(n))
            suma_x2 = sum(x[i] ** 2 for i in range(n))
            pendiente = (n * suma_xy - suma_x * suma_y) / (n * suma_x2 - suma_x ** 2)
            intercepto = (suma_y - pendiente * suma_x) / n
            coeficiente_r2 = 1 - (sum((y[i] - pendiente * x[i] - intercepto) ** 2 for i in range(n)) / sum((y[i] - suma_y / n) ** 2 for i in range(n)))
            return pendiente, intercepto, coeficiente_r2
        except ZeroDivisionError:
            return None

def main():
    valores = [1, 2, 3, 4, 5]
    analizador = AnalizadorDatos(valores)
    print(analizador.calcular_promedio())
    print(analizador.calcular_mediana())
    print(analizador.calcular_desviacion_estandar())
    print(analizador.calcular_varianza())
    print(analizador.calcular_valor_maximo())
    print(analizador.calcular_valor_minimo())
    print(analizador.calcular_rango())

    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    pendiente, intercepto, coeficiente_r2 = analizador.calcular_regresion_lineal_simple(x, y)
    print(pendiente, intercepto, coeficiente_r2)

if __name__ == "__main__":
    main()
    """