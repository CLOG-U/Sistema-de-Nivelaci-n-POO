from abc import ABC, abstractmethod

from servicios.exportador_reportes import ArchivoExportado, exportar_reporte


class IExportable(ABC):
    @abstractmethod
    def exportar(self, datos) -> ArchivoExportado:
        pass


class ExportarExcel(IExportable):
    def __init__(self):
        self.ultimo_archivo = None

    def exportar(self, datos) -> ArchivoExportado:
        archivo = exportar_reporte(datos, "Excel")
        self.ultimo_archivo = archivo
        return archivo


class ExportarPDF(IExportable):
    def __init__(self):
        self.ultimo_archivo = None

    def exportar(self, datos) -> ArchivoExportado:
        archivo = exportar_reporte(datos, "PDF")
        self.ultimo_archivo = archivo
        return archivo
