class Aula:

    def __init__(self, id_aula, codigo, nombre, capacidad, piso, edificio, estado=True):
        self.__id_aula = id_aula
        self.__codigo = codigo
        self.__nombre = nombre
        self.__capacidad = capacidad
        self.__piso = piso
        self.__edificio = edificio
        self.__estado = estado 

#uso de propiedades para acceder a los atributos privados
    @property
    def id_aula(self):
        return self.__id_aula

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def capacidad(self):
        return self.__capacidad

    @property
    def edificio(self):
        return self.__edificio

    @property
    def estado(self):
        return self.__estado

    def registrar_aula(self):
        print("Aula registrada: " + self.__nombre + " edificio " + self.__edificio + " piso " + str(self.__piso))

#modifica informacion del aula 
    def modificar_aula(self, campo, valor):
        print("Aula modificada: " + campo + " cambiado a " + str(valor))

#muestra la informacion del aula
    def mostrar_info(self):
        print("Aula: " + self.__nombre + " capacidad: " + str(self.__capacidad))
