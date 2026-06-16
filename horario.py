class Horario:
    def __init__(self, id_horario, dia, hora_inicio, hora_fin, modalidad, grupo, aula):
        self.__id_horario = id_horario
        self.__dia = dia
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.__modalidad = modalidad
        self.__grupo = grupo
        self.__aula = aula

#uso de propiedades para acceder a los atributos privados
    @property
    def id_horario(self):
        return self.__id_horario

    @property
    def dia(self):
        return self.__dia

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @property
    def hora_fin(self):
        return self.__hora_fin

    @property
    def modalidad(self):
        return self.__modalidad

    @property
    def aula(self):
        return self.__aula

    def registrar_horario(self):
        print("Horario registrado: " + self.__dia + " de " + self.__hora_inicio + " a " + self.__hora_fin + " en " + self.__aula.nombre)
#modifica informacion del horario
    def modificar_horario(self, campo, valor):
        print("Horario modificado: " + campo + " cambiado a " + str(valor))

#elimina el horario
    def eliminar_horario(self):
        print("Horario eliminado")

#muestra la informacion del horario
    def mostrar_info(self):
        print("Horario: " + self.__dia + " " + self.__hora_inicio + " a " + self.__hora_fin + " modalidad: " + self.__modalidad)