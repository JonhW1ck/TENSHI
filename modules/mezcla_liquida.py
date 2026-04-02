import math

class MezclaLiquidaBinaria:
    def __init__(self, fraccion_masico_componente1, densidad_componente1, viscosidad_componente1, cp_componente1,
                 fraccion_masico_componente2, densidad_componente2, viscosidad_componente2, cp_componente2):
        self.fraccion_masico_componente1 = fraccion_masico_componente1
        self.densidad_componente1 = densidad_componente1
        self.viscosidad_componente1 = viscosidad_componente1
        self.cp_componente1 = cp_componente1
        self.fraccion_masico_componente2 = fraccion_masico_componente2
        self.densidad_componente2 = densidad_componente2
        self.viscosidad_componente2 = viscosidad_componente2
        self.cp_componente2 = cp_componente2

    def calcular_densidad_mezcla(self):
        try:
            densidad_mezcla = (self.fraccion_masico_componente1 * self.densidad_componente1 +
                               self.fraccion_masico_componente2 * self.densidad_componente2)
            return densidad_mezcla
        except Exception as e:
            print(f"Error al calcular densidad de la mezcla: {str(e)}")
            return None

    def calcular_viscosidad_dinamica(self):
        try:
            viscosidad_componente1_log = math.log10(self.viscosidad_componente1)
            viscosidad_componente2_log = math.log10(self.viscosidad_componente2)
            viscosidad_mezcla_log = (self.fraccion_masico_componente1 * viscosidad_componente1_log +
                                    self.fraccion_masico_componente2 * viscosidad_componente2_log)
            viscosidad_mezcla = 10 ** viscosidad_mezcla_log
            return viscosidad_mezcla
        except Exception as e:
            print(f"Error al calcular viscosidad dinámica de la mezcla: {str(e)}")
            return None

    def calcular_calor_especifico(self):
        try:
            calor_especifico_mezcla = (self.fraccion_masico_componente1 * self.cp_componente1 +
                                       self.fraccion_masico_componente2 * self.cp_componente2)
            return calor_especifico_mezcla
        except Exception as e:
            print(f"Error al calcular calor específico de la mezcla: {str(e)}")
            return None

def crear_mezcla_liquida_binaria(fraccion_masico_componente1, densidad_componente1, viscosidad_componente1, cp_componente1,
                                 fraccion_masico_componente2, densidad_componente2, viscosidad_componente2, cp_componente2):
    mezcla = MezclaLiquidaBinaria(fraccion_masico_componente1, densidad_componente1, viscosidad_componente1, cp_componente1,
                                  fraccion_masico_componente2, densidad_componente2, viscosidad_componente2, cp_componente2)
    return mezcla

def main():
    mezcla = crear_mezcla_liquida_binaria(0.5, 1000, 0.01, 2.5, 0.5, 800, 0.02, 2.8)
    densidad_mezcla = mezcla.calcular_densidad_mezcla()
    viscosidad_mezcla = mezcla.calcular_viscosidad_dinamica()
    calor_especifico_mezcla = mezcla.calcular_calor_especifico()
    print(f"Densidad de la mezcla: {densidad_mezcla}")
    print(f"Viscosidad dinámica de la mezcla: {viscosidad_mezcla}")
    print(f"Calor específico de la mezcla: {calor_especifico_mezcla}")

if __name__ == "__main__":
    main()