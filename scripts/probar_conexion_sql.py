from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from models.datos_model import obtener_conexion


if __name__ == "__main__":
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT @@SERVERNAME AS servidor, DB_NAME() AS base_datos")
        fila = cursor.fetchone()
        print("Conexión SQL Server correcta.")
        print(f"Servidor: {fila.servidor}")
        print(f"Base de datos: {fila.base_datos}")
        cursor.close()
    finally:
        conexion.close()
