# Cambio 1: Fabrica de usuarios para el sistema de nivelación
# Este archivo es un módulo adicional y no modifica los archivos existentes.
# una clase FabricaUsuario que crea instancias de Estudiante, Docente o Administrador.

from Usuario import Usuario
from Docente import Docente
from Estudiante import Estudiante
from Administrador import Administrador


class FabricaUsuario:
    """Fábrica para crear usuarios del sistema según su tipo."""

    def crear_usuario(self, tipo_usuario, *args, **kwargs):
        if tipo_usuario == "Estudiante":
            return Estudiante(*args, **kwargs)
        elif tipo_usuario == "Docente":
            return Docente(*args, **kwargs)
        elif tipo_usuario == "Administrador" or tipo_usuario == "Admin":
            return Administrador(*args, **kwargs)
        else:
            raise ValueError(f"Tipo de usuario no válido: {tipo_usuario}")


# fabrica = FabricaUsuario()
# estudiante = fabrica.crear_usuario(
#     "Estudiante",
#     2,
#     "1300002222",
#     "Maykel",
#     "Castro",
#     "mcastro@uleam.edu.ec",
#     "est123",
#     "0997654321",
#     "Cedula",
#     "1300002222",
#     "2005-03-15"
# )
#
# docente = fabrica.crear_usuario(
#     "Docente",
#     1,
#     "1300001111",
#     "Valentin",
#     "Perez",
#     "perez123@uleam.edu.ec",
#     "doc123",
#     "0991234567",
#     "Magister en Software",
#     "Programacion OO"
# )
#
# admin = fabrica.crear_usuario(
#     "Administrador",
#     4,
#     "1300004444",
#     "Carlos",
#     "Ortiz",
#     "cortiz@uleam.edu.ec",
#     "adm123",
#     "0993456789",
#     1,
#     "Director de Nivelacion"
# )
#
# for usuario in [estudiante, docente, admin]:
#     usuario.mostrar_info()
