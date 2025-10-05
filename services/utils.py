# services/utils.py
import requests

def validar_direccion_nominatim(street=None, city=None, state=None, country=None, postalcode=None):
    url = "https://nominatim.openstreetmap.org/search"

    # ✅ Usamos solo los campos más generales (país, estado, ciudad)
    params = {
        "city": city,
        "state": state,
        "country": country,
        "format": "json",
        "limit": 1  # solo necesitamos una coincidencia
    }

    headers = {
        "User-Agent": "sistema-tutorias-uttt/1.0 (contacto@uttt.edu.mx)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
            else:
                # Si no encuentra, devolvemos una dirección básica compuesta
                return {
                    "display_name": f"{city}, {state}, {country}",
                    "lat": None,
                    "lon": None
                }
        else:
            return {
                "display_name": f"{city}, {state}, {country}",
                "lat": None,
                "lon": None
            }

    except requests.RequestException:
        # Si hay error en la API, devolvemos una respuesta básica
        return {
            "display_name": f"{city}, {state}, {country}",
            "lat": None,
            "lon": None
        }
