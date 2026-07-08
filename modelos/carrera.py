from modelos.facultad import Facultad   # Importa la clase Facultad desde el módulo modelos.facultad

class Carrera:

    def __init__(self, id_carrera, codigo, nombre, estado, facultad):   # Inicializa los atributos de la carrera.
        self.__id_carrera = id_carrera
        self.__codigo = codigo
        self.__nombre = nombre
        self.__estado = estado
        self.__facultad = facultad
 # Métodos Getter (lectura)
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
# Método Setter (modificación)
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

#se muestra la informacion de la carrera
            """
        Muestra  la información principal de la carrera,
        incluyendo su nombre, código y la facultad a la que pertenece.
        """
    def mostrar_info(self):
        print("Carrera: " + self.__nombre + " codigo: " + self.__codigo)
        print("Facultad: " + self.__facultad.nombre)
