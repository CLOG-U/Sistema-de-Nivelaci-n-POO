class DetalleCalificacion:

    def __init__(self, id_detalle, tipo_evaluacion, descripcion, puntaje_obtenido, puntaje_total, fecha_evaluacion):  # Inicializa los atributos del detalle de la calificación.
        self.__id_detalle = id_detalle
        self.__tipo_evaluacion = tipo_evaluacion
        self.__descripcion = descripcion
        self.__puntaje_obtenido = puntaje_obtenido
        self.__puntaje_total = puntaje_total
        self.__fecha_evaluacion = fecha_evaluacion
#uso de propiedades para acceder a los atributos privados
    # Métodos Getter (lectura)
    @property
    def tipo_evaluacion(self):
        return self.__tipo_evaluacion

    @property
    def puntaje_obtenido(self):
        return self.__puntaje_obtenido

    @property
    def puntaje_total(self):
        return self.__puntaje_total
#se calcula el porcentaje de la evaluacion con base al puntaje obtenido y el puntaje total
    # Si el puntaje total es 0, retorna 0 para evitar división por cero.
    @property
    def porcentaje(self):
        if self.__puntaje_total == 0:
            return 0
        resultado = (self.__puntaje_obtenido / self.__puntaje_total) * 100
        return round(resultado, 2)
# Método Setter (modificación)
    @puntaje_obtenido.setter
    def puntaje_obtenido(self, valor):
        self.__puntaje_obtenido = valor

    def registrar_detalle(self):
        print("Detalle registrado: " + self.__tipo_evaluacion + " puntaje: " + str(self.__puntaje_obtenido) + "/" + str(self.__puntaje_total))
#editamos el puntaje obtenido en la evaluacion
    def editar_detalle(self, nuevo_puntaje):
                """
        Actualiza el puntaje obtenido en la evaluación.
        """
        self.__puntaje_obtenido = nuevo_puntaje
        print("Puntaje actualizado a " + str(nuevo_puntaje))

    def eliminar_detalle(self):
        print("Detalle eliminado")
#se muetra un resumen del detalle de calificacion 
    def mostrar_info(self):
                """
        Muestra un resumen de la evaluación,
        incluyendo el puntaje obtenido y el porcentaje.
        """
        print("Evaluacion: " + self.__tipo_evaluacion + " " + str(self.__puntaje_obtenido) + "/" + str(self.__puntaje_total) + " porcentaje: " + str(self.porcentaje) + "%")
