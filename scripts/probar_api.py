from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.api_client import APIClient


if __name__ == "__main__":
    cliente = APIClient()
    registros = cliente.obtener_registros(limite=5)
    print(f"Registros recibidos: {len(registros)}")
    if registros:
        print("Campos del primer registro:")
        for campo, valor in registros[0].items():
            print(f"  {campo}: {valor}")
    else:
        print("La API respondió correctamente, pero no devolvió filas para esta consulta.")
