import os
import requests
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    """Cliente HTTP para el recurso SIVIGILA 2018 publicado en datos.gov.co."""

    CAMPOS_ESPERADOS = {
        "cod_eve", "nombre", "ano", "semana", "cod_dpto_o",
        "nom_mun", "cod_mun_o", "conteo_casos",
    }

    def __init__(self):
        recurso = os.getenv("API_RESOURCE_ID", "xd2n-cu8j").strip()
        if not recurso:
            raise ValueError("API_RESOURCE_ID está vacío en el archivo .env.")
        self.url = f"https://www.datos.gov.co/resource/{recurso}.json"

    def obtener_registros(self, limite=None):
        limite = int(limite or os.getenv("API_LIMIT", "100"))
        if not 1 <= limite <= 5000:
            raise ValueError("API_LIMIT debe estar entre 1 y 5000.")

        parametros = {
            "$limit": limite,
            "$order": "ano DESC, semana DESC, cod_eve ASC",
        }
        respuesta = requests.get(
            self.url,
            params=parametros,
            headers={"Accept": "application/json"},
            timeout=30,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
        if not isinstance(datos, list):
            raise ValueError("La API no devolvió una lista JSON.")
        if datos and not any(self.CAMPOS_ESPERADOS.intersection(fila.keys()) for fila in datos if isinstance(fila, dict)):
            raise ValueError(
                "La respuesta no contiene los campos esperados de SIVIGILA 2018. "
                "Comprueba el identificador del recurso."
            )
        if any(not isinstance(fila, dict) for fila in datos):
            raise ValueError("La API devolvió elementos JSON con un formato inesperado.")
        return datos
