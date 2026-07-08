from modelos.usuario import Usuario


class Docente(Usuario):
    """
    Clase que representa a un docente en el sistema.
    Hereda de Usuario y gestiona notas, asistencia y reportes.
    """
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
    def registrar_notas(self, id_calificacion, id_estudiante, parcial1, parcial2, **kwargs):
        """
        Registra notas de un estudiante.
        Args:
            parcial1, parcial2: Notas entre 0-10
            **kwargs: observacion, fecha (opcionales)
        """
        #se valida que las notas estén entre 0 y 10
        if parcial1 < 0 or parcial1 > 10 or parcial2 < 0 or parcial2 > 10:
            print("Las notas deben estar entre 0 y 10")
            return
            # Calcular nota final
        nota_final = round((parcial1 + parcial2) / 2, 2)
    #se crea un diccionario con la información de la calificación
        nota = {
            "id_calificacion": id_calificacion,
            "id_estudiante": id_estudiante,
            "parcial1": parcial1,
            "parcial2": parcial2,
            "nota_final": nota_final
        }
        # Agregar campos opcionales
        if "observacion" in kwargs:
            nota["observacion"] = kwargs["observacion"]
        if "fecha" in kwargs:
            nota["fecha"] = kwargs["fecha"]
        self.__notas_registradas.append(nota)
        print("Nota registrada para el estudiante " + str(id_estudiante) + " nota final: " + str(nota_final))

    def registrar_asistencia(self, fecha, estado, *args):
        """
        Registra asistencia de multiples estudiantes.
        """
        for id_estudiante in args: #recorre cada estudiante enviado en args
            print("Asistencia registrada para el estudiante " + str(id_estudiante) + " el " + fecha + " estado: " + estado)

    def consultar_estudiantes(self, curso):
        return curso.lista_estudiantes       #Retorna la lista de estudiantes de un curso.
#sobrecarga simulada con kwargs
    def generar_reporte(self, **kwargs):     #Genera reporte del docente.
        print("Reporte del docente: " + self.nombres + " " + self.apellidos)
        print("Titulo: " + self.__titulo_profesional)
        print("Especialidad: " + self.__especialidad)
        if "periodo" in kwargs:
            print("Periodo: " + kwargs["periodo"])
            # Mostrar detalle de notas si se solicita
        if "incluir_notas" in kwargs and kwargs["incluir_notas"] == True:
            print("Notas registradas: " + str(len(self.__notas_registradas)))
        else:
            print("Notas registradas: " + str(len(self.__notas_registradas)))
#Sobrescribe método de Usuario para inicio de sesión.
    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            print("Inicio de sesion como docente correctamente para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False

    def mostrar_info(self):
        """Sobrescribe metodo de Usuario (polimorfismo)."""
        print("Docente: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Titulo profesional: " + self.__titulo_profesional)
        print("Especialidad: " + self.__especialidad)
