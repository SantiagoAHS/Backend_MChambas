# services/utils.py
import requests

def validar_direccion_nominatim(street=None, city=None, state=None, country=None, postalcode=None):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "street": street,
        "city": city,
        "state": state,
        "country": country,
        "postalcode": postalcode,
        "format": "json"
    }

    headers = {
        "User-Agent": "miapp-direcciones/1.0 (prueba@ejemplo.com)"  # cámbialo por tu correo real en producción
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]  # retorna la mejor coincidencia
        else:
            return None
    else:
        return None
