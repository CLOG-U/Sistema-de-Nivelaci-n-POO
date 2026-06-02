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
    #Setter  
#Nos permite modificar los atributos privado aplicando validaciones
    @nombres.setter
    def nombres(self, valor):
        if valor == "":             #Valida que el nombre no este vacío
            print("El nombre no puede estar vacio")
        else:
            self.__nombres = valor

    @apellidos.setter
    def apellidos(self, valor):
        if valor == "":    #valida que los apellidos no esten vacios.
            print("Los apellidos no pueden estar vacios")
        else:
            self.__apellidos = valor

#método estatico.
# Valida si el correo contiene '@' y '.' además no utiliza atributos del objeto.
    @staticmethod
    def validar_correo(correo):
     return "@" in correo and "." in correo
    
    @correo.setter
    def correo(self, valor):
     if not Usuario.validar_correo(valor):
         print("El correo no es valido")
     else:
         self.__correo = valor

    @telefono.setter
    def telefono(self, valor):
        if len(valor) < 9: #valida que el telefono tenga los digitos correctos
            print("El telefono debe tener al menos 9 digitos")
        else:
            self.__telefono = valor

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    @contraseña.setter
    def contraseña(self, valor):
        self.__contraseña = valor
