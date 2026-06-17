import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from modelos.aula import Aula
from modelos.carga_academica import CargaAcademica
from modelos.curso_nivelacion import CursoNivelacion
from modelos.horario import Horario
from modelos.iexportable import ExportarExcel, ExportarPDF
from modelos.reporte import Reporte
from modelos.usuario import Usuario
from servicios.fabrica import FabricaUsuario


def main():
    print("Creando usuarios del sistema")
    print("")

    fabrica = FabricaUsuario()
    docente1 = fabrica.crear_usuario("Docente", 1, "1300001111", "Valentin", "Perez", "perez123@uleam.edu.ec", "doc123", "0991234567", "Magister en Software", "Programacion OO")
    estudiante1 = fabrica.crear_usuario("Estudiante", 2, "1300002222", "Maykel", "Castro", "mcastro@uleam.edu.ec", "est123", "0997654321", "Cedula", "2005-03-15")
    estudiante2 = fabrica.crear_usuario("Estudiante", 3, "1300003333", "Bryan", "Chiquito", "bchiquito@uleam.edu.ec", "est456", "0994567890", "Cedula", "2004-07-22")
    admin1 = fabrica.crear_usuario("Administrador", 4, "1300004444", "Carlos", "Ortiz", "cortiz@uleam.edu.ec", "adm123", "0993456789", 1, "Director de Nivelacion")

    print("Polimorfismo - el metodo mostrar_info se comporta diferente en cada clase")
    print("")
    lista_usuarios = [docente1, estudiante1, admin1]
    for usuario in lista_usuarios:
        usuario.mostrar_info()
        print("")

    print("Verificar metodo estatico")
    print(Usuario.validar_correo("pablo@uleam.edu.ec"))

    print("Metodo de clases")
    print("Total usuarios:", Usuario.total_usuarios())
    print("")

    print("Creando curso de nivelacion")
    aula1 = Aula(1, "A101", "Aula 101", 35, 1, "Bloque A")
    horario1 = Horario(1, "Lunes", "08:00", "10:00", "Presencial", "A", aula1)
    curso1 = CursoNivelacion(1, "POO-001", "Programacion Orientada a Objetos", "Nivelacion", "A", 30, docente1, horario1, aula1)
    curso1.agregar_estudiante(estudiante1)
    curso1.agregar_estudiante(estudiante2)
    curso1.mostrar_info()
    print("")

    print("Generando carga academica")
    carga1 = CargaAcademica(1, estudiante1, "2026-1", 5, 20)
    carga1.generar_carga()
    print("")

    print("Polimorfismo con interfaces")
    reporte_excel = ExportarExcel()
    reporte_pdf = ExportarPDF()

    exportadores = [reporte_excel, reporte_pdf]
    for exportador in exportadores:
        exportador.exportar("Reporte de asistencia")
    print("")

    print("Generando reporte")
    reporte1 = Reporte(1, "Asistencia", "2026-06-16", "2026-1", "Reporte general de asistencia", reporte_pdf)
    reporte1.generar_reporte()
    reporte1.exportar()


if __name__ == "__main__":
    main()
