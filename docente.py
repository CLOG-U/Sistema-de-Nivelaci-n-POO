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
#se registra las notas de un estudiante usando kwargs
    def registrar_notas(self, id_calificacion, id_estudiante, parcial1, parcial2, **kwargs):
        #se valida que las notas estén entre 0 y 10
        if parcial1 < 0 or parcial1 > 10 or parcial2 < 0 or parcial2 > 10:
            print("Las notas deben estar entre 0 y 10")
            return
        nota_final = round((parcial1 + parcial2) / 2, 2)
    #se crea un diccionario con la información de la calificación
        nota = {
            "id_calificacion": id_calificacion,
            "id_estudiante": id_estudiante,
            "parcial1": parcial1,
            "parcial2": parcial2,
            "nota_final": nota_final
        }
        if "observacion" in kwargs:
            nota["observacion"] = kwargs["observacion"]
        if "fecha" in kwargs:
            nota["fecha"] = kwargs["fecha"]
        self.__notas_registradas.append(nota)
        print("Nota registrada para el estudiante " + str(id_estudiante) + " nota final: " + str(nota_final))
#sobrecarga simulada con args
    def registrar_asistencia(self, fecha, estado, *args):
        for id_estudiante in args: #recorre cada estudiante enviado en args
            print("Asistencia registrada para el estudiante " + str(id_estudiante) + " el " + fecha + " estado: " + estado)

    def consultar_estudiantes(self, curso):
        return curso.lista_estudiantes
#sobrecarga simulada con kwargs
    def generar_reporte(self, **kwargs):
        print("Reporte del docente: " + self.nombres + " " + self.apellidos)
        print("Titulo: " + self.__titulo_profesional)
        print("Especialidad: " + self.__especialidad)
        if "periodo" in kwargs:
            print("Periodo: " + kwargs["periodo"])
        if "incluir_notas" in kwargs and kwargs["incluir_notas"] == True:
            print("Notas registradas: " + str(len(self.__notas_registradas)))
        else:
            print("Notas registradas: " + str(len(self.__notas_registradas)))
#método sobreescrito para iniciar sesión  
    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            print("Inicio de sesion como docente correctamente para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False
#sobreescribe el metodo de Usuario, aqui se aplica el poliformismo
    def mostrar_info(self):
        print("Docente: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Titulo profesional: " + self.__titulo_profesional)
        print("Especialidad: " + self.__especialidad)
