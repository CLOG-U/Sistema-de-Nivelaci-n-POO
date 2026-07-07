from datetime import date  

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
from datetime import date
from servicios.BaseD import ConexionDB  # <--- Aquí importamos tu clase de base de datos

class SistemaNivelacion:

    CREDITOS_POR_CURSO = 4

    def __init__(self):
        self.fabrica = FabricaUsuario()
        self.periodo_actual = "2026-1"
        self.periodos_disponibles = [self.periodo_actual] 
        
        # Instanciamos la conexión a la base de datos
        self.db = ConexionDB()
        
        self.usuarios = {}
        self.aulas = {}
        self.horarios = {}
        self.cursos = {}
        self.cargas_academicas = {}
        self.reportes = {}

    def guardar_usuarios_en_db(self):
        try:
            self.db.conectar()
            

            query = "INSERT INTO usuarios (id, nombres, apellidos) VALUES (%s, %s, %s)"
            
            for id_usuario, usuario in self.usuarios.items():
                valores = (id_usuario, usuario.nombres, usuario.apellidos)
                self.db.cursor.execute(query, valores)
            
            self.db.conn.commit()  
            print(f"Se guardaron {len(self.usuarios)} usuarios exitosamente.")
            
        except Exception as e:
            print(f"Error al guardar en la base de datos: {e}")
            
        finally:
            self.db.cerrar()  

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
                datos.get("fecha_nacimiento", ""),
                datos.get("discapacidad", False),
            )
        elif tipo_usuario == "Administrador":
            # Uso de .values() para iterar sobre los elementos del diccionario
            cantidad_admins = sum(1 for u in self.usuarios.values() if isinstance(u, Administrador))
            usuario = self.fabrica.crear_usuario(
                "Administrador",
                id_usuario,
                cedula,
                nombres,
                apellidos,
                correo,
                contrasena,
                telefono,
                cantidad_admins + 1,
                datos.get("cargo", ""),
            )
        else:
            raise ValueError("Tipo de usuario no valido")

        self.usuarios[id_usuario] = usuario
        return usuario

    def registrar_aula(self, codigo, nombre, capacidad, piso, edificio):
        id_aula = len(self.aulas) + 1
        aula = Aula(id_aula, codigo, nombre, int(capacidad), int(piso), edificio)
        self.aulas[id_aula] = aula
        return aula

    def registrar_horario(self, dia, hora_inicio, hora_fin, modalidad, grupo, aula):
        id_horario = len(self.horarios) + 1
        horario = Horario(id_horario, dia, hora_inicio, hora_fin, modalidad, grupo, aula)
        self.horarios[id_horario] = horario
        return horario

    def registrar_curso(self, codigo, nombre, nivel, paralelo, cupo_maximo, docente, horario, aula):
        id_curso = len(self.cursos) + 1
        curso = CursoNivelacion(
            id_curso,
            codigo,
            nombre,
            nivel,
            paralelo,
            int(cupo_maximo),
            docente,
            horario,
            aula,
        )
        self.cursos[id_curso] = curso
        return curso

    def inscribir_estudiante(self, curso, estudiante):
        if estudiante in curso.lista_estudiantes:
            raise ValueError("El estudiante ya esta inscrito en este curso")
        curso.agregar_estudiante(estudiante)
        estudiante.estado_nivelacion = "En Curso"
        return curso

    def registrar_carga_academica(self, estudiante):
        cursos_estudiante = self.obtener_cursos_estudiante(estudiante)
        total_asignaturas = len(cursos_estudiante)
        
        if total_asignaturas == 0:
            raise ValueError("El estudiante no tiene cursos inscritos")

        for carga in self.cargas_academicas.values():
            if carga.estudiante == estudiante and carga.periodo == self.periodo_actual:
                raise ValueError("El estudiante ya tiene una carga academica registrada en el periodo actual")

        total_creditos = total_asignaturas * self.CREDITOS_POR_CURSO
        id_carga = len(self.cargas_academicas) + 1
        carga = CargaAcademica(id_carga, estudiante, self.periodo_actual, total_asignaturas, total_creditos)
        self.cargas_academicas[id_carga] = carga
        return carga

    def obtener_cursos_estudiante(self, estudiante):
        return [curso for curso in self.cursos.values() if estudiante in curso.lista_estudiantes]

    def listar_periodos(self):
        return self.periodos_disponibles

    def generar_reporte(self, tipo_reporte, periodo, descripcion, formato):
        if periodo not in self.periodos_disponibles:
            raise ValueError("Seleccione un periodo valido")
        exportador = ExportarExcel() if formato == "Excel" else ExportarPDF()
        fecha_generacion = date.today().isoformat()
        
        id_reporte = len(self.reportes) + 1
        reporte = Reporte(
            id_reporte,
            tipo_reporte,
            fecha_generacion,
            periodo,
            descripcion,
            exportador,
        )
        self.reportes[id_reporte] = reporte
        return reporte

    def listar_docentes(self):
        return [usuario for usuario in self.usuarios.values() if isinstance(usuario, Docente)]

    def listar_estudiantes(self):
        return [usuario for usuario in self.usuarios.values() if isinstance(usuario, Estudiante)]

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
        self.registrar_carga_academica(estudiante1)
        self.generar_reporte("Asistencia", "2026-1", "Reporte general de asistencia", "PDF")
