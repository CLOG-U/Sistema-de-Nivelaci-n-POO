from facultad import Facultad

class Carrera:

    def __init__(self, id_carrera, codigo, nombre, estado, facultad):
        self.__id_carrera = id_carrera
        self.__codigo = codigo
        self.__nombre = nombre
        self.__estado = estado
        self.__facultad = facultad
#getter 
    @property
    def id_carrera(self):
        return self.__id_carrera

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def estado(self):
        return self.__estado

    @property
    def facultad(self):
        return self.__facultad
#setter
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

#se muestra la informacion de la carrera
    def mostrar_info(self):
        print("Carrera: " + self.__nombre + " codigo: " + self.__codigo)
        print("Facultad: " + self.__facultad.nombre)
