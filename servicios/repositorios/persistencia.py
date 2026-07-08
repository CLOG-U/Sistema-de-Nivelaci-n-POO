"""Capa de persistencia SQL Server para SistemaNivelacion."""

from datetime import date, datetime, time

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
from modelos.matricula import Matricula
from modelos.periodo_academico import PeriodoAcademico
from modelos.reporte import Reporte


def _a_texto(valor):
    if valor is None:
        return ""
    if isinstance(valor, datetime):
        return valor.date().isoformat()
    if isinstance(valor, date):
        return valor.isoformat()
    if isinstance(valor, time):
        return valor.strftime("%H:%M")
    return str(valor)


def _a_bool(valor):
    if valor is None:
        return True
    return bool(valor)


class PersistenciaSQL:
    def __init__(self, db):
        self.db = db

    def cargar(self, sistema):
        if not self.db.conectar():
            return False, "No se pudo conectar a SQL Server."

        try:
            self._limpiar_memoria(sistema)
            self._cargar_periodos(sistema)
            self._cargar_usuarios(sistema)
            self._cargar_aulas(sistema)
            self._cargar_horarios(sistema)
            self._cargar_cursos(sistema)
            self._cargar_matriculas(sistema)
            self._cargar_calificaciones(sistema)
            self._cargar_asistencias(sistema)
            self._cargar_cargas(sistema)
            self._cargar_reportes(sistema)
            self._sincronizar_periodo_actual(sistema)
            return True, "Datos cargados desde SQL Server."
        except Exception as error:
            return False, f"Error al cargar datos: {error}"
        finally:
            self.db.cerrar()

    def _limpiar_memoria(self, sistema):
        sistema.periodos.clear()
        sistema.usuarios.clear()
        sistema.aulas.clear()
        sistema.horarios.clear()
        sistema.cursos.clear()
        sistema.matriculas.clear()
        sistema.calificaciones.clear()
        sistema.asistencias.clear()
        sistema.cargas_academicas.clear()
        sistema.reportes.clear()
        sistema.periodos_disponibles = []
        sistema.periodo_actual = None

    def _cargar_periodos(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT id_periodo, nombre, fecha_inicio, fecha_fin, estado FROM PeriodoAcademico"
        )
        for fila in filas:
            periodo = PeriodoAcademico(
                fila.id_periodo,
                fila.nombre,
                _a_texto(fila.fecha_inicio),
                _a_texto(fila.fecha_fin),
                fila.estado,
            )
            sistema.periodos[periodo.id_periodo] = periodo
        sistema.periodos_disponibles = [p.nombre for p in sistema.periodos.values()]

    def _cargar_usuarios(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT id_usuario, cedula, nombres, apellidos, correo, contrasena, telefono, estado FROM Usuario"
        )
        for fila in filas:
            uid = fila.id_usuario
            estado = _a_bool(fila.estado)

            admin = self.db.consultar_uno(
                "SELECT id_administrador, cargo FROM Administrador WHERE id_usuario = ?",
                (uid,),
            )
            if admin:
                usuario = Administrador(
                    uid,
                    fila.cedula,
                    fila.nombres,
                    fila.apellidos,
                    fila.correo,
                    fila.contrasena,
                    fila.telefono or "",
                    admin.id_administrador,
                    admin.cargo or "",
                )
                usuario.estado = estado
                sistema.usuarios[uid] = usuario
                continue

            docente = self.db.consultar_uno(
                "SELECT titulo_profesional, especialidad FROM Docente WHERE id_usuario = ?",
                (uid,),
            )
            if docente:
                usuario = Docente(
                    uid,
                    fila.cedula,
                    fila.nombres,
                    fila.apellidos,
                    fila.correo,
                    fila.contrasena,
                    fila.telefono or "",
                    docente.titulo_profesional or "",
                    docente.especialidad or "",
                )
                usuario.estado = estado
                sistema.usuarios[uid] = usuario
                continue

            estudiante = self.db.consultar_uno(
                "SELECT tipo_documento, fecha_nacimiento, discapacidad, estado_nivelacion "
                "FROM Estudiante WHERE id_usuario = ?",
                (uid,),
            )
            if estudiante:
                usuario = Estudiante(
                    uid,
                    fila.cedula,
                    fila.nombres,
                    fila.apellidos,
                    fila.correo,
                    fila.contrasena,
                    fila.telefono or "",
                    estudiante.tipo_documento or "Cedula",
                    _a_texto(estudiante.fecha_nacimiento),
                    _a_bool(estudiante.discapacidad),
                )
                usuario.estado = estado
                usuario.estado_nivelacion = estudiante.estado_nivelacion or "Pendiente"
                sistema.usuarios[uid] = usuario

    def _cargar_aulas(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT id_aula, codigo, nombre, capacidad, piso, edificio, estado FROM Aula"
        )
        for fila in filas:
            aula = Aula(
                fila.id_aula,
                fila.codigo,
                fila.nombre,
                int(fila.capacidad or 0),
                int(fila.piso or 0),
                fila.edificio or "",
                _a_bool(fila.estado),
            )
            sistema.aulas[aula.id_aula] = aula

    def _cargar_horarios(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT id_horario, dia, hora_inicio, hora_fin, modalidad, grupo, id_aula FROM Horario"
        )
        for fila in filas:
            aula = sistema.aulas.get(fila.id_aula)
            if not aula:
                continue
            horario = Horario(
                fila.id_horario,
                fila.dia,
                _a_texto(fila.hora_inicio),
                _a_texto(fila.hora_fin),
                fila.modalidad or "",
                fila.grupo or "",
                aula,
            )
            sistema.horarios[horario.id_horario] = horario

    def _cargar_cursos(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT id_curso, codigo, nombre, nivel, paralelo, cupo_maximo, cupo_actual, estado, "
            "id_docente, id_horario, id_aula FROM CursoNivelacion"
        )
        for fila in filas:
            docente = sistema.usuarios.get(fila.id_docente)
            horario = sistema.horarios.get(fila.id_horario)
            aula = sistema.aulas.get(fila.id_aula)
            if not docente or not horario or not aula:
                continue
            curso = CursoNivelacion(
                fila.id_curso,
                fila.codigo,
                fila.nombre,
                fila.nivel or "",
                fila.paralelo or "",
                int(fila.cupo_maximo or 0),
                docente,
                horario,
                aula,
                _a_bool(fila.estado),
            )
            curso.cupo_actual = int(fila.cupo_actual or 0)
            sistema.cursos[curso.id_curso] = curso

    def _cargar_matriculas(self, sistema):
        for curso in sistema.cursos.values():
            curso.cupo_actual = 0

        filas = self.db.consultar_todos(
            "SELECT m.id_matricula, m.fecha_matricula, m.tipo_matricula, m.id_periodo, "
            "m.id_estudiante, m.id_curso, m.estado, m.observaciones, p.nombre AS periodo_nombre "
            "FROM Matricula m "
            "INNER JOIN PeriodoAcademico p ON p.id_periodo = m.id_periodo"
        )
        for fila in filas:
            estudiante = sistema.usuarios.get(fila.id_estudiante)
            curso = sistema.cursos.get(fila.id_curso)
            if not isinstance(estudiante, Estudiante) or not curso:
                continue

            if estudiante not in curso.lista_estudiantes:
                curso.agregar_estudiante(estudiante)

            matricula = Matricula(
                fila.id_matricula,
                _a_texto(fila.fecha_matricula),
                fila.tipo_matricula or "Regular",
                fila.periodo_nombre,
                fila.estado or "Activa",
            )
            if fila.observaciones:
                matricula.observaciones = fila.observaciones
            estudiante.matricula = matricula
            sistema.matriculas[fila.id_matricula] = matricula

    def _cargar_calificaciones(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT id_calificacion, nota_parcial1, nota_parcial2, estado, "
            "id_estudiante, id_curso, id_docente, periodo FROM Calificacion"
        )
        for fila in filas:
            estudiante = sistema.usuarios.get(fila.id_estudiante)
            curso = sistema.cursos.get(fila.id_curso)
            docente = sistema.usuarios.get(fila.id_docente)
            if not estudiante or not curso or not docente:
                continue
            calificacion = Calificacion(
                fila.id_calificacion,
                float(fila.nota_parcial1 or 0),
                float(fila.nota_parcial2 or 0),
                fila.estado or "Publicada",
            )
            calificacion.calcular_promedio()
            sistema.calificaciones[fila.id_calificacion] = {
                "calificacion": calificacion,
                "estudiante": estudiante,
                "curso": curso,
                "docente": docente,
                "periodo": fila.periodo or sistema.periodo_actual,
            }

    def _cargar_asistencias(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT id_asistencia, fecha, estado, observacion, "
            "id_estudiante, id_curso, id_docente, periodo FROM Asistencia"
        )
        for fila in filas:
            estudiante = sistema.usuarios.get(fila.id_estudiante)
            curso = sistema.cursos.get(fila.id_curso)
            docente = sistema.usuarios.get(fila.id_docente)
            if not estudiante or not curso or not docente:
                continue
            asistencia = Asistencia(
                fila.id_asistencia,
                _a_texto(fila.fecha),
                fila.estado or "Presente",
                fila.observacion or "",
            )
            sistema.asistencias[fila.id_asistencia] = {
                "asistencia": asistencia,
                "estudiante": estudiante,
                "curso": curso,
                "docente": docente,
                "periodo": fila.periodo or sistema.periodo_actual,
            }

    def _cargar_cargas(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT c.id_carga, c.id_estudiante, c.total_asignaturas, c.total_creditos, "
            "c.estado, p.nombre AS periodo_nombre "
            "FROM CargaAcademica c "
            "INNER JOIN PeriodoAcademico p ON p.id_periodo = c.id_periodo"
        )
        for fila in filas:
            estudiante = sistema.usuarios.get(fila.id_estudiante)
            if not isinstance(estudiante, Estudiante):
                continue
            carga = CargaAcademica(
                fila.id_carga,
                estudiante,
                fila.periodo_nombre,
                int(fila.total_asignaturas or 0),
                int(fila.total_creditos or 0),
                _a_bool(fila.estado),
            )
            sistema.cargas_academicas[fila.id_carga] = carga

    def _cargar_reportes(self, sistema):
        filas = self.db.consultar_todos(
            "SELECT r.id_reporte, r.tipo_reporte, r.fecha_generacion, r.descripcion, "
            "r.formato, p.nombre AS periodo_nombre "
            "FROM Reporte r "
            "INNER JOIN PeriodoAcademico p ON p.id_periodo = r.id_periodo"
        )
        for fila in filas:
            exportador = ExportarExcel() if (fila.formato or "").upper() == "EXCEL" else ExportarPDF()
            reporte = Reporte(
                fila.id_reporte,
                fila.tipo_reporte,
                _a_texto(fila.fecha_generacion),
                fila.periodo_nombre,
                fila.descripcion or "",
                exportador,
            )
            sistema.reportes[fila.id_reporte] = reporte

    def _sincronizar_periodo_actual(self, sistema):
        abiertos = [p for p in sistema.periodos.values() if p.estado == "Abierto"]
        if abiertos:
            sistema.periodo_actual = abiertos[0].nombre
        elif sistema.periodos:
            sistema.periodo_actual = next(iter(sistema.periodos.values())).nombre
        sistema.periodos_disponibles = [p.nombre for p in sistema.periodos.values()]

    def _obtener_id_periodo(self, sistema, nombre_periodo):
        periodo = sistema.obtener_periodo(nombre_periodo)
        return periodo.id_periodo if periodo else None

    def _conectar_escritura(self):
        return self.db.conectar()

    def guardar_periodo(self, periodo):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "INSERT INTO PeriodoAcademico (id_periodo, nombre, fecha_inicio, fecha_fin, estado) "
                "VALUES (?, ?, ?, ?, ?)",
                (periodo.id_periodo, periodo.nombre, periodo.fecha_inicio, periodo.fecha_fin, periodo.estado),
            )
        finally:
            self.db.cerrar()

    def actualizar_periodo(self, periodo):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "UPDATE PeriodoAcademico SET estado = ? WHERE id_periodo = ?",
                (periodo.estado, periodo.id_periodo),
            )
        finally:
            self.db.cerrar()

    def guardar_usuario(self, usuario, tipo_usuario, datos_extra=None):
        if not self._conectar_escritura():
            return
        datos_extra = datos_extra or {}
        try:
            self.db.ejecutar(
                "INSERT INTO Usuario (id_usuario, cedula, nombres, apellidos, correo, contrasena, telefono, estado) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    usuario.id_usuario,
                    usuario.cedula,
                    usuario.nombres,
                    usuario.apellidos,
                    usuario.correo,
                    usuario.contraseña,
                    usuario.telefono,
                    1 if usuario.estado else 0,
                ),
            )
            if tipo_usuario == "Docente" and isinstance(usuario, Docente):
                self.db.ejecutar(
                    "INSERT INTO Docente (id_usuario, titulo_profesional, especialidad) VALUES (?, ?, ?)",
                    (usuario.id_usuario, usuario.titulo_profesional, usuario.especialidad),
                )
            elif tipo_usuario == "Estudiante" and isinstance(usuario, Estudiante):
                self.db.ejecutar(
                    "INSERT INTO Estudiante (id_usuario, tipo_documento, fecha_nacimiento, discapacidad, estado_nivelacion) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        usuario.id_usuario,
                        usuario.tipo_documento,
                        usuario.fecha_nacimiento or None,
                        1 if usuario.discapacidad else 0,
                        usuario.estado_nivelacion,
                    ),
                )
            elif tipo_usuario == "Administrador" and isinstance(usuario, Administrador):
                self.db.ejecutar(
                    "INSERT INTO Administrador (id_usuario, id_administrador, cargo) VALUES (?, ?, ?)",
                    (usuario.id_usuario, usuario.id_administrador, usuario.cargo),
                )
        finally:
            self.db.cerrar()

    def actualizar_usuario(self, usuario):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "UPDATE Usuario SET correo = ?, telefono = ?, estado = ? WHERE id_usuario = ?",
                (usuario.correo, usuario.telefono, 1 if usuario.estado else 0, usuario.id_usuario),
            )
            if isinstance(usuario, Estudiante):
                self.db.ejecutar(
                    "UPDATE Estudiante SET estado_nivelacion = ? WHERE id_usuario = ?",
                    (usuario.estado_nivelacion, usuario.id_usuario),
                )
        finally:
            self.db.cerrar()

    def guardar_aula(self, aula):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "INSERT INTO Aula (id_aula, codigo, nombre, capacidad, piso, edificio, estado) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    aula.id_aula,
                    aula.codigo,
                    aula.nombre,
                    aula.capacidad,
                    aula.piso,
                    aula.edificio,
                    1 if aula.estado else 0,
                ),
            )
        finally:
            self.db.cerrar()

    def guardar_horario(self, horario):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "INSERT INTO Horario (id_horario, dia, hora_inicio, hora_fin, modalidad, grupo, id_aula) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    horario.id_horario,
                    horario.dia,
                    horario.hora_inicio,
                    horario.hora_fin,
                    horario.modalidad,
                    horario.grupo,
                    horario.aula.id_aula,
                ),
            )
        finally:
            self.db.cerrar()

    def guardar_curso(self, curso):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "INSERT INTO CursoNivelacion (id_curso, codigo, nombre, nivel, paralelo, cupo_maximo, "
                "cupo_actual, estado, id_docente, id_horario, id_aula) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    curso.id_curso,
                    curso.codigo,
                    curso.nombre,
                    curso.nivel,
                    curso.paralelo,
                    curso.cupo_maximo,
                    curso.cupo_actual,
                    1 if curso.estado else 0,
                    curso.docente.id_usuario,
                    curso.horario.id_horario,
                    curso.aula.id_aula,
                ),
            )
        finally:
            self.db.cerrar()

    def actualizar_curso(self, curso):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "UPDATE CursoNivelacion SET cupo_actual = ?, estado = ? WHERE id_curso = ?",
                (curso.cupo_actual, 1 if curso.estado else 0, curso.id_curso),
            )
        finally:
            self.db.cerrar()

    def guardar_matricula(self, sistema, matricula, estudiante, curso, periodo_obj):
        if not self._conectar_escritura():
            return
        try:
            self.db.ejecutar(
                "INSERT INTO Matricula (id_matricula, fecha_matricula, tipo_matricula, id_periodo, "
                "id_estudiante, id_curso, estado, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    matricula.id_matricula,
                    matricula.fecha_matricula,
                    matricula.tipo_matricula,
                    periodo_obj.id_periodo,
                    estudiante.id_usuario,
                    curso.id_curso,
                    matricula.estado,
                    matricula.observaciones or "",
                ),
            )
            self.db.ejecutar(
                "UPDATE CursoNivelacion SET cupo_actual = ? WHERE id_curso = ?",
                (curso.cupo_actual, curso.id_curso),
            )
            if isinstance(estudiante, Estudiante):
                self.db.ejecutar(
                    "UPDATE Estudiante SET estado_nivelacion = ? WHERE id_usuario = ?",
                    (estudiante.estado_nivelacion, estudiante.id_usuario),
                )
        finally:
            self.db.cerrar()

    def guardar_calificacion(self, registro):
        if not self._conectar_escritura():
            return
        cal = registro["calificacion"]
        try:
            self.db.ejecutar(
                "INSERT INTO Calificacion (id_calificacion, nota_parcial1, nota_parcial2, estado, "
                "id_estudiante, id_curso, id_docente, periodo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    cal.id_calificacion,
                    cal.nota_parcial1,
                    cal.nota_parcial2,
                    cal.estado,
                    registro["estudiante"].id_usuario,
                    registro["curso"].id_curso,
                    registro["docente"].id_usuario,
                    registro["periodo"],
                ),
            )
        finally:
            self.db.cerrar()

    def guardar_asistencia(self, registro):
        if not self._conectar_escritura():
            return
        asist = registro["asistencia"]
        try:
            self.db.ejecutar(
                "INSERT INTO Asistencia (id_asistencia, fecha, estado, observacion, "
                "id_estudiante, id_curso, id_docente, periodo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    asist.id_asistencia,
                    asist.fecha,
                    asist.estado,
                    asist.observacion or "",
                    registro["estudiante"].id_usuario,
                    registro["curso"].id_curso,
                    registro["docente"].id_usuario,
                    registro["periodo"],
                ),
            )
        finally:
            self.db.cerrar()

    def guardar_carga(self, sistema, carga):
        if not self._conectar_escritura():
            return
        id_periodo = self._obtener_id_periodo(sistema, carga.periodo)
        if not id_periodo:
            return
        try:
            self.db.ejecutar(
                "INSERT INTO CargaAcademica (id_carga, id_estudiante, id_periodo, total_asignaturas, total_creditos, estado) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    carga.id_carga,
                    carga.estudiante.id_usuario,
                    id_periodo,
                    carga.total_asignaturas,
                    carga.total_creditos,
                    1 if carga.estado else 0,
                ),
            )
        finally:
            self.db.cerrar()

    def guardar_reporte(self, sistema, reporte):
        if not self._conectar_escritura():
            return
        id_periodo = self._obtener_id_periodo(sistema, reporte.periodo)
        if not id_periodo:
            return
        try:
            self.db.ejecutar(
                "INSERT INTO Reporte (id_reporte, tipo_reporte, fecha_generacion, id_periodo, descripcion, formato) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    reporte.id_reporte,
                    reporte.tipo_reporte,
                    reporte.fecha_generacion,
                    id_periodo,
                    reporte.descripcion,
                    reporte.formato,
                ),
            )
        finally:
            self.db.cerrar()

    def siguiente_id(self, tabla, columna):
        if not self._conectar_escritura():
            return None
        try:
            return self.db.siguiente_id(tabla, columna)
        finally:
            self.db.cerrar()
