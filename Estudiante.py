from usuario import Usuario
class Estudiante(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, tipo_documento, numero_documento, fecha_nacimiento, discapacidad=False):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__tipo_documento = tipo_documento
        self.__numero_documento = numero_documento
        self.__fecha_nacimiento = fecha_nacimiento
        self.__discapacidad = discapacidad
        self.__estado_nivelacion = "Pendiente"
        self.__matricula = None
#uso de propiedades, getter y setter para acceder a los atributos privados 
    @property
    def tipo_documento(self):
        return self.__tipo_documento

    @property
    def numero_documento(self):
        return self.__numero_documento

    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento

    @property
    def discapacidad(self):
        return self.__discapacidad

    @property
    def estado_nivelacion(self):
        return self.__estado_nivelacion

    @property
    def matricula(self):
        return self.__matricula

    @estado_nivelacion.setter
    def estado_nivelacion(self, valor):
        self.__estado_nivelacion = valor

    @matricula.setter
    def matricula(self, mat):
        self.__matricula = mat
