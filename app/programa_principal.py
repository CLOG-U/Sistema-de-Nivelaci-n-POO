import sys
from pathlib import Path

# Configurar la ruta del proyecto para poder importar módulos desde cualquier nivel
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from modelos.aula import Aula
from modelos.carga_academica import CargaAcademica
from modelos.curso_nivelacion import CursoNivelacion
from modelos.horario import Horario
from modelos.usuario import Usuario
from servicios.fabrica import FabricaUsuario
from servicios.sistema_nivelacion import SistemaNivelacion
from servicios.matricula_facade import MatriculaFacade
from modelos.periodo_academico import PeriodoAcademico


def main():
    print("Creando usuarios del sistema")
    print("")

    # Usar el patrón Factory para crear diferentes tipos de usuarios
    fabrica = FabricaUsuario()
    docente1 = fabrica.crear_usuario("Docente", 1, "1300001111", "Valentin", "Perez", "perez123@uleam.edu.ec", "doc123", "0991234567", "Magister en Software", "Programacion OO")
    estudiante1 = fabrica.crear_usuario("Estudiante", 2, "1300002222", "Maykel", "Castro", "mcastro@uleam.edu.ec", "est123", "0997654321", "Cedula", "2005-03-15")
    estudiante2 = fabrica.crear_usuario("Estudiante", 3, "1300003333", "Bryan", "Chiquito", "bchiquito@uleam.edu.ec", "est456", "0994567890", "Cedula", "2004-07-22")
    admin1 = fabrica.crear_usuario("Administrador", 4, "1300004444", "Carlos", "Ortiz", "cortiz@uleam.edu.ec", "adm123", "0993456789", 1, "Director de Nivelacion")

    # Demostración de Polimorfismo: el método mostrar_info() se ejecuta de forma diferente
    # según el tipo de usuario (Docente, Estudiante o Administrador)
    print("Polimorfismo - el metodo mostrar_info se comporta diferente en cada clase")
    print("")
    lista_usuarios = [docente1, estudiante1, admin1]
    for usuario in lista_usuarios:
        usuario.mostrar_info()
        print("")

    # Método estático de la clase Usuario para validar formato de correo
    print("Verificar metodo estatico")
    print(Usuario.validar_correo("pablo@uleam.edu.ec"))

    # Método de clase que retorna el total de usuarios creados en el sistema
    print("Metodo de clases")
    print("Total usuarios:", Usuario.total_usuarios())
    print("")

    # Crear curso de nivelación con aula y horario asignados
    print("Creando curso de nivelacion")
    aula1 = Aula(1, "A101", "Aula 101", 35, 1, "Bloque A")
    horario1 = Horario(1, "Lunes", "08:00", "10:00", "Presencial", "A", aula1)
    curso1 = CursoNivelacion(1, "POO-001", "Programacion Orientada a Objetos", "Nivelacion", "A", 30, docente1, horario1, aula1)
    curso1.agregar_estudiante(estudiante1)
    curso1.agregar_estudiante(estudiante2)
    curso1.mostrar_info()
    print("")

    # Generar carga académica para un estudiante en el periodo 2026-1
    print("Generando carga academica")
    carga1 = CargaAcademica(1, estudiante1, "2026-1", 1, 4)
    carga1.generar_carga()
    print("")

    print("Usando el patron facade para matricular estudiantes")
    periodo1 = PeriodoAcademico(1, "2026-1", "2026-01-01", "2026-06-30", "Abierto")
    facade = MatriculaFacade(periodo1, curso1, estudiante1)
    facade.matricular(1, "2026-01-10", "Regular")
    print("")

    # ================================================================
    # Patron Strategy: el cliente (SistemaNivelacion.generar_reporte)
    # decide en tiempo de ejecucion QUE estrategia de exportacion usar
    # (ExportarPDF o ExportarExcel), y Reporte (el contexto) no conoce
    # ni le importa cual fue: solo delega en el objeto que recibio.
    # ================================================================
    print("Patron Strategy - generacion de reportes en distintos formatos")
    print("")

    sistema = SistemaNivelacion()

    formatos_solicitados = ["PDF", "Excel"]
    for formato in formatos_solicitados:
        print(f"--- Cliente solicita reporte en formato: {formato} ---")
        reporte = sistema.generar_reporte(
            "Asistencia", "2026-1", "Reporte general de asistencia", formato
        )
        reporte.generar_reporte()
        reporte.exportar()  # <- mismo metodo, comportamiento distinto segun la estrategia inyectada
        print("")

    print("Reportes generados en el sistema:")
    for reporte in sistema.reportes:
        print(f"Reporte {reporte.id_reporte} | {reporte.tipo_reporte} | {reporte.periodo} | Formato: {reporte.formato}")


if __name__ == "__main__":
    main()

