# self_coder.py

class Temperaturas:
    def __init__(self):
        pass

    def celsius_a_fahrenheit(self, celsius):
        try:
            return (celsius * 9/5) + 32
        except TypeError:
            raise ValueError("La temperatura debe ser un número")

    def fahrenheit_a_celsius(self, fahrenheit):
        try:
            return (fahrenheit - 32) * 5/9
        except TypeError:
            raise ValueError("La temperatura debe ser un número")

    def celsius_a_kelvin(self, celsius):
        try:
            return celsius + 273.15
        except TypeError:
            raise ValueError("La temperatura debe ser un número")

    def kelvin_a_celsius(self, kelvin):
        try:
            return kelvin - 273.15
        except TypeError:
            raise ValueError("La temperatura debe ser un número")

    def fahrenheit_a_kelvin(self, fahrenheit):
        try:
            return (fahrenheit - 32) * 5/9 + 273.15
        except TypeError:
            raise ValueError("La temperatura debe ser un número")

    def kelvin_a_fahrenheit(self, kelvin):
        try:
            return (kelvin - 273.15) * 9/5 + 32
        except TypeError:
            raise ValueError("La temperatura debe ser un número")

    def __str__(self):
        return "Clase Temperaturas"

if __name__ == "__main__":
    temperaturas = Temperaturas()
    print(temperaturas.celsius_a_fahrenheit(30))  # 86.0
    print(temperaturas.fahrenheit_a_celsius(86))  # 30.0
    print(temperaturas.celsius_a_kelvin(30))  # 303.15
    print(temperaturas.kelvin_a_celsius(303.15))  # 30.0
    print(temperaturas.fahrenheit_a_kelvin(86))  # 303.15
    print(temperaturas.kelvin_a_fahrenheit(303.15))  # 86.0