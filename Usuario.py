from abc import ABC, abstractmethod

class Usuario(ABC):
    contador = 0      #variable de clase que cuenta cuantos usuarios se crean
    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, estado=True):
        self.__id_usuario = id_usuario     #atributos privados
        self.__cedula = cedula
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__correo = correo
        self.__contraseña = contraseña
        self.__telefono = telefono
        self.__estado = estado
        Usuario.contador += 1     #Incrementa el contador de usuarios creados
      @property      #Este docorador permite acceder al atributo privado, como si fuera una variable normal, sin llamar un método
    def id_usuario(self):
        return self.__id_usuario

    @property
    def cedula(self):
        return self.__cedula

    @property
    def nombres(self):
        return self.__nombres

    @property
    def apellidos(self):
        return self.__apellidos

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    @property
    def estado(self):
        return self.__estado

    @property
    def contraseña(self):
        return self.__contraseña
