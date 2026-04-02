# self_coder.py

class ConstantesFisicas:
    def __init__(self):
        self.R = self.constante_gas_ideal_joules()
        self.R_cal = self.constante_gas_ideal_calor()
        self.R_litros_atm = self.constante_gas_ideal_litros_atm()
        self.g = self.gravedad()
        self.NA = self.numero_avogadro()
        self.kB = self.constante_boltzmann()
        self.sigma = self.constante_stefan_boltzmann()
        self.permitividad_vacio = self.permitividad_vacio()

    def constante_gas_ideal_joules(self):
        try:
            return 8.31446261815324  # J/mol·K
        except Exception as e:
            print(f"Error: {e}")

    def constante_gas_ideal_calor(self):
        try:
            return 8.31446261815324 / 4.184  # cal/mol·K
        except Exception as e:
            print(f"Error: {e}")

    def constante_gas_ideal_litros_atm(self):
        try:
            return 0.083145  # L·atm/mol·K
        except Exception as e:
            print(f"Error: {e}")

    def gravedad(self):
        try:
            return 9.80665  # m/s^2
        except Exception as e:
            print(f"Error: {e}")

    def numero_avogadro(self):
        try:
            return 6.02214076e23  # mol^-1
        except Exception as e:
            print(f"Error: {e}")

    def constante_boltzmann(self):
        try:
            return 1.38064852e-23  # J/K
        except Exception as e:
            print(f"Error: {e}")

    def constante_stefan_boltzmann(self):
        try:
            return 5.670367e-8  # W/m^2K^4
        except Exception as e:
            print(f"Error: {e}")

    def permitividad_vacio(self):
        try:
            return 8.85418781762039e-12  # F/m
        except Exception as e:
            print(f"Error: {e}")

# Crear una instancia de la clase ConstantesFisicas
constantes = ConstantesFisicas()

# Acceder a las constantes
print(constantes.R)
print(constantes.R_cal)
print(constantes.R_litros_atm)
print(constantes.g)
print(constantes.NA)
print(constantes.kB)
print(constantes.sigma)
print(constantes.permitividad_vacio)