# Guion breve de sustentación – Jean Carlos Pérez Pacheco

Buenos días. Mi nombre es Jean Carlos Pérez Pacheco y voy a presentar mi proyecto de consulta y análisis básico de datos abiertos de salud pública, utilizando el conjunto SIVIGILA 2018 del Instituto Nacional de Salud.

El objetivo es consumir una API pública, recibir los datos en formato JSON, almacenarlos en una base de datos SQL Server y permitir que se consulten desde una aplicación web.

El proyecto está organizado con el patrón MVC. El modelo está en `models/datos_model.py` y se encarga de la conexión, las inserciones y las consultas a SQL Server. La vista está en `templates/index.html` y `static/estilos.css`; allí se muestran los indicadores, el buscador y la tabla. El controlador está en `app.py`, donde se reciben las solicitudes y se coordinan las operaciones. Además, `api/api_client.py` contiene el componente encargado de consumir la API externa.

El conjunto de datos contiene ocho campos: código y nombre del evento, año, semana epidemiológica, códigos de departamento y municipio, nombre del municipio y conteo de casos. Es información histórica del año 2018, por lo que no se interpreta como una cifra actual de salud pública.

Cuando se pulsa el botón de sincronización, Flask solicita los datos a la API, el modelo los normaliza y los almacena en SQL Server. Para evitar duplicados, se genera una huella única a partir del registro JSON y se protege con una restricción única en la base de datos. Después, la página permite buscar por municipio, evento o código y presenta un resumen de los datos guardados.

Con este proyecto se integran consumo de API REST, Python, SQL Server, persistencia de datos, consultas web y separación de responsabilidades mediante MVC. Muchas gracias.

---

**Nota para la presentación:** durante la sustentación, muestra la aplicación ejecutándose y reemplaza expresiones generales como “se almacena” por una demostración real. No afirmes que una prueba fue exitosa si no la has ejecutado.
