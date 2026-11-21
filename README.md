# Sistema de consulta de datos abiertos de salud pública – SIVIGILA 2018

**Asignatura:** Desarrollo de Aplicaciones con Acceso a Datos  
**Integrante:** Jean Carlos Pérez Pacheco  
**Tecnologías:** Python, Flask, API REST Socrata, SQL Server, pyodbc, HTML y CSS.

## 1. Descripción y objetivo

Aplicación web académica que consulta el conjunto **SIVIGILA 2018** del Instituto Nacional de Salud, recibe los registros en formato JSON, almacena una selección de sus campos en SQL Server y permite consultarlos desde el navegador mediante un filtro sencillo y un resumen numérico.

El conjunto contiene información agregada de vigilancia en salud pública para el año 2018. **Es información histórica y no debe presentarse como una medición de la situación sanitaria actual.** El portal informa aproximadamente 194 mil filas y ocho columnas. La página de metadatos fue actualizada el 18 de mayo de 2026, mientras que la última actualización de los datos está registrada el 7 de enero de 2021.

## 2. Fuente de datos y endpoint

- Entidad: Instituto Nacional de Salud (INS), Colombia.
- Conjunto: [SIVIGILA 2018 – datos.gov.co](https://www.datos.gov.co/Salud-y-Protecci-n-Social/SIVIGILA-2018/xd2n-cu8j).
- Identificador del recurso: `xd2n-cu8j`.
- Endpoint base: `https://www.datos.gov.co/resource/xd2n-cu8j.json`.
- Consulta inicial: `https://www.datos.gov.co/resource/xd2n-cu8j.json?$limit=100`.
- Campos API documentados: `cod_eve`, `nombre`, `ano`, `semana`, `cod_dpto_o`, `nom_mun`, `cod_mun_o`, `conteo_casos`.

La aplicación solicita hasta 100 registros por sincronización. El límite puede modificarse en `.env` mediante `API_LIMIT`, sin exceder 5000 en esta configuración.

## 3. Campos almacenados

| Campo API | Columna SQL | Uso |
|---|---|---|
| `cod_eve` | `cod_eve` | Código del evento de vigilancia |
| `nombre` | `nombre` | Nombre del evento |
| `ano` | `ano` | Año reportado |
| `semana` | `semana` | Semana epidemiológica reportada |
| `cod_dpto_o` | `cod_dpto_o` | Código de departamento |
| `nom_mun` | `nom_mun` | Nombre del municipio |
| `cod_mun_o` | `cod_mun_o` | Código de municipio |
| `conteo_casos` | `conteo_casos` | Conteo de casos del registro |

Además se guarda `json_original` para conservar la respuesta original y `fecha_captura` para registrar cuándo se almacenó localmente.

## 4. Arquitectura MVC

- **Modelo:** `models/datos_model.py`. Administra la conexión con SQL Server, normaliza los campos, evita duplicados, inserta y consulta registros.
- **Vista:** `templates/index.html` y `static/estilos.css`. Presenta indicadores, formulario de búsqueda y tabla de resultados.
- **Controlador:** `app.py`. Atiende las rutas web, coordina la sincronización de la API con el modelo y envía la información a la vista.
- **Servicio de API:** `api/api_client.py`. Realiza la petición HTTP al endpoint de datos.gov.co y valida que la respuesta sea una lista JSON.

## 5. Requisitos

1. Windows 10/11.
2. Python 3.10 o superior.
3. Microsoft SQL Server iniciado localmente.
4. Microsoft ODBC Driver 18 for SQL Server (o compatible).
5. SQL Server Management Studio (SSMS).
6. Visual Studio Code y conexión a Internet.

## 6. Configuración de SQL Server

La conexión identificada para este equipo es `localhost` con autenticación de Windows. La configuración del archivo `.env.example` ya parte de esos datos.

1. En la carpeta principal, copia `.env.example` y cambia el nombre de la copia a `.env`.
2. Verifica que contenga `DB_SERVER=localhost`, `DB_NAME=SIVIGILA2018DB`, `DB_TRUSTED=yes` y el controlador ODBC instalado.
3. En SSMS, abre `sql/crear_base_datos.sql` y ejecútalo con F5.
4. Comprueba que exista la base `SIVIGILA2018DB` y la tabla `dbo.RegistrosSivigila2018`.

No se necesita escribir una contraseña de SQL Server porque se usa autenticación de Windows. Si tu instalación de ODBC tiene otro nombre de controlador, cambia `DB_DRIVER` en `.env` para que coincida exactamente con el instalado.

## 7. Instalación y ejecución en Windows

Abre la terminal de VS Code en la carpeta raíz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell impide activar el entorno, utiliza CMD:

```bat
venv\Scripts\activate.bat
```

Verifica primero el controlador disponible con `python -c "import pyodbc; print(pyodbc.drivers())"`. Si no aparece `ODBC Driver 18 for SQL Server`, instala el controlador ODBC 18 de Microsoft o ajusta `DB_DRIVER` al nombre de un controlador compatible instalado.

Ejecuta las pruebas unitarias y de conexión:

```powershell
python -m unittest discover -s tests -v
python scripts/probar_api.py
python scripts/probar_conexion_sql.py
```

Cuando ambas pruebas sean satisfactorias, inicia la aplicación:

```powershell
python app.py
```

Abre `http://127.0.0.1:5000` en el navegador. Pulsa **Consultar API y guardar registros**. Luego usa el campo de búsqueda para filtrar por municipio, nombre del evento o código.

## 8. Prevención de duplicados

La fuente no expone un identificador único de fila entre los ocho campos descritos. Por eso la aplicación genera una huella SHA-256 a partir del JSON completo y la almacena en `id_api`, que tiene una restricción `UNIQUE` en SQL Server. Una sincronización repetida de los mismos registros no vuelve a insertarlos.

## 9. Resumen numérico y alcance

La página calcula sobre los registros almacenados: número de filas, suma de `conteo_casos`, municipios distintos y códigos de evento distintos. La tabla web presenta hasta 100 filas por consulta.

El alcance implementado es consulta de API, lectura de JSON, persistencia en SQL Server, consulta SELECT, filtro, resumen y separación MVC. No implementa CRUD administrativo, autenticación de usuarios ni edición o eliminación desde la web, porque no forman parte del alcance reducido indicado en la guía académica.

## 10. Estructura del repositorio

```text
Proyecto_SIVIGILA_2018_Salud_Publica/
├── api/
│   ├── __init__.py
│   └── api_client.py
├── docs/
│   ├── ENTREGA_EVA.md
│   ├── ARQUITECTURA_MVC.md
│   ├── FICHA_CONJUNTO_DATOS.md
│   ├── GUIA_EVIDENCIAS.md
│   └── GUION_SUSTENTACION.md
├── models/
│   ├── __init__.py
│   └── datos_model.py
├── presentation/
│   └── Presentacion_SIVIGILA_2018.pptx
├── scripts/
│   ├── probar_api.py
│   └── probar_conexion_sql.py
├── sql/
│   └── crear_base_datos.sql
├── static/
│   └── estilos.css
├── templates/
│   └── index.html
├── tests/
│   └── test_modelo.py
├── evidencias/
│   └── LEEME.txt
├── .env.example
├── .gitignore
├── app.py
└── requirements.txt
```

## 11. Subir a GitHub

Perfil de GitHub: [jeancarlosperezpacheco2000-png](https://github.com/jeancarlosperezpacheco2000-png).

Crea en GitHub un repositorio público llamado `Proyecto-SIVIGILA-2018-Salud-Publica`. No marques la opción para inicializarlo con README. Luego abre la terminal de VS Code desde esta carpeta y ejecuta:

```bash
git init
git add .
git commit -m "Entrega proyecto SIVIGILA 2018"
git branch -M main
git remote add origin https://github.com/jeancarlosperezpacheco2000-png/Proyecto-SIVIGILA-2018-Salud-Publica.git
git push -u origin main
```

Comprueba en el navegador que el repositorio muestre las carpetas y archivos. **No subas `.env`, `venv/`, credenciales ni contraseñas.** El archivo `.gitignore` excluye `.env` y el entorno virtual.

## 12. Entrega en EVA

La actividad de EVA solicita el enlace del repositorio público. Consulta `docs/ENTREGA_EVA.md` para los pasos exactos y el enlace previsto. La entrega es individual.

## 13. Evidencias que deben añadirse después de ejecutar el proyecto

Guarda capturas reales en EVA o en una carpeta local de evidencias: respuesta JSON de la API, base y tabla en SSMS, registros insertados, página principal, mensaje de sincronización y consulta filtrada. Ejecuta dos veces la sincronización y comprueba que la segunda no duplique los identificadores. No se incluyen capturas simuladas: deben generarse en el equipo donde se ejecute la aplicación.

## 14. Autor

**Jean Carlos Pérez Pacheco**  
Proyecto académico – Desarrollo de Aplicaciones con Acceso a Datos.
