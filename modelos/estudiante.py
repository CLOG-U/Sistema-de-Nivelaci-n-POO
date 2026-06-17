from modelos.usuario import Usuario
class Estudiante(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, tipo_documento, fecha_nacimiento, discapacidad=False):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__tipo_documento = tipo_documento
        self.__fecha_nacimiento = fecha_nacimiento
        self.__discapacidad = discapacidad
        self.__estado_nivelacion = "Pendiente"
        self.__matricula = None
#uso de propiedades, getter y setter para acceder a los atributos privados 
    @property
    def tipo_documento(self):
        return self.__tipo_documento

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

#consulta las calificaciones del estudiante
    def consultar_calificaciones(self, calificacion):
        return calificacion.obtener_resumen()
#consulta asistencia 
    def consultar_asistencia(self, asistencia):
        return asistencia.obtener_resumen()

    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            print("Inicio de sesion como estudiante correctamente para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False

#metodo sobreescrito para mostrar informacion del estudiante
    def mostrar_info(self):
        print("Estudiante: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Documento: " + self.__tipo_documento + " " + self.cedula)
        print("Fecha de nacimiento: " + self.__fecha_nacimiento)
        print("Estado nivelacion: " + self.__estado_nivelacion)
        if self.__discapacidad:
            print("Discapacidad: Si")
        else:
            print("Discapacidad: No")

