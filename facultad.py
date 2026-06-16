class Facultad:

    def __init__(self, id_facultad, nombre):
        self.__id_facultad = id_facultad
        self.__nombre = nombre
#getter
    @property
    def id_facultad(self):
        return self.__id_facultad

    @property
    def nombre(self):
        return self.__nombre
#setter
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    def mostrar_info(self):
        print("Facultad: " + self.__nombre)
