class PresionAtmosferica:
    def __init__(self):
        self.ciudades_mexicanas = {
            "México D.F.": 2240,
            "Guadalajara": 1590,
            "Monterrey": 540,
            "Cancún": 10,
            "Tijuana": 160,
            "Puebla": 2130,
            "León": 1750,
            "Guanajuato": 2100,
            "San Luis Potosí": 1900,
            "Chihuahua": 1400
        }

    def calcular_presion(self, ciudad):
        try:
            altitud = self.ciudades_mexicanas[ciudad]
            presion = 101325 * (1 - 0.0000226 * altitud) ** 5.256
            return round(presion, 2)
        except KeyError:
            return f"La ciudad '{ciudad}' no se encuentra en la base de datos."
        except Exception as e:
            return f"Ocurrió un error: {str(e)}"

    def agregar_ciudad(self, ciudad, altitud):
        self.ciudades_mexicanas[ciudad] = altitud

    def eliminar_ciudad(self, ciudad):
        if ciudad in self.ciudades_mexicanas:
            del self.ciudades_mexicanas[ciudad]
        else:
            return f"La ciudad '{ciudad}' no se encuentra en la base de datos."

def self_coder():
    class PresionAtmosferica:
        def __init__(self):
            self.ciudades_mexicanas = {
                "México D.F.": 2240,
                "Guadalajara": 1590,
                "Monterrey": 540,
                "Cancún": 10,
                "Tijuana": 160,
                "Puebla": 2130,
                "León": 1750,
                "Guanajuato": 2100,
                "San Luis Potosí": 1900,
                "Chihuahua": 1400
            }

        def calcular_presion(self, ciudad):
            try:
                altitud = self.ciudades_mexicanas[ciudad]
                presion = 101325 * (1 - 0.0000226 * altitud) ** 5.256
                return round(presion, 2)
            except KeyError:
                return f"La ciudad '{ciudad}' no se encuentra en la base de datos."
            except Exception as e:
                return f"Ocurrió un error: {str(e)}"

        def agregar_ciudad(self, ciudad, altitud):
            self.ciudades_mexicanas[ciudad] = altitud

        def eliminar_ciudad(self, ciudad):
            if ciudad in self.ciudades_mexicanas:
                del self.ciudades_mexicanas[ciudad]
            else:
                return f"La ciudad '{ciudad}' no se encuentra en la base de datos."

    return PresionAtmosferica()