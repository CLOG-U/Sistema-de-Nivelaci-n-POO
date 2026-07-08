from modelos.detalle_asistencia import DetalleAsistencia

class Asistencia:

    def __init__(self, id_asistencia, fecha, estado="Presente", observacion=""):
        self.__id_asistencia = id_asistencia
        self.__fecha = fecha
        self.__estado = estado
        self.__observacion = observacion
        self.__detalles = []
#uso de propiedades para acceder a los atributos privados
    @property
    def id_asistencia(self):
        return self.__id_asistencia

    @property
    def fecha(self):
        return self.__fecha

    @property
    def estado(self):
        return self.__estado

    @property
    def observacion(self):
        return self.__observacion

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    @observacion.setter
    def observacion(self, valor):
        self.__observacion = valor

#se anota la asistencia del estudiante
    def anotar_asistencia(self, estado, obs=""):
        self.__estado = estado
        self.__observacion = obs
        print("Asistencia anotada el " + self.__fecha + " estado: " + estado)

#se justifica la falta del estudiante verificando si el estado es ausente y se agrega el detalle de la justificacion
    def justificar_falta(self, detalle):
        if self.__estado == "Ausente":
            self.__detalles.append(detalle)
            self.__estado = "Justificado"
            print("Falta justificada con: " + detalle.tipo_justificacion)
        else:
            print("Solo se pueden justificar ausencias")

#se obtiene un resumen de la asistencia
    def obtener_resumen(self):
        resumen = {
            "id": self.__id_asistencia,
            "fecha": self.__fecha,
            "estado": self.__estado,
            "observacion": self.__observacion
        }
        return resumen

#se muestra la informacion de la asistencia 
    def mostrar_info(self):
        print("Asistencia " + str(self.__id_asistencia) + " fecha: " + self.__fecha + " estado: " + self.__estado)
