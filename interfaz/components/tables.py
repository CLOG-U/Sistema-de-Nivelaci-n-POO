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
