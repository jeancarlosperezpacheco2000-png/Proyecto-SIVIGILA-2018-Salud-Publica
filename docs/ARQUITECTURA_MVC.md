# Arquitectura del sistema

## Componentes

**Controlador – `app.py`**  
Recibe solicitudes HTTP del navegador. La ruta `GET /` lee el filtro, solicita al modelo los registros y el resumen, y renderiza la plantilla. La ruta `POST /sincronizar` coordina al cliente API y al modelo para guardar los nuevos datos.

**Servicio externo – `api/api_client.py`**  
Construye el endpoint de SIVIGILA 2018, envía la petición HTTP con límite y orden, valida el código de respuesta y entrega la lista JSON.

**Modelo – `models/datos_model.py`**  
Establece la conexión con SQL Server mediante pyodbc, transforma los campos de la API, genera una huella SHA-256 para cada fila, inserta registros nuevos y ejecuta consultas SELECT para búsqueda y resumen.

**Vista – `templates/index.html` y `static/estilos.css`**  
Muestra botón de sincronización, mensajes, indicadores, campo de búsqueda y tabla de registros. No realiza conexiones directas a SQL Server.

## Flujo de sincronización

1. La persona pulsa el botón de sincronización en el navegador.
2. Flask recibe `POST /sincronizar`.
3. El controlador llama al cliente API.
4. El cliente API consulta datos.gov.co y recibe JSON.
5. El controlador entrega los datos al modelo.
6. El modelo normaliza campos y guarda registros en SQL Server sin repetir la misma huella.
7. Flask muestra un mensaje y redirige a la página principal.

## Flujo de consulta

1. La persona abre la página o envía un término de búsqueda.
2. Flask recibe `GET /` y el parámetro `q`.
3. El modelo ejecuta un SELECT parametrizado en SQL Server.
4. El modelo devuelve registros y métricas al controlador.
5. Flask entrega la información a `index.html`.
6. La vista presenta tabla e indicadores.
