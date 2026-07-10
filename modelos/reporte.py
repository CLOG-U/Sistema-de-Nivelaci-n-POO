from modelos.iexportable import IExportable


# Patrón Strategy aplicado al módulo de Reportes
#   - Estrategia (interfaz común) ......... IExportable
#   - Estrategias concretas ............... ExportarPDF, ExportarExcel
#         (definidas en modelos/iexportable.py)
#   - Contexto ............................ Reporte (esta clase)
#   - Cliente .............................. SistemaNivelacion.generar_reporte

class Reporte:
                                                                                        #inyección de dependencia exportador:IExportable
    def __init__(self, id_reporte, tipo_reporte, fecha_generacion, periodo, descripcion, exportador: IExportable):
        self.__id_reporte = id_reporte
        self.__tipo_reporte = tipo_reporte
        self.__fecha_generacion = fecha_generacion
        self.__periodo = periodo
        self.__descripcion = descripcion
        self.__exportador = exportador
        self.__formato = exportador.__class__.__name__.replace("Exportar", "")
#uso de propiedades para acceder a los atributos privados
    # Métodos Getter (lectura)
    @property
    def id_reporte(self):
        return self.__id_reporte

    @property
    def tipo_reporte(self):
        return self.__tipo_reporte

    @property
    def periodo(self):
        return self.__periodo

    @property
    def fecha_generacion(self):
        return self.__fecha_generacion

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def formato(self):
        return self.__formato

#generamos un reporte con la informacion dada
    def generar_reporte(self):
        print("Reporte: " + self.__tipo_reporte)
        print("Descripcion: " + self.__descripcion)
        print("Periodo: " + self.__periodo)
        print("Fecha de generacion: " + self.__fecha_generacion)
#delegamos la exportacion al objeto estrategia (IExportable) recibido por inyeccion de dependencias
    def exportar(self, filas=None):
        datos = {
            "tipo": self.__tipo_reporte,
            "periodo": self.__periodo,
            "descripcion": self.__descripcion,
            "fecha": self.__fecha_generacion,
            "filas": filas or [],
        }
        return self.__exportador.exportar(datos)
