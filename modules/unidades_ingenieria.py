class Unidades:
    def __init__(self):
        pass

    def presion(self, valor, unidad):
        try:
            if unidad.lower() == 'pa':
                return valor, 'Pa'
            elif unidad.lower() == 'bar':
                return valor * 100000, 'Pa'
            elif unidad.lower() == 'atm':
                return valor * 101325, 'Pa'
            elif unidad.lower() == 'psi':
                return valor * 6894.76, 'Pa'
            else:
                raise ValueError('Unidad de presión no válida')
        except ValueError as e:
            print(f'Error: {e}')

    def temperatura(self, valor, unidad):
        try:
            if unidad.lower() == '°c':
                return valor + 273.15, '°K'
            elif unidad.lower() == '°k':
                return valor - 273.15, '°C'
            elif unidad.lower() == '°f':
                return (valor - 32) * 5/9, '°C'
            else:
                raise ValueError('Unidad de temperatura no válida')
        except ValueError as e:
            print(f'Error: {e}')

    def masa(self, valor, unidad):
        try:
            if unidad.lower() == 'kg':
                return valor, 'kg'
            elif unidad.lower() == 'g':
                return valor / 1000, 'kg'
            elif unidad.lower() == 'lb':
                return valor * 0.453592, 'kg'
            else:
                raise ValueError('Unidad de masa no válida')
        except ValueError as e:
            print(f'Error: {e}')

    def caudal(self, valor, unidad):
        try:
            if unidad.lower() == 'm³/s':
                return valor, 'm³/s'
            elif unidad.lower() == 'l/min':
                return valor / 60 / 1000, 'm³/s'
            elif unidad.lower() == 'gpm':
                return valor * 0.002228, 'm³/s'
            else:
                raise ValueError('Unidad de caudal no válida')
        except ValueError as e:
            print(f'Error: {e}')

# Crear instancia del módulo
unidades = Unidades()

# Ejemplos de uso
print(unidades.presion(10, 'bar'))  # (1000000.0, 'Pa')
print(unidades.temperatura(20, '°C'))  # (293.15, '°K')
print(unidades.masa(10, 'kg'))  # (10.0, 'kg')
print(unidades.caudal(10, 'm³/s'))  # (10.0, 'm³/s')