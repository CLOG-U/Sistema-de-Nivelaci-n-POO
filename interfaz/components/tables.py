from modelos.admin import Administrador
from modelos.docente import Docente
from modelos.estudiante import Estudiante


def usuario_to_dict(usuario):
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

