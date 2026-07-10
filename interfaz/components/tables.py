from modelos.admin import Administrador
from modelos.docente import Docente
from modelos.estudiante import Estudiante


def usuario_to_dict(usuario):
    # Convierte un objeto usuario a diccionario con información formateada
    if isinstance(usuario, Estudiante):
        tipo = "Estudiante"
    elif isinstance(usuario, Docente):
        tipo = "Docente"
    elif isinstance(usuario, Administrador):
        tipo = "Administrador"
    else:
        tipo = "Usuario"

    return {
        "ID": usuario.id_usuario,
        "Cedula": usuario.cedula,
        "Nombres": usuario.nombres,
        "Apellidos": usuario.apellidos,
        "Correo": usuario.correo,
        "Telefono": usuario.telefono,
        "Tipo": tipo,
        "Estado": "Activo" if usuario.estado else "Inactivo",
    }


def aula_to_dict(aula):
    # Convierte un aula a diccionario con detalles de ubicación y estado
    return {
        "ID": aula.id_aula,
        "Codigo": aula.codigo,
        "Nombre": aula.nombre,
        "Capacidad": aula.capacidad,
        "Piso": aula.piso,
        "Edificio": aula.edificio,
        "Estado": "Disponible" if aula.estado else "No disponible",
    }


def horario_to_dict(horario):
    # Convierte un horario a diccionario con información del aula asociada
    aula = horario.aula
    aula_texto = f"{aula.codigo} - {aula.nombre}" if aula else "Sin aula"
    return {
        "ID": horario.id_horario,
        "Dia": horario.dia,
        "Hora inicio": horario.hora_inicio,
        "Hora fin": horario.hora_fin,
        "Modalidad": horario.modalidad,
        "Grupo": horario.grupo,
        "Aula": aula_texto,
    }


def curso_to_dict(curso):
    # Convierte un curso a diccionario con docente, aula y horario formateados
    docente = curso.docente
    docente_texto = f"{docente.nombres} {docente.apellidos}" if docente else "Sin docente"
    aula = curso.aula
    aula_texto = f"{aula.codigo} - {aula.nombre}" if aula else "Sin aula"
    horario = curso.horario
    horario_texto = f"{horario.dia} {horario.hora_inicio}-{horario.hora_fin}" if horario else "Sin horario"
    return {
        "ID": curso.id_curso,
        "Codigo": curso.codigo,
        "Nombre": curso.nombre,
        "Nivel": curso.nivel,
        "Paralelo": curso.paralelo,
        "Cupo": f"{curso.cupo_actual}/{curso.cupo_maximo}",
        "Docente": docente_texto,
        "Aula": aula_texto,
        "Horario": horario_texto,
        "Estado": "Abierto" if curso.estado else "Cerrado",
    }


def carga_to_dict(carga):
    # Convierte una carga académica a diccionario con información del estudiante
    estudiante = carga.estudiante
    return {
        "ID": carga.id_carga,
        "Estudiante": f"{estudiante.nombres} {estudiante.apellidos}",
        "Periodo": carga.periodo,
        "Total asignaturas": carga.total_asignaturas,
        "Total creditos": carga.total_creditos,
        "Estado": "Activa" if carga.estado else "Inactiva",
    }


def reporte_to_dict(reporte):
    # Convierte un reporte a diccionario con tipo, fecha y formato
    return {
        "ID": reporte.id_reporte,
        "Tipo": reporte.tipo_reporte,
        "Fecha": reporte.fecha_generacion,
        "Periodo": reporte.periodo,
        "Descripcion": reporte.descripcion,
        "Formato": reporte.formato,
    }


def matricula_to_dict(matricula):
    # Convierte una matrícula a diccionario, maneja casos vacíos
    if not matricula:
        return {
            "ID matricula": "-",
            "Periodo": "-",
            "Tipo": "-",
            "Fecha": "-",
            "Estado": "-",
        }
    return {
        "ID matricula": matricula.id_matricula,
        "Periodo": matricula.periodo,
        "Tipo": matricula.tipo_matricula,
        "Fecha": matricula.fecha_matricula,
        "Estado": matricula.estado,
    }


def periodo_to_dict(periodo):
    # Convierte un período académico a diccionario con fechas
    return {
        "ID": periodo.id_periodo,
        "Nombre": periodo.nombre,
        "Inicio": periodo.fecha_inicio,
        "Fin": periodo.fecha_fin,
        "Estado": periodo.estado,
    }


def calificacion_registro_to_dict(registro):
    # Convierte registro de calificación a diccionario con notas y estado
    calificacion = registro["calificacion"]
    estudiante = registro["estudiante"]
    curso = registro["curso"]
    return {
        "ID": calificacion.id_calificacion,
        "Estudiante": f"{estudiante.nombres} {estudiante.apellidos}",
        "Curso": curso.codigo,
        "Parcial 1": calificacion.nota_parcial1,
        "Parcial 2": calificacion.nota_parcial2,
        "Nota final": calificacion.nota_final,
        "Estado": calificacion.estado,
        "Periodo": registro["periodo"],
    }


def asistencia_registro_to_dict(registro):
    # Convierte registro de asistencia a diccionario con fecha y observación
    asistencia = registro["asistencia"]
    estudiante = registro["estudiante"]
    curso = registro["curso"]
    return {
        "ID": asistencia.id_asistencia,
        "Estudiante": f"{estudiante.nombres} {estudiante.apellidos}",
        "Curso": curso.codigo,
        "Fecha": asistencia.fecha,
        "Estado": asistencia.estado,
        "Observacion": asistencia.observacion or "-",
        "Periodo": registro["periodo"],
    }


def usuario_detalle_campos(usuario):
    # Genera campos de detalle de usuario según su tipo (estudiante, docente, admin)
    campos = [
        ("ID", usuario.id_usuario),
        ("Cedula", usuario.cedula),
        ("Nombres", usuario.nombres),
        ("Apellidos", usuario.apellidos),
        ("Correo", usuario.correo),
        ("Telefono", usuario.telefono),
        ("Estado", "Activo" if usuario.estado else "Inactivo"),
    ]

    if isinstance(usuario, Estudiante):
        campos.extend(
            [
                ("Tipo documento", usuario.tipo_documento),
                ("Fecha nacimiento", usuario.fecha_nacimiento),
                ("Discapacidad", "Si" if usuario.discapacidad else "No"),
                ("Estado nivelacion", usuario.estado_nivelacion),
            ]
        )
    elif isinstance(usuario, Docente):
        campos.extend(
            [
                ("Titulo profesional", usuario.titulo_profesional),
                ("Especialidad", usuario.especialidad),
            ]
        )
    elif isinstance(usuario, Administrador):
        campos.extend(
            [
                ("ID administrador", usuario.id_administrador),
                ("Cargo", usuario.cargo),
            ]
        )

    return campos


def aula_con_uso_dict(aula, cursos_asignados):
    # Augmenta datos de aula con cantidad de cursos asignados
    datos = aula_to_dict(aula)
    datos["Cursos asignados"] = cursos_asignados
    return datos


def curso_detalle_dict(curso):
    # Augmenta datos de curso con inscritos y cupo disponible
    datos = curso_to_dict(curso)
    datos["Inscritos"] = len(curso.lista_estudiantes)
    datos["Cupo disponible"] = curso.cupo_maximo - curso.cupo_actual
    return datos
