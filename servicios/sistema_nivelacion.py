from modelos.aula import Aula
from modelos.carga_academica import CargaAcademica
from modelos.curso_nivelacion import CursoNivelacion
from modelos.horario import Horario
from modelos.iexportable import ExportarExcel, ExportarPDF
from modelos.reporte import Reporte
from modelos.admin import Administrador
from modelos.docente import Docente
from modelos.estudiante import Estudiante
from servicios.fabrica import FabricaUsuario


class SistemaNivelacion:

    def __init__(self):
        self.fabrica = FabricaUsuario()
        self.usuarios = []
        self.aulas = []
        self.horarios = []
        self.cursos = []
        self.cargas_academicas = []
        self.reportes = []

    def registrar_usuario(self, tipo_usuario, cedula, nombres, apellidos, correo, contrasena, telefono, **datos):
        id_usuario = len(self.usuarios) + 1

        if tipo_usuario == "Docente":
            usuario = self.fabrica.crear_usuario(
                "Docente",
                id_usuario,
                cedula,
                nombres,
                apellidos,
                correo,
                contrasena,
                telefono,
                datos.get("titulo_profesional", ""),
                datos.get("especialidad", ""),
            )
        elif tipo_usuario == "Estudiante":
            usuario = self.fabrica.crear_usuario(
                "Estudiante",
                id_usuario,
                cedula,
                nombres,
                apellidos,
                correo,
                contrasena,
                telefono,
                datos.get("tipo_documento", "Cedula"),
                datos.get("numero_documento", cedula),
                datos.get("fecha_nacimiento", ""),
                datos.get("discapacidad", False),
            )
        elif tipo_usuario == "Administrador":
            usuario = self.fabrica.crear_usuario(
                "Administrador",
                id_usuario,
                cedula,
                nombres,
                apellidos,
                correo,
                contrasena,
                telefono,
                len([u for u in self.usuarios if isinstance(u, Administrador)]) + 1,
                datos.get("cargo", ""),
            )
        else:
            raise ValueError("Tipo de usuario no valido")

        self.usuarios.append(usuario)
        return usuario

    def registrar_aula(self, codigo, nombre, capacidad, piso, edificio):
        aula = Aula(len(self.aulas) + 1, codigo, nombre, int(capacidad), int(piso), edificio)
        self.aulas.append(aula)
        return aula

    def registrar_horario(self, dia, hora_inicio, hora_fin, modalidad, grupo, aula):
        horario = Horario(len(self.horarios) + 1, dia, hora_inicio, hora_fin, modalidad, grupo, aula)
        self.horarios.append(horario)
        return horario

    def registrar_curso(self, codigo, nombre, nivel, paralelo, cupo_maximo, docente, horario, aula):
        curso = CursoNivelacion(
            len(self.cursos) + 1,
            codigo,
            nombre,
            nivel,
            paralelo,
            int(cupo_maximo),
            docente,
            horario,
            aula,
        )
        self.cursos.append(curso)
        return curso

    def inscribir_estudiante(self, curso, estudiante):
        if estudiante in curso.lista_estudiantes:
            raise ValueError("El estudiante ya esta inscrito en este curso")
        curso.agregar_estudiante(estudiante)
        estudiante.estado_nivelacion = "En Curso"
        return curso

    def registrar_carga_academica(self, total_asignaturas, total_creditos):
        carga = CargaAcademica(len(self.cargas_academicas) + 1, int(total_asignaturas), int(total_creditos))
        self.cargas_academicas.append(carga)
        return carga

    def generar_reporte(self, tipo_reporte, fecha_generacion, periodo, descripcion, formato):
        exportador = ExportarExcel() if formato == "Excel" else ExportarPDF()
        reporte = Reporte(
            len(self.reportes) + 1,
            tipo_reporte,
            fecha_generacion,
            periodo,
            descripcion,
            exportador,
        )
        self.reportes.append(reporte)
        return reporte

    def listar_docentes(self):
        return [usuario for usuario in self.usuarios if isinstance(usuario, Docente)]

    def listar_estudiantes(self):
        return [usuario for usuario in self.usuarios if isinstance(usuario, Estudiante)]

    def resumen(self):
        return {
            "usuarios": len(self.usuarios),
            "docentes": len(self.listar_docentes()),
            "estudiantes": len(self.listar_estudiantes()),
            "cursos": len(self.cursos),
            "aulas": len(self.aulas),
            "cargas": len(self.cargas_academicas),
            "reportes": len(self.reportes),
        }

    def cargar_datos_demo(self):
        if self.usuarios or self.aulas or self.cursos:
            return

        docente = self.registrar_usuario(
            "Docente",
            "1300001111",
            "Valentin",
            "Perez",
            "perez123@uleam.edu.ec",
            "doc123",
            "0991234567",
            titulo_profesional="Magister en Software",
            especialidad="Programacion OO",
        )
        estudiante1 = self.registrar_usuario(
            "Estudiante",
            "1300002222",
            "Maykel",
            "Castro",
            "mcastro@uleam.edu.ec",
            "est123",
            "0997654321",
            tipo_documento="Cedula",
            numero_documento="1300002222",
            fecha_nacimiento="2005-03-15",
        )
        estudiante2 = self.registrar_usuario(
            "Estudiante",
            "1300003333",
            "Bryan",
            "Chiquito",
            "bchiquito@uleam.edu.ec",
            "est456",
            "0994567890",
            tipo_documento="Cedula",
            numero_documento="1300003333",
            fecha_nacimiento="2004-07-22",
        )
        self.registrar_usuario(
            "Administrador",
            "1300004444",
            "Carlos",
            "Ortiz",
            "cortiz@uleam.edu.ec",
            "adm123",
            "0993456789",
            cargo="Director de Nivelacion",
        )

        aula = self.registrar_aula("A101", "Aula 101", 35, 1, "Bloque A")
        horario = self.registrar_horario("Lunes", "08:00", "10:00", "Presencial", "A", aula)
        curso = self.registrar_curso("POO-001", "Programacion Orientada a Objetos", "Nivelacion", "A", 30, docente, horario, aula)
        self.inscribir_estudiante(curso, estudiante1)
        self.inscribir_estudiante(curso, estudiante2)
        self.registrar_carga_academica(5, 20)
        self.generar_reporte("Asistencia", "2026-06-17", "2026-1", "Reporte general de asistencia", "PDF")

