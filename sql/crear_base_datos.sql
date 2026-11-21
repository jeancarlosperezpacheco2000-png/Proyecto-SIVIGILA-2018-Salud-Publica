/* Base de datos del proyecto: SIVIGILA 2018 */
IF DB_ID(N'SIVIGILA2018DB') IS NULL
BEGIN
    CREATE DATABASE SIVIGILA2018DB;
END;
GO

USE SIVIGILA2018DB;
GO

IF OBJECT_ID(N'dbo.RegistrosSivigila2018', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.RegistrosSivigila2018
    (
        id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_RegistrosSivigila2018 PRIMARY KEY,
        id_api CHAR(64) NOT NULL,
        cod_eve INT NULL,
        nombre NVARCHAR(250) NULL,
        ano INT NULL,
        semana INT NULL,
        cod_dpto_o INT NULL,
        nom_mun NVARCHAR(200) NULL,
        cod_mun_o INT NULL,
        conteo_casos BIGINT NULL,
        json_original NVARCHAR(MAX) NOT NULL,
        fecha_captura DATETIME2(0) NOT NULL CONSTRAINT DF_RegistrosSivigila2018_fecha DEFAULT SYSDATETIME(),
        CONSTRAINT UQ_RegistrosSivigila2018_id_api UNIQUE (id_api)
    );

    CREATE INDEX IX_RegistrosSivigila2018_municipio
        ON dbo.RegistrosSivigila2018(nom_mun);
    CREATE INDEX IX_RegistrosSivigila2018_evento
        ON dbo.RegistrosSivigila2018(nombre);
END;
GO

/* Verificación inicial: debe devolver la tabla creada y cero filas al inicio. */
SELECT COUNT(*) AS registros_almacenados
FROM dbo.RegistrosSivigila2018;
GO
