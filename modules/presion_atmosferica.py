class PresionAtmosferica:
    def __init__(self):
        self.ciudades_mexicanas = {
            "Mexico D.F.": 2240,
            "Guadalajara": 1590,
            "Monterrey": 540,
            "Cancun": 10,
            "Tijuana": 160,
            "Puebla": 2130,
            "Leon": 1750,
            "Guanajuato": 2100,
            "San Luis Potosi": 1900,
            "Chihuahua": 1400
        }

    def calcular_presion(self, ciudad):
        try:
            altitud = self.ciudades_mexicanas[ciudad]
            presion = 101325 * (1 - 0.0000226 * altitud) ** 5.256
            return round(presion, 2)
        except KeyError:
            return f"Ciudad '{ciudad}' no encontrada."
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    p = PresionAtmosferica()
    for ciudad in ["Guadalajara", "Mexico D.F.", "Cancun"]:
        print(f"{ciudad}: {p.calcular_presion(ciudad)} Pa")
