IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'PROYECTOPOO')
BEGIN
    CREATE DATABASE PROYECTOPOO;
END
GO

USE PROYECTOPOO;
GO

IF OBJECT_ID('DetalleCalificacion', 'U') IS NOT NULL DROP TABLE DetalleCalificacion;
IF OBJECT_ID('DetalleAsistencia', 'U') IS NOT NULL DROP TABLE DetalleAsistencia;
IF OBJECT_ID('Reporte', 'U') IS NOT NULL DROP TABLE Reporte;
IF OBJECT_ID('CargaAcademica', 'U') IS NOT NULL DROP TABLE CargaAcademica;
IF OBJECT_ID('Calificacion', 'U') IS NOT NULL DROP TABLE Calificacion;
IF OBJECT_ID('Asistencia', 'U') IS NOT NULL DROP TABLE Asistencia;
IF OBJECT_ID('Matricula', 'U') IS NOT NULL DROP TABLE Matricula;
IF OBJECT_ID('CursoNivelacion', 'U') IS NOT NULL DROP TABLE CursoNivelacion;
IF OBJECT_ID('Horario', 'U') IS NOT NULL DROP TABLE Horario;
IF OBJECT_ID('Aula', 'U') IS NOT NULL DROP TABLE Aula;
IF OBJECT_ID('Carrera', 'U') IS NOT NULL DROP TABLE Carrera;
IF OBJECT_ID('Estudiante', 'U') IS NOT NULL DROP TABLE Estudiante;
IF OBJECT_ID('Docente', 'U') IS NOT NULL DROP TABLE Docente;
IF OBJECT_ID('Administrador', 'U') IS NOT NULL DROP TABLE Administrador;
IF OBJECT_ID('Usuario', 'U') IS NOT NULL DROP TABLE Usuario;
IF OBJECT_ID('PeriodoAcademico', 'U') IS NOT NULL DROP TABLE PeriodoAcademico;
IF OBJECT_ID('Facultad', 'U') IS NOT NULL DROP TABLE Facultad;
GO

CREATE TABLE Facultad(
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

CREATE TABLE Usuario(
    id_usuario INT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(120) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    estado BIT NOT NULL DEFAULT 1
);

CREATE TABLE Administrador(
    id_usuario INT PRIMARY KEY,
    id_administrador INT UNIQUE NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Docente(
    id_usuario INT PRIMARY KEY,
    titulo_profesional VARCHAR(120),
    especialidad VARCHAR(120),
    FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Estudiante(
    id_usuario INT PRIMARY KEY,
    tipo_documento VARCHAR(30),
    fecha_nacimiento DATE,
    discapacidad BIT DEFAULT 0,
    estado_nivelacion VARCHAR(50) DEFAULT 'Pendiente',
    FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Carrera(
    id_carrera INT PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(120),
    estado BIT,
    id_facultad INT NOT NULL,
    FOREIGN KEY(id_facultad) REFERENCES Facultad(id_facultad)
);

CREATE TABLE Aula(
    id_aula INT PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(100),
    capacidad INT,
    piso INT,
    edificio VARCHAR(100),
    estado BIT DEFAULT 1
);

CREATE TABLE Horario(
    id_horario INT PRIMARY KEY,
    dia VARCHAR(20),
    hora_inicio TIME,
    hora_fin TIME,
    modalidad VARCHAR(30),
    grupo VARCHAR(20),
    id_aula INT NOT NULL,
    FOREIGN KEY(id_aula) REFERENCES Aula(id_aula)
);

CREATE TABLE CursoNivelacion(
    id_curso INT PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(120),
    nivel VARCHAR(30),
    paralelo VARCHAR(10),
    cupo_maximo INT,
    cupo_actual INT DEFAULT 0,
    estado BIT DEFAULT 1,
    id_docente INT NOT NULL,
    id_horario INT NOT NULL,
    id_aula INT NOT NULL,
    FOREIGN KEY(id_docente) REFERENCES Docente(id_usuario),
    FOREIGN KEY(id_horario) REFERENCES Horario(id_horario),
    FOREIGN KEY(id_aula) REFERENCES Aula(id_aula)
);

CREATE TABLE Matricula(
    id_matricula INT PRIMARY KEY,
    fecha_matricula DATE,
    tipo_matricula VARCHAR(40),
    id_periodo INT NOT NULL,
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    estado VARCHAR(20),
    observaciones VARCHAR(255),
    FOREIGN KEY(id_periodo) REFERENCES PeriodoAcademico(id_periodo),
    FOREIGN KEY(id_estudiante) REFERENCES Estudiante(id_usuario),
    FOREIGN KEY(id_curso) REFERENCES CursoNivelacion(id_curso)
);

CREATE TABLE CargaAcademica(
    id_carga INT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_periodo INT NOT NULL,
    total_asignaturas INT,
    total_creditos INT,
    estado BIT DEFAULT 1,
    FOREIGN KEY(id_estudiante) REFERENCES Estudiante(id_usuario),
    FOREIGN KEY(id_periodo) REFERENCES PeriodoAcademico(id_periodo)
);

CREATE TABLE Asistencia(
    id_asistencia INT PRIMARY KEY,
    fecha DATE,
    estado VARCHAR(20),
    observacion VARCHAR(255),
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    id_docente INT NOT NULL,
    periodo VARCHAR(20),
    FOREIGN KEY(id_estudiante) REFERENCES Estudiante(id_usuario),
    FOREIGN KEY(id_curso) REFERENCES CursoNivelacion(id_curso),
    FOREIGN KEY(id_docente) REFERENCES Docente(id_usuario)
);

CREATE TABLE DetalleAsistencia(
    id_detalle_asistencia INT IDENTITY(1,1) PRIMARY KEY,
    id_asistencia INT NOT NULL,
    tipo_justificacion VARCHAR(50),
    observacion VARCHAR(255),
    documento_soporte VARCHAR(255),
    FOREIGN KEY(id_asistencia) REFERENCES Asistencia(id_asistencia)
);

CREATE TABLE Calificacion(
    id_calificacion INT PRIMARY KEY,
    nota_parcial1 DECIMAL(5,2),
    nota_parcial2 DECIMAL(5,2),
    estado VARCHAR(30),
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    id_docente INT NOT NULL,
    periodo VARCHAR(20),
    FOREIGN KEY(id_estudiante) REFERENCES Estudiante(id_usuario),
    FOREIGN KEY(id_curso) REFERENCES CursoNivelacion(id_curso),
    FOREIGN KEY(id_docente) REFERENCES Docente(id_usuario)
);

CREATE TABLE DetalleCalificacion(
    id_detalle INT PRIMARY KEY,
    id_calificacion INT NOT NULL,
    tipo_evaluacion VARCHAR(50),
    descripcion VARCHAR(255),
    puntaje_obtenido DECIMAL(5,2),
    puntaje_total DECIMAL(5,2),
    fecha_evaluacion DATE,
    FOREIGN KEY(id_calificacion) REFERENCES Calificacion(id_calificacion)
);

CREATE TABLE Reporte(
    id_reporte INT PRIMARY KEY,
    tipo_reporte VARCHAR(50),
    fecha_generacion DATE,
    id_periodo INT NOT NULL,
    descripcion VARCHAR(255),
    formato VARCHAR(20),
    FOREIGN KEY(id_periodo) REFERENCES PeriodoAcademico(id_periodo)
);
GO

-- Datos iniciales (usuarios de prueba, periodos, curso POO-001, etc.)
INSERT INTO Facultad VALUES (1, 'Facultad de Ingenieria Informatica y Ciencias Computacionales');

INSERT INTO PeriodoAcademico VALUES
(1, '2026-1', '2026-01-01', '2026-06-30', 'Abierto'),
(2, '2026-2', '2026-07-01', '2026-12-15', 'Cerrado');

INSERT INTO Usuario (id_usuario, cedula, nombres, apellidos, correo, contrasena, telefono, estado) VALUES
(1, '1300001111', 'Valentin', 'Perez', 'perez123@uleam.edu.ec', 'doc123', '0991234567', 1),
(2, '1300002222', 'Maykel', 'Castro', 'mcastro@uleam.edu.ec', 'est123', '0997654321', 1),
(3, '1300003333', 'Bryan', 'Chiquito', 'bchiquito@uleam.edu.ec', 'est456', '0994567890', 1),
(4, '1300004444', 'Carlos', 'Ortiz', 'cortiz@uleam.edu.ec', 'adm123', '0993456789', 1);

INSERT INTO Docente VALUES (1, 'Magister en Software', 'Programacion OO');

INSERT INTO Estudiante VALUES
(2, 'Cedula', '2005-03-15', 0, 'En Curso'),
(3, 'Cedula', '2004-07-22', 0, 'En Curso');

INSERT INTO Administrador VALUES (4, 1, 'Director de Nivelacion');

INSERT INTO Aula VALUES (1, 'A101', 'Aula 101', 35, 1, 'Bloque A', 1);

INSERT INTO Horario VALUES (1, 'Lunes', '08:00', '10:00', 'Presencial', 'A', 1);

INSERT INTO CursoNivelacion VALUES
(1, 'POO-001', 'Programacion Orientada a Objetos', 'Nivelacion', 'A', 30, 2, 1, 1, 1, 1);

INSERT INTO Matricula VALUES
(1, '2026-07-08', 'Regular', 1, 2, 1, 'Activa', ''),
(2, '2026-07-08', 'Regular', 1, 3, 1, 'Activa', '');

INSERT INTO Calificacion VALUES
(1, 8.50, 9.00, 'Publicada', 2, 1, 1, '2026-1'),
(2, 6.50, 7.50, 'Publicada', 3, 1, 1, '2026-1');

INSERT INTO Asistencia VALUES
(1, '2026-03-10', 'Presente', '', 2, 1, 1, '2026-1'),
(2, '2026-03-10', 'Ausente', 'Falta justificada pendiente', 3, 1, 1, '2026-1');

INSERT INTO CargaAcademica VALUES (1, 2, 1, 1, 4, 1);

INSERT INTO Reporte VALUES
(1, 'Asistencia', '2026-07-08', 1, 'Reporte general de asistencia | Asistencias: 2 registros, 1 presentes', 'PDF');
GO
