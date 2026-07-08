CREATE DATABASE PROYECTOPOO

CREATE CREATE TABLE Facultad(
    id_facultad INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE PeriodoAcademico(
    id_periodo INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado VARCHAR(20) NOT NULL
);
