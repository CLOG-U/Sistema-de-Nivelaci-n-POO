from usuario import Usuario
class Docente(Usuario):                           #se inicializan los atributos heredados y propios
    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, titulo_profesional, especialidad):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono) 
        self.__titulo_profesional = titulo_profesional
        self.__especialidad = especialidad
        self.__notas_registradas = []
#setter
    @property
    def titulo_profesional(self):
        return self.__titulo_profesional

    @property
    def especialidad(self):
        return self.__especialidad

    @titulo_profesional.setter
    def titulo_profesional(self, valor):
        self.__titulo_profesional = valor

    @especialidad.setter
    def especialidad(self, valor):
        self.__especialidad = valor
      
