import hashlib
import json
import os
from decimal import Decimal, InvalidOperation

from dotenv import load_dotenv

load_dotenv()

TABLA = "dbo.RegistrosSivigila2018"


def obtener_conexion():
    """Abre SQL Server usando la autenticación de Windows configurada por el usuario."""
    servidor = os.getenv("DB_SERVER", "localhost").strip()
    base_datos = os.getenv("DB_NAME", "SIVIGILA2018DB").strip()
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server").strip()
    trusted = os.getenv("DB_TRUSTED", "yes").strip().lower() == "yes"

    if not servidor or not base_datos or not driver:
        raise ValueError("Revisa DB_SERVER, DB_NAME y DB_DRIVER en el archivo .env.")

    cadena = (
        f"DRIVER={{{driver}}};"
        f"SERVER={servidor};"
        f"DATABASE={base_datos};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    if trusted:
        cadena += "Trusted_Connection=yes;"
    else:
        usuario = os.getenv("DB_USER", "").strip()
        clave = os.getenv("DB_PASSWORD", "")
        if not usuario or not clave:
            raise ValueError("Seleccionaste autenticación SQL, pero DB_USER o DB_PASSWORD están vacíos.")
        cadena += f"UID={usuario};PWD={clave};"
    try:
        import pyodbc
    except ImportError as exc:
        raise RuntimeError("Falta pyodbc. Ejecuta: pip install -r requirements.txt") from exc
    return pyodbc.connect(cadena, timeout=10)


def _texto(valor):
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto if texto else None


def _entero(valor, campo):
    if valor is None or str(valor).strip() == "":
        return None
    try:
        numero = Decimal(str(valor).strip())
        if numero != numero.to_integral_value():
            raise ValueError(f"El campo {campo} contiene un valor que no es entero: {valor}")
        return int(numero)
    except (InvalidOperation, ValueError) as exc:
        if isinstance(exc, ValueError) and str(exc).startswith("El campo"):
            raise
        raise ValueError(f"No se pudo convertir el campo {campo} a entero: {valor}") from exc


def normalizar_registro(registro):
    """Mapea los ocho campos reales de la API y crea una clave SHA-256 estable."""
    if not isinstance(registro, dict):
        raise ValueError("Cada registro recibido debe ser un objeto JSON.")

    campos = {
        "cod_eve": _entero(registro.get("cod_eve"), "cod_eve"),
        "nombre": _texto(registro.get("nombre")),
        "ano": _entero(registro.get("ano"), "ano"),
        "semana": _entero(registro.get("semana"), "semana"),
        "cod_dpto_o": _entero(registro.get("cod_dpto_o"), "cod_dpto_o"),
        "nom_mun": _texto(registro.get("nom_mun")),
        "cod_mun_o": _entero(registro.get("cod_mun_o"), "cod_mun_o"),
        "conteo_casos": _entero(registro.get("conteo_casos"), "conteo_casos"),
    }
    json_original = json.dumps(registro, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    id_api = hashlib.sha256(json_original.encode("utf-8")).hexdigest()
    return id_api, campos, json_original


def guardar_registros(registros):
    """Inserta registros nuevos; la restricción UNIQUE y el hash evitan duplicados."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    insertados = 0
    try:
        for registro in registros:
            id_api, campos, json_original = normalizar_registro(registro)
            cursor.execute(f"SELECT 1 FROM {TABLA} WHERE id_api = ?", id_api)
            if cursor.fetchone() is not None:
                continue
            cursor.execute(
                f"""
                INSERT INTO {TABLA}
                (id_api, cod_eve, nombre, ano, semana, cod_dpto_o, nom_mun,
                 cod_mun_o, conteo_casos, json_original)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                id_api,
                campos["cod_eve"],
                campos["nombre"],
                campos["ano"],
                campos["semana"],
                campos["cod_dpto_o"],
                campos["nom_mun"],
                campos["cod_mun_o"],
                campos["conteo_casos"],
                json_original,
            )
            insertados += 1
        conexion.commit()
        return insertados
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def consultar_registros(filtro=""):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        columnas = "id, cod_eve, nombre, ano, semana, cod_dpto_o, nom_mun, cod_mun_o, conteo_casos"
        if filtro:
            patron = f"%{filtro}%"
            cursor.execute(
                f"""SELECT TOP 100 {columnas} FROM {TABLA}
                    WHERE nom_mun LIKE ? OR nombre LIKE ? OR CONVERT(NVARCHAR(30), cod_eve) LIKE ?
                    ORDER BY ano DESC, semana DESC, id DESC""",
                patron, patron, patron,
            )
        else:
            cursor.execute(
                f"SELECT TOP 100 {columnas} FROM {TABLA} ORDER BY ano DESC, semana DESC, id DESC"
            )
        nombres = [columna[0] for columna in cursor.description]
        return [dict(zip(nombres, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def obtener_resumen():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            f"""SELECT COUNT(*) AS total_registros,
                       COALESCE(SUM(CAST(conteo_casos AS BIGINT)), 0) AS casos_sumados,
                       COUNT(DISTINCT nom_mun) AS municipios,
                       COUNT(DISTINCT cod_eve) AS eventos
                FROM {TABLA}"""
        )
        fila = cursor.fetchone()
        return {
            "total_registros": int(fila[0]),
            "casos_sumados": int(fila[1]),
            "municipios": int(fila[2]),
            "eventos": int(fila[3]),
        }
    finally:
        cursor.close()
        conexion.close()
