import os
from flask import Flask, flash, redirect, render_template, request, url_for
from api.api_client import APIClient
from models.datos_model import consultar_registros, guardar_registros, obtener_resumen

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-local-solo-desarrollo")


@app.get("/")
def inicio():
    filtro = request.args.get("q", "").strip()
    try:
        registros = consultar_registros(filtro)
        resumen = obtener_resumen()
    except Exception as exc:
        registros = []
        resumen = {"total_registros": 0, "casos_sumados": 0, "municipios": 0, "eventos": 0}
        flash(
            "No fue posible consultar SQL Server. Revisa la conexión y ejecuta "
            "sql/crear_base_datos.sql. Detalle: " + str(exc),
            "error",
        )
    return render_template("index.html", registros=registros, filtro=filtro, resumen=resumen)


@app.post("/sincronizar")
def sincronizar():
    try:
        cliente = APIClient()
        datos = cliente.obtener_registros()
        cantidad = guardar_registros(datos)
        flash(
            f"Consulta completada. La API devolvió {len(datos)} registros; "
            f"se almacenaron {cantidad} nuevos y se omitieron los ya existentes.",
            "success",
        )
    except Exception as exc:
        flash("No fue posible sincronizar los datos: " + str(exc), "error")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").strip().lower() == "true"
    app.run(host="127.0.0.1", port=5000, debug=debug)
