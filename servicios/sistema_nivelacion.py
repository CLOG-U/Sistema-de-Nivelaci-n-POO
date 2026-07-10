from datetime import date

from modelos.admin import Administrador
from modelos.asistencia import Asistencia
from modelos.aula import Aula
from modelos.calificacion import Calificacion
from modelos.carga_academica import CargaAcademica
from modelos.curso_nivelacion import CursoNivelacion
from modelos.docente import Docente
from modelos.estudiante import Estudiante
from modelos.horario import Horario
from modelos.iexportable import ExportarExcel, ExportarPDF
from modelos.periodo_academico import PeriodoAcademico
from modelos.reporte import Reporte
from servicios.BaseD import ConexionDB
from servicios.fabrica import FabricaUsuario
from servicios.matricula_facade import MatriculaFacade
from servicios.repositorios.persistencia import PersistenciaSQL

# Clase principal del Sistema de Nivelación
class SistemaNivelacion:
    # Constante que representa los créditos asignados a cada curso.
    CREDITOS_POR_CURSO = 4

    def __init__(self):
        # Crea la fábrica de usuarios.
        self.fabrica = FabricaUsuario()
        self.periodos = {}
        self.matriculas = {}
        self.calificaciones = {}
        self.asistencias = {}
        self.periodo_actual = None
        self.periodos_disponibles = []

        self.db = ConexionDB()
        self._persistencia = PersistenciaSQL(self.db)
        self._db_activa = False
        self.usuarios = {}
        self.aulas = {}
        self.horarios = {}
        self.cursos = {}
        self.cargas_academicas = {}
        self.reportes = {}

    # Inicializa los períodos académicos por defecto
    def _inicializar_periodos(self):
        if self.periodos:
            return
        periodo1 = PeriodoAcademico(1, "2026-1", "2026-01-01", "2026-06-30", "Abierto")
        periodo2 = PeriodoAcademico(2, "2026-2", "2026-07-01", "2026-12-15", "Cerrado")
        self.periodos[periodo1.id_periodo] = periodo1
        self.periodos[periodo2.id_periodo] = periodo2
        self._sincronizar_periodos_disponibles()
        self.periodo_actual = periodo1.nombre

    # Sincroniza la lista de períodos disponibles
    def _sincronizar_periodos_disponibles(self):
        self.periodos_disponibles = [periodo.nombre for periodo in self.periodos.values()]

    # Registra un nuevo período académico
    def registrar_periodo(self, nombre, fecha_inicio, fecha_fin, estado="Abierto"):
        if self.obtener_periodo(nombre):
            raise ValueError("Ya existe un periodo con ese nombre")
        id_periodo = self._siguiente_id(self.periodos, "PeriodoAcademico", "id_periodo")
        periodo = PeriodoAcademico(id_periodo, nombre, fecha_inicio, fecha_fin, estado)
        self.periodos[id_periodo] = periodo
        self._sincronizar_periodos_disponibles()
        if self._db_activa:
            self._persistencia.guardar_periodo(periodo)
        return periodo

    # Establece el período académico actual
    def establecer_periodo_actual(self, nombre_periodo):
        periodo = self.obtener_periodo(nombre_periodo)
        if not periodo:
            raise ValueError("Periodo academico no valido")
        self.periodo_actual = periodo.nombre
        return periodo

    # Abre un período académico
    def abrir_periodo(self, nombre_periodo):
        periodo = self.obtener_periodo(nombre_periodo)
        if not periodo:
            raise ValueError("Periodo academico no valido")
        periodo.abrir_periodo()
        if self._db_activa:
            self._persistencia.actualizar_periodo(periodo)
        return periodo

    # Cierra un período académico
    def cerrar_periodo(self, nombre_periodo):
        periodo = self.obtener_periodo(nombre_periodo)
        if not periodo:
            raise ValueError("Periodo academico no valido")
        periodo.cerrar_periodo()
        if self._db_activa:
            self._persistencia.actualizar_periodo(periodo)
        return periodo

    # Obtiene un período por nombre o ID
    def obtener_periodo(self, nombre_o_id):
        for periodo in self.periodos.values():
            if periodo.nombre == nombre_o_id or periodo.id_periodo == nombre_o_id:
                return periodo
        return None

    # Retorna el período académico actual
    def obtener_periodo_actual(self):
        return self.obtener_periodo(self.periodo_actual)

    # Retorna una lista de todos los períodos académicos
    def listar_periodos_academicos(self):
        return list(self.periodos.values())

    # Retorna los períodos académicos con estado Abierto
    def listar_periodos_abiertos(self):
        return [periodo for periodo in self.periodos.values() if periodo.estado == "Abierto"]

    # Gestiona usuarios (activar, desactivar, suspender)
    def gestionar_usuario(self, administrador, accion, usuario, motivo=None, fecha=None):
        if not isinstance(administrador, Administrador):
            raise ValueError("Solo un administrador puede gestionar usuarios")
        resultado = administrador.gestionar_usuario(accion, usuario, motivo, fecha)
        if self._db_activa:
            self._persistencia.actualizar_usuario(usuario)
        return resultado

    # Gestiona cursos (crear, modificar, eliminar)
    def gestionar_curso(self, administrador, accion, curso):
        if not isinstance(administrador, Administrador):
            raise ValueError("Solo un administrador puede gestionar cursos")
        resultado = administrador.gestionar_cursos(accion, curso)
        if self._db_activa:
            self._persistencia.actualizar_curso(curso)
        return resultado

    # Actualiza información de un usuario (correo y teléfono)
    def actualizar_usuario(self, usuario, correo=None, telefono=None):
        if correo is not None:
            usuario.correo = correo.strip()
        if telefono is not None:
            usuario.telefono = telefono.strip()
        if self._db_activa:
            self._persistencia.actualizar_usuario(usuario)
        return usuario

    # Prueba la conexión a SQL Server
    def probar_conexion_db(self):
        try:
            conexion = self.db.conectar(silencioso=True)
            if conexion:
                self.db.cerrar()
                return True, "Conexion a SQL Server establecida correctamente."
            detalle = self.db.ultimo_error or "Revise secrets.toml y que el servidor sea accesible."
            return False, f"No se pudo establecer la conexion. {detalle}"
        except Exception as error:
            return False, f"Error de conexion: {error}"

    # Carga datos desde la base de datos
    def cargar_desde_db(self):
        ok, mensaje = self._persistencia.cargar(self)
        self._db_activa = ok
        return ok, mensaje

    # Inicializa datos del sistema (desde BD o en memoria)
    def inicializar_datos(self):
        ok, mensaje = self.cargar_desde_db()
        if ok:
            return True, mensaje, "sql"

        self._inicializar_periodos()
        self.cargar_datos_demo()
        aviso = (
            "SQL Server no disponible. La aplicacion inicio en modo demostracion en memoria. "
            "Los cambios no se guardaran en BD hasta configurar una conexion valida."
        )
        if mensaje:
            aviso = f"{aviso} Detalle: {mensaje}"
        return False, aviso, "demo"

    # Busca un usuario por cédula o correo electrónico
    def buscar_usuario_por_identificador(self, identificador):
        identificador = identificador.strip()
        identificador_lower = identificador.lower()
        for usuario in self.usuarios.values():
            if usuario.cedula == identificador:
                return usuario
            if usuario.correo.lower() == identificador_lower:
                return usuario
        return None

    # Genera el siguiente ID disponible para una tabla
    def _siguiente_id(self, diccionario, tabla=None, columna=None):
        if self._db_activa and tabla and columna:
            nuevo_id = self._persistencia.siguiente_id(tabla, columna)
            if nuevo_id:
                return nuevo_id
        return len(diccionario) + 1

    # Registra un nuevo usuario (Docente, Estudiante o Administrador)
    def registrar_usuario(self, tipo_usuario, cedula, nombres, apellidos, correo, contrasena, telefono, **datos):
        # Genera un ID automático.
        id_usuario = self._siguiente_id(self.usuarios, "Usuario", "id_usuario")
        # Si es un docente.
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
        # Si es un estudiante.
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
        # Si es un administrador.
        elif tipo_usuario == "Administrador":
            # Cuenta cuántos administradores existen.
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
        # Si el tipo no existe.
        else:
            raise ValueError("Tipo de usuario no valido")
        # Guarda el usuario en el diccionario.
        self.usuarios[id_usuario] = usuario
        if self._db_activa:
            self._persistencia.guardar_usuario(usuario, tipo_usuario, datos)
        return usuario

    # Registra un aula con sus datos específicos
    def registrar_aula(self, codigo, nombre, capacidad, piso, edificio):
        # Genera un ID.
        id_aula = self._siguiente_id(self.aulas, "Aula", "id_aula")
        aula = Aula(id_aula, codigo, nombre, int(capacidad), int(piso), edificio)
        self.aulas[id_aula] = aula
        if self._db_activa:
            self._persistencia.guardar_aula(aula)
        return aula

    # Registra un horario para un curso
    def registrar_horario(self, dia, hora_inicio, hora_fin, modalidad, grupo, aula):
        # Genera un ID.
        id_horario = self._siguiente_id(self.horarios, "Horario", "id_horario")
        horario = Horario(id_horario, dia, hora_inicio, hora_fin, modalidad, grupo, aula)
        self.horarios[id_horario] = horario
        if self._db_activa:
            self._persistencia.guardar_horario(horario)
        return horario

    # Registra un nuevo curso de nivelación
    def registrar_curso(self, codigo, nombre, nivel, paralelo, cupo_maximo, docente, horario, aula):
        id_curso = self._siguiente_id(self.cursos, "CursoNivelacion", "id_curso")
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
        if self._db_activa:
            self._persistencia.guardar_curso(curso)
        return curso

    # Inscribe un estudiante en un curso
    def inscribir_estudiante(self, curso, estudiante, periodo=None, tipo_matricula="Regular", fecha=None):
        if estudiante in curso.lista_estudiantes:
            raise ValueError("El estudiante ya esta inscrito en este curso")
        if curso.cupo_actual >= curso.cupo_maximo:
            raise ValueError("No hay cupos disponibles en este curso")

        if isinstance(periodo, PeriodoAcademico):
            periodo_obj = periodo
        else:
            periodo_obj = self.obtener_periodo(periodo or self.periodo_actual)
        if not periodo_obj:
            raise ValueError("Periodo academico no valido")
        if periodo_obj.estado == "Cerrado":
            raise ValueError("No se puede matricular: el periodo esta cerrado")

        fecha_matricula = fecha or date.today().isoformat()
        id_matricula = self._siguiente_id(self.matriculas, "Matricula", "id_matricula")
        facade = MatriculaFacade(periodo_obj, curso, estudiante)
        if not facade.matricular(id_matricula, fecha_matricula, tipo_matricula):
            raise ValueError("No se pudo completar la matricula")

        matricula = estudiante.matricula
        self.matriculas[id_matricula] = matricula
        estudiante.estado_nivelacion = "En Curso"
        if self._db_activa:
            self._persistencia.guardar_matricula(self, matricula, estudiante, curso, periodo_obj)
        return matricula

    # Registra la carga académica de un estudiante
    def registrar_carga_academica(self, estudiante, periodo=None):
        cursos_estudiante = self.obtener_cursos_estudiante(estudiante)
        total_asignaturas = len(cursos_estudiante)
        if total_asignaturas == 0:
            raise ValueError("El estudiante no tiene cursos inscritos")

        periodo_nombre = periodo or self.periodo_actual
        if periodo_nombre not in self.periodos_disponibles:
            raise ValueError("Seleccione un periodo valido")

        for carga in self.cargas_academicas.values():
            if carga.estudiante == estudiante and carga.periodo == periodo_nombre:
                raise ValueError("El estudiante ya tiene una carga academica registrada en ese periodo")

        total_creditos = total_asignaturas * self.CREDITOS_POR_CURSO
        id_carga = self._siguiente_id(self.cargas_academicas, "CargaAcademica", "id_carga")
        carga = CargaAcademica(id_carga, estudiante, periodo_nombre, total_asignaturas, total_creditos)
        self.cargas_academicas[id_carga] = carga
        if self._db_activa:
            self._persistencia.guardar_carga(self, carga)
        return carga

    # Obtiene los cursos donde está inscrito un estudiante
    def obtener_cursos_estudiante(self, estudiante):
        return [curso for curso in self.cursos.values() if estudiante in curso.lista_estudiantes]

    # Retorna los períodos disponibles
    def listar_periodos(self):
        return self.periodos_disponibles

    # Registra una calificación para un estudiante en un curso
    def registrar_calificacion(self, docente, curso, estudiante, parcial1, parcial2, observacion=""):
        if curso.docente != docente:
            raise ValueError("El docente no es responsable de este curso")
        if estudiante not in curso.lista_estudiantes:
            raise ValueError("El estudiante no esta inscrito en este curso")

        for registro in self.calificaciones.values():
            if registro["estudiante"] == estudiante and registro["curso"] == curso:
                raise ValueError("Ya existe una calificacion registrada para este estudiante en el curso")

        id_calificacion = self._siguiente_id(self.calificaciones, "Calificacion", "id_calificacion")
        calificacion = Calificacion(id_calificacion, float(parcial1), float(parcial2))
        calificacion.calcular_promedio()
        calificacion.publicar_calificacion()
        docente.registrar_notas(
            id_calificacion,
            estudiante.id_usuario,
            float(parcial1),
            float(parcial2),
            observacion=observacion,
            fecha=date.today().isoformat(),
        )
        registro = {
            "calificacion": calificacion,
            "estudiante": estudiante,
            "curso": curso,
            "docente": docente,
            "periodo": self.periodo_actual,
        }
        self.calificaciones[id_calificacion] = registro
        if self._db_activa:
            self._persistencia.guardar_calificacion(registro)
        return calificacion

    # Registra la asistencia de un estudiante a una clase
    def registrar_asistencia(self, docente, curso, estudiante, fecha, estado, observacion=""):
        if curso.docente != docente:
            raise ValueError("El docente no es responsable de este curso")
        if estudiante not in curso.lista_estudiantes:
            raise ValueError("El estudiante no esta inscrito en este curso")

        id_asistencia = self._siguiente_id(self.asistencias, "Asistencia", "id_asistencia")
        asistencia = Asistencia(id_asistencia, fecha, estado, observacion)
        asistencia.anotar_asistencia(estado, observacion)
        docente.registrar_asistencia(fecha, estado, estudiante.id_usuario)
        registro = {
            "asistencia": asistencia,
            "estudiante": estudiante,
            "curso": curso,
            "docente": docente,
            "periodo": self.periodo_actual,
        }
        self.asistencias[id_asistencia] = registro
        if self._db_activa:
            self._persistencia.guardar_asistencia(registro)
        return asistencia

    # Obtiene las calificaciones de un estudiante
    def obtener_calificaciones_estudiante(self, estudiante, periodo=None):
        registros = [
            registro
            for registro in self.calificaciones.values()
            if registro["estudiante"] == estudiante
        ]
        if periodo:
            registros = [registro for registro in registros if registro["periodo"] == periodo]
        return registros

    # Obtiene las asistencias de un estudiante
    def obtener_asistencias_estudiante(self, estudiante, periodo=None):
        registros = [
            registro
            for registro in self.asistencias.values()
            if registro["estudiante"] == estudiante
        ]
        if periodo:
            registros = [registro for registro in registros if registro["periodo"] == periodo]
        return registros

    # Genera un resumen de datos para reportes
    def resumen_datos_reporte(self, tipo_reporte, periodo):
        if tipo_reporte == "Asistencia":
            total = sum(
                1 for registro in self.asistencias.values() if registro["periodo"] == periodo
            )
            presentes = sum(
                1
                for registro in self.asistencias.values()
                if registro["periodo"] == periodo and registro["asistencia"].estado == "Presente"
            )
            return f"Asistencias: {total} registros, {presentes} presentes"
        if tipo_reporte == "Calificaciones":
            registros = [
                registro
                for registro in self.calificaciones.values()
                if registro["periodo"] == periodo
            ]
            if not registros:
                return "Calificaciones: 0 registros"
            promedio = round(
                sum(registro["calificacion"].nota_final for registro in registros) / len(registros),
                2,
            )
            return f"Calificaciones: {len(registros)} registros, promedio {promedio}"
        if tipo_reporte == "Inscripciones":
            return f"Inscripciones: {self.total_inscripciones()} estudiantes en cursos"
        if tipo_reporte == "Carga academica":
            cargas = [
                carga for carga in self.cargas_academicas.values() if carga.periodo == periodo
            ]
            creditos = sum(carga.total_creditos for carga in cargas)
            return f"Cargas academicas: {len(cargas)} registros, {creditos} creditos"
        usuarios = len(self.usuarios)
        cursos = len(self.cursos)
        return f"General: {usuarios} usuarios, {cursos} cursos, periodo {periodo}"

    # Genera un reporte en formato Excel o PDF
    def generar_reporte(self, tipo_reporte, periodo, descripcion, formato):
        if periodo not in self.periodos_disponibles:
            raise ValueError("Seleccione un periodo valido")

        resumen_datos = self.resumen_datos_reporte(tipo_reporte, periodo)
        descripcion_completa = f"{descripcion.strip()} | {resumen_datos}"
        exportador = ExportarExcel() if formato == "Excel" else ExportarPDF()
        fecha_generacion = date.today().isoformat()

        id_reporte = self._siguiente_id(self.reportes, "Reporte", "id_reporte")
        reporte = Reporte(
            id_reporte,
            tipo_reporte,
            fecha_generacion,
            periodo,
            descripcion_completa,
            exportador,
        )
        self.reportes[id_reporte] = reporte
        if self._db_activa:
            self._persistencia.guardar_reporte(self, reporte)
        return reporte

    # Devuelve todos los docentes del sistema
    def listar_docentes(self):
        return [usuario for usuario in self.usuarios.values() if isinstance(usuario, Docente)]

    # Devuelve todos los estudiantes del sistema
    def listar_estudiantes(self):
        return [usuario for usuario in self.usuarios.values() if isinstance(usuario, Estudiante)]

    # Devuelve todos los administradores del sistema
    def listar_administradores(self):
        return [usuario for usuario in self.usuarios.values() if isinstance(usuario, Administrador)]

    # Calcula el total de inscripciones en todos los cursos
    def total_inscripciones(self):
        return sum(len(curso.lista_estudiantes) for curso in self.cursos.values())

    # Genera un resumen de horarios agrupados por día
    def resumen_horarios_por_dia(self):
        resumen = {}
        for horario in self.horarios.values():
            resumen[horario.dia] = resumen.get(horario.dia, 0) + 1
        return resumen

    # Devuelve un resumen completo del estado del sistema
    def resumen(self):
        return {
            "usuarios": len(self.usuarios),
            "docentes": len(self.listar_docentes()),
            "estudiantes": len(self.listar_estudiantes()),
            "cursos": len(self.cursos),
            "aulas": len(self.aulas),
            "cargas": len(self.cargas_academicas),
            "reportes": len(self.reportes),
            "matriculas": len(self.matriculas),
            "calificaciones": len(self.calificaciones),
            "asistencias": len(self.asistencias),
            "periodos": len(self.periodos),
        }

    # Carga datos de prueba para demostrar el funcionamiento del sistema
    def cargar_datos_demo(self):
        self._inicializar_periodos()
        if self.usuarios or self.aulas or self.cursos:
            return
        # Registra un docente.
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
        # Registra estudiantes
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
        # Registra un administrador.
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
        # Registra un aula.
        aula = self.registrar_aula("A101", "Aula 101", 35, 1, "Bloque A")
        # Registra un horario.
        horario = self.registrar_horario("Lunes", "08:00", "10:00", "Presencial", "A", aula)
        # Registra un curso.
        curso = self.registrar_curso("POO-001", "Programacion Orientada a Objetos", "Nivelacion", "A", 30, docente, horario, aula)
        # Inscribe estudiantes.
        self.inscribir_estudiante(curso, estudiante1)
        self.inscribir_estudiante(curso, estudiante2)
        self.registrar_calificacion(docente, curso, estudiante1, 8.5, 9.0, observacion="Buen desempeno")
        self.registrar_calificacion(docente, curso, estudiante2, 6.5, 7.5, observacion="Mejora continua")
        self.registrar_asistencia(docente, curso, estudiante1, "2026-03-10", "Presente")
        self.registrar_asistencia(docente, curso, estudiante2, "2026-03-10", "Ausente", observacion="Falta justificada pendiente")
        self.registrar_carga_academica(estudiante1)
        self.generar_reporte("Asistencia", "2026-1", "Reporte general de asistencia", "PDF")
