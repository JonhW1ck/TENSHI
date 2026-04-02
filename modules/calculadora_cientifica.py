# módulo calculadora_cientifica.py

def suma(num1, num2):
    """Calcula la suma de dos números."""
    try:
        return num1 + num2
    except TypeError:
        raise ValueError("Ambos operandos deben ser números.")

def resta(num1, num2):
    """Calcula la resta de dos números."""
    try:
        return num1 - num2
    except TypeError:
        raise ValueError("Ambos operandos deben ser números.")

def multiplicacion(num1, num2):
    """Calcula la multiplicación de dos números."""
    try:
        return num1 * num2
    except TypeError:
        raise ValueError("Ambos operandos deben ser números.")

def division(num1, num2):
    """Calcula la división de dos números."""
    try:
        if num2 == 0:
            raise ValueError("No se puede dividir por cero.")
        return num1 / num2
    except TypeError:
        raise ValueError("Ambos operandos deben ser números.")

def potencia(base, exponente):
    """Calcula la potencia de un número."""
    try:
        return base ** exponente
    except TypeError:
        raise ValueError("Ambos operandos deben ser números.")

def raiz_cuadrada(num):
    """Calcula la raíz cuadrada de un número."""
    try:
        return num ** 0.5
    except TypeError:
        raise ValueError("El operando debe ser un número.")

def seno(angulo):
    """Calcula el seno de un ángulo en grados."""
    try:
        import math
        return math.sin(math.radians(angulo))
    except TypeError:
        raise ValueError("El operando debe ser un número.")

def coseno(angulo):
    """Calcula el coseno de un ángulo en grados."""
    try:
        import math
        return math.cos(math.radians(angulo))
    except TypeError:
        raise ValueError("El operando debe ser un número.")

def tangente(angulo):
    """Calcula la tangente de un ángulo en grados."""
    try:
        import math
        return math.tan(math.radians(angulo))
    except TypeError:
        raise ValueError("El operando debe ser un número.")

def logaritmo(num, base=10):
    """Calcula el logaritmo de un número."""
    try:
        import math
        if num <= 0:
            raise ValueError("El número debe ser positivo.")
        return math.log(num, base)
    except TypeError:
        raise ValueError("El operando debe ser un número.")

def factorial(num):
    """Calcula el factorial de un número."""
    try:
        import math
        if num < 0:
            raise ValueError("El número debe ser no negativo.")
        return math.factorial(num)
    except TypeError:
        raise ValueError("El operando debe ser un número.")