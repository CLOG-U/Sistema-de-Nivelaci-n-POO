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

CREATE TABLE Usuario(
    id_usuario INT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(120) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    estado BIT NOT NULL
);

CREATE TABLE Administrador(
    id_usuario INT PRIMARY KEY,
    id_administrador INT UNIQUE NOT NULL,
    cargo VARCHAR(100) NOT NULL,

    FOREIGN KEY(id_usuario)
        REFERENCES Usuario(id_usuario)
);

CREATE TABLE Docente(
    id_usuario INT PRIMARY KEY,
    titulo_profesional VARCHAR(120),
    especialidad VARCHAR(120),

    FOREIGN KEY(id_usuario)
        REFERENCES Usuario(id_usuario)
);

CREATE TABLE Estudiante(
    id_usuario INT PRIMARY KEY,
    tipo_documento VARCHAR(30),
    fecha_nacimiento DATE,
    discapacidad BIT,

    FOREIGN KEY(id_usuario)
        REFERENCES Usuario(id_usuario)
);

CREATE TABLE Carrera(
    id_carrera INT PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(120),
    estado BIT,
    id_facultad INT NOT NULL,

    FOREIGN KEY(id_facultad)
        REFERENCES Facultad(id_facultad)
);

CREATE TABLE Aula(
    id_aula INT PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(100),
    capacidad INT,
    piso INT,
    edificio VARCHAR(100),
    estado BIT
);

CREATE TABLE Horario(
    id_horario INT PRIMARY KEY,
    dia VARCHAR(20),
    hora_inicio TIME,
    hora_fin TIME,
    modalidad VARCHAR(30),
    grupo VARCHAR(20),
    id_aula INT NOT NULL,

    FOREIGN KEY(id_aula)
        REFERENCES Aula(id_aula)
);

CREATE TABLE CursoNivelacion(
    id_curso INT PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(120),
    nivel VARCHAR(30),
    paralelo VARCHAR(10),
    cupo_maximo INT,
    cupo_actual INT DEFAULT 0,
    estado BIT,

    id_docente INT NOT NULL,
    id_horario INT NOT NULL,
    id_aula INT NOT NULL,

    FOREIGN KEY(id_docente)
        REFERENCES Docente(id_usuario),

    FOREIGN KEY(id_horario)
        REFERENCES Horario(id_horario),

    FOREIGN KEY(id_aula)
        REFERENCES Aula(id_aula)
);

CREATE TABLE Matricula(
    id_matricula INT PRIMARY KEY,
    fecha_matricula DATE,
    tipo_matricula VARCHAR(40),
    id_periodo INT NOT NULL,
    estado VARCHAR(20),
    observaciones VARCHAR(255),

    FOREIGN KEY(id_periodo)
        REFERENCES PeriodoAcademico(id_periodo)
);

CREATE TABLE CargaAcademica(
    id_carga INT PRIMARY KEY,

    id_estudiante INT NOT NULL,
    id_periodo INT NOT NULL,

    total_asignaturas INT,
    total_creditos INT,
    estado BIT,

    FOREIGN KEY(id_estudiante)
        REFERENCES Estudiante(id_usuario),

    FOREIGN KEY(id_periodo)
        REFERENCES PeriodoAcademico(id_periodo)
);

CREATE TABLE Asistencia(
    id_asistencia INT PRIMARY KEY,
    fecha DATE,
    estado VARCHAR(20),
    observacion VARCHAR(255)
);

CREATE TABLE DetalleAsistencia(
    id_detalle_asistencia INT IDENTITY(1,1) PRIMARY KEY,
    id_asistencia INT NOT NULL,
    tipo_justificacion VARCHAR(50),
    observacion VARCHAR(255),
    documento_soporte VARCHAR(255),

    FOREIGN KEY(id_asistencia)
        REFERENCES Asistencia(id_asistencia)
);
