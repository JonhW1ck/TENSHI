import requests
import json

def obtener_clima(ciudad):
    try:
        # Paso 1: Geocodificar con Open-Meteo
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1"
        response_geocoding = requests.get(geocoding_url, timeout=5)
        response_geocoding.raise_for_status()
        results = response_geocoding.json()
        if results['results']:
            lat = results['results'][0]['latitude']
            lon = results['results'][0]['longitude']
        else:
            return None

        # Paso 2: Obtener clima con Open-Meteo
        clima_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
        response_clima = requests.get(clima_url, timeout=5)
        response_clima.raise_for_status()
        clima_data = response_clima.json()

        # Extraer datos de clima
        temperatura_c = clima_data['current']['temperature_2m']
        humedad = clima_data['current']['relative_humidity_2m']
        weather_code = clima_data['current']['weather_code']

        # Retornar datos de clima
        return {
            'ciudad': ciudad,
            'temperatura_c': temperatura_c,
            'humedad': humedad,
            'weather_code': weather_code
        }
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener clima: {e}")
        return None

if __name__ == "__main__":
    ciudad = "Madrid"
    clima = obtener_clima(ciudad)
    if clima:
        print(json.dumps(clima, indent=4))