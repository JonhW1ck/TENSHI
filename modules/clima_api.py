import requests
import json

class Clima:
    def __init__(self):
        self.url_base = "http://wttr.in/"

    def obtener_clima(self, ciudad):
        try:
            response = requests.get(f"{self.url_base}{ciudad}?format=j1", timeout=5)
            response.raise_for_status()
            datos = response.json()
            current_condition = datos["current_condition"][0]
            temperatura_c = current_condition["temp_C"]
            humedad = current_condition["humidity"]
            condicion = current_condition["weatherDesc"][0]["value"]
            return {
                "ciudad": ciudad,
                "temperatura_c": temperatura_c,
                "humedad": humedad,
                "condicion": condicion
            }
        except requests.exceptions.HTTPError as http_err:
            print(f"Error de HTTP: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Error de solicitud: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"Error de JSON: {json_err}")
        except Exception as err:
            print(f"Error desconocido: {err}")
        return None

def self_coder():
    class Clima:
        def __init__(self):
            self.url_base = "http://wttr.in/"

        def obtener_clima(self, ciudad):
            try:
                response = requests.get(f"{self.url_base}{ciudad}?format=j1", timeout=5)
                response.raise_for_status()
                datos = response.json()
                current_condition = datos["current_condition"][0]
                temperatura_c = current_condition["temp_C"]
                humedad = current_condition["humidity"]
                condicion = current_condition["weatherDesc"][0]["value"]
                return {
                    "ciudad": ciudad,
                    "temperatura_c": temperatura_c,
                    "humedad": humedad,
                    "condicion": condicion
                }
            except requests.exceptions.HTTPError as http_err:
                print(f"Error de HTTP: {http_err}")
            except requests.exceptions.RequestException as req_err:
                print(f"Error de solicitud: {req_err}")
            except json.JSONDecodeError as json_err:
                print(f"Error de JSON: {json_err}")
            except Exception as err:
                print(f"Error desconocido: {err}")
            return None
    return Clima()