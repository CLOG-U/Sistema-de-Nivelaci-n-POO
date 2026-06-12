class Usuario:
    contador = 0
    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, estado=True):
        self.__id_usuario = id_usuario
        self.__cedula = cedula
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__correo = correo
        self.__contraseña = contraseña
        self.__telefono = telefono
        self.__estado = estado
        Usuario.contador += 1
#getter nos permite acceder a los atributos privados de manera controlada
    @property
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
    
    

#setter nos va a permitir modificar los atributos privado aplicando validaciones
    @nombres.setter
    def nombres(self, valor):
        if valor == "":
            print("El nombre no puede estar vacio")
        else:
            self.__nombres = valor

    @apellidos.setter
    def apellidos(self, valor):
        if valor == "":
            print("Los apellidos no pueden estar vacios")
        else:
            self.__apellidos = valor

#metodo estatico para validar que el correo contenga @ 
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
        if len(valor) < 9:
            print("El telefono debe tener al menos 9 digitos")
        else:
            self.__telefono = valor

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    @contraseña.setter
    def contraseña(self, valor):
        self.__contraseña = valor

#metodo de clase para ver el total de usuarios
    @classmethod
    def total_usuarios(cls):
     return cls.contador

    def iniciar_sesion(self, contraseña):
        if self.__contraseña == contraseña and self.__estado == True:
            print("Sesion iniciada correctamente para " + self.__nombres + " " + self.__apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False

    def cerrar_sesion(self):
        print("Sesion cerrada para " + self.__nombres + " " + self.__apellidos)
# kwargs nos permite simular sobrecarga
    def actualizar_perfil(self, **kwargs):
        if "nombres" in kwargs:
            self.nombres = kwargs["nombres"]
        if "correo" in kwargs:
            self.correo = kwargs["correo"]
        if "telefono" in kwargs:
            self.telefono = kwargs["telefono"]
        print("Perfil actualizado con los campos: " + str(list(kwargs.keys())))

    # Este metodo se sobreescribe en cada subclase para aplicar polimorfismo

    def mostrar_info(self):
        print("Metodo mostrar_info no implementado")


#Hereda de usuario 
class Docente(Usuario):
#se inicializan los atributos heredados y propios
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
        if parcial1 < 0 or parcial1 > 10 or parcial2 < 0 or parcial2 > 10:
            print("Las notas deben estar entre 0 y 10")
            return
        nota_final = round((parcial1 + parcial2) / 2, 2)
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


    def registrar_asistencia(self, fecha, estado, *args):
        for id_estudiante in args: #recorre cada estudiante enviado en args
            print("Asistencia registrada para el estudiante " + str(id_estudiante) + " el " + fecha + " estado: " + estado)

    def consultar_estudiantes(self, curso):
        return curso.lista_estudiantes


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
#sobreescribe el metodo de Usuario, aqui se aplica el poliformismo
    def mostrar_info(self):
        print("Docente: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Titulo: " + self.__titulo_profesional)
        print("Especialidad: " + self.__especialidad)
        print("Correo: " + self.correo)


#clase estudiante esta hereda de usuario tambien 
class Estudiante(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, tipo_documento, numero_documento, fecha_nacimiento, discapacidad=False):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__tipo_documento = tipo_documento
        self.__numero_documento = numero_documento
        self.__fecha_nacimiento = fecha_nacimiento
        self.__discapacidad = discapacidad
        self.__estado_nivelacion = "Pendiente"
        self.__matricula = None

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
#solicita un cupo en curso- verifica la disponibilidad del cupo
    def solicitar_cupo(self, curso):
        if curso.cupo_actual < curso.cupo_maximo:
            curso.cupo_actual = curso.cupo_actual + 1
            self.__estado_nivelacion = "En Curso"
            print("Cupo asignado en " + curso.nombre + " para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("No hay cupos disponibles en " + curso.nombre)
            return False
#consulta las calificaciones del estudiante
    def consultar_calificaciones(self, calificacion):
        return calificacion.obtener_resumen()
#consulta asistencia 
    def consultar_asistencia(self, asistencia):
        return asistencia.obtener_resumen()
#metodo sobreescrito para mostrar informacion del estudiante
    def mostrar_info(self):
        print("Estudiante: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Documento: " + self.__tipo_documento + " " + self.__numero_documento)
        print("Fecha de nacimiento: " + self.__fecha_nacimiento)
        print("Estado nivelacion: " + self.__estado_nivelacion)
        if self.__discapacidad:
            print("Discapacidad: Si")
        else:
            print("Discapacidad: No")

#clase administrador igual hereda de usuario
class Administrador(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, id_administrador, cargo):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__id_administrador = id_administrador
        self.__cargo = cargo

    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, valor):
        self.__cargo = valor

#gestiona usuario del sistema puede activarlos o desactivarlos
    def gestionar_usuario(self, accion, usuario, **kwargs):
        if accion == "activar":
            usuario.estado = True
            print("Usuario " + usuario.nombres + " activado")
        elif accion == "desactivar":
            usuario.estado = False
            print("Usuario " + usuario.nombres + " desactivado")
        else:
            print("Accion no reconocida")
        if "motivo" in kwargs:
            print("Motivo: " + kwargs["motivo"])
        if "fecha" in kwargs:
            print("Fecha del cambio: " + kwargs["fecha"])
#gestiona procesos administrativos
    def gestionar_procesos(self, proceso):
        print("Proceso ejecutado: " + proceso)
#genera reportes
    def gestionar_reportes(self):
        print("Reporte generado por: " + self.nombres + " " + self.apellidos + " cargo: " + self.__cargo)

#configura parametros ademas se usa args para configurar varios parametros a la vez
    def configurar_parametros(self, *args):
        for item in args: #recorre cada parametro recibido
            print("Parametro configurado: " + str(item[0]) + " = " + str(item[1]))
#gestiona curso
    def gestionar_cursos(self, accion, curso):
        print("Administrador " + self.nombres + " ejecuto " + accion + " en el curso " + curso.nombre)
#metodo sobreescrito aplica polimorfismo 
    def mostrar_info(self):
        print("Administrador: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Cargo: " + self.__cargo)
        print("Correo: " + self.correo)




docente1 = Docente(1, "1300001111", "Valentin", "Perez", "perez123@uleam.edu.ec", "doc123", "0991234567", "Magister en Software", "Programacion OO")
estudiante1 = Estudiante(2, "1300002222", "Maykel", "Castro", "mcastro@uleam.edu.ec", "est123", "0997654321", "Cedula", "1300002222", "2005-03-15")
estudiante2 = Estudiante(3, "1300003333", "Bryan", "Chiquito", "bchiquito@uleam.edu.ec", "est456", "0994567890", "Cedula", "1300003333", "2004-07-22")
admin1 = Administrador(4, "1300004444", "Carlos", "Ortiz", "cortiz@uleam.edu.ec", "adm123", "0993456789", 1, "Director de Nivelacion")

