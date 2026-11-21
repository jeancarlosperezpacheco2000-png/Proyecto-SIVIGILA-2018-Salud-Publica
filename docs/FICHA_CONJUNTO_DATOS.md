# Ficha técnica del conjunto de datos

## Identificación

- **Nombre:** SIVIGILA 2018.
- **Tema:** Salud pública / vigilancia en salud pública.
- **Entidad suministradora:** Instituto Nacional de Salud (INS), Colombia.
- **Portal:** [datos.gov.co – SIVIGILA 2018](https://www.datos.gov.co/Salud-y-Protecci-n-Social/SIVIGILA-2018/xd2n-cu8j).
- **Identificador del recurso:** `xd2n-cu8j`.
- **Endpoint REST:** `https://www.datos.gov.co/resource/xd2n-cu8j.json`.
- **Formato:** JSON.
- **Cobertura declarada:** nacional.
- **Periodo de referencia de este conjunto:** año 2018.

## Descripción

El portal describe SIVIGILA como el Sistema Nacional de Vigilancia en Salud Pública, creado para suministrar información sistemática y oportuna sobre la dinámica de eventos que afecten o puedan afectar la salud de la población colombiana.

En la ficha del portal consultada el 20 de noviembre de 2026 se listan aproximadamente 194.000 filas y ocho columnas. La página de metadatos muestra actualización del 18 de mayo de 2026, mientras que la última actualización de los datos figura como 7 de enero de 2021. Por tanto, la información aquí utilizada se trata como histórica, correspondiente a 2018.

## Campos del recurso

| Campo API | Tipo indicado en portal |
|---|---|
| `cod_eve` | Número |
| `nombre` | Texto |
| `ano` | Número |
| `semana` | Número |
| `cod_dpto_o` | Número |
| `nom_mun` | Texto |
| `cod_mun_o` | Número |
| `conteo_casos` | Número |

## Propósito de uso académico

Consultar una muestra de hasta 100 filas desde la API pública, analizar su estructura JSON, conservar los ocho campos en SQL Server, evitar duplicados y mostrar búsquedas y un resumen de los registros almacenados.

## Consideración

El conjunto es histórico. El número de casos que muestra la aplicación representa los registros almacenados desde este recurso, no una medición actual de incidencia, prevalencia o riesgo sanitario.
