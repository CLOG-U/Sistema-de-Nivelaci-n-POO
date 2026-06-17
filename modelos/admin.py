from modelos.usuario import Usuario


class Administrador(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, id_administrador, cargo):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__id_administrador = id_administrador
        self.__cargo = cargo
    
    #uso de propiedades 
    @property
    def id_administrador(self):
        return self.__id_administrador

    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, valor):
        self.__cargo = valor
    
    #gestiona usuario del sistema puede activarlos o desactivarlos
    def gestionar_usuario(self, accion, usuario, motivo=None, fecha=None):
        #si usuario es None se lanza una excepcion
        if usuario is None:
            raise ValueError("Debe proporcionar un usuario para gestionar")
        #si accion no es activar o desactivar se lanza una excepcion
        if accion not in ("activar", "desactivar"):
            raise ValueError(f"Acción no reconocida: {accion}")
        
        #se cambia el estado del usuario segun la accion
        usuario.estado = accion == "activar"
        estado_texto = "activado" if usuario.estado else "desactivado"
        mensaje = f"Usuario {usuario.nombres} {usuario.apellidos} {estado_texto}"
        
        #creamos una lista de detalles para incluir el detalle del motivo 
        detalles = []
        if motivo:
            #si se proporciona un motivo se agrega a los detalles
            detalles.append(f"Motivo: {motivo}")
        if fecha:
            #si se proporciona una fecha se agrega a los detalles
            detalles.append(f"Fecha del cambio: {fecha}")
        #si hay detalles se agregan al mensaje
        if detalles:
            mensaje += ". " + ", ".join(detalles)

        print(mensaje)
        return mensaje
    
    #gestiona procesos administrativos
    def gestionar_procesos(self, proceso):
        mensaje = "Proceso ejecutado: " + proceso
        print(mensaje)
        return mensaje
    
    #genera reportes
    def gestionar_reportes(self):
        mensaje = "Reporte generado por: " + self.nombres + " " + self.apellidos + " cargo: " + self.__cargo
        print(mensaje)
        return mensaje
    
    #configura parametros ademas se usa args para configurar varios parametros a la vez
    def configurar_parametros(self, *args):
        #creamos una lista de lineas para mostrar cada parametro configurado
        lineas = []
        for item in args:
            #cada item se espera que sea una tupla con clave y valor
            clave = str(item[0])
            valor = str(item[1])
            lineas.append("Parametro configurado: " + clave + " = " + valor)  #se agrega una linea por cada parametro configurado
        mensaje = "\n".join(lineas) if lineas else "Sin parametros configurados"
        print(mensaje)
        return mensaje
    
    #gestionar cursos, se usa un metodo para abrir o cerrar cursos
    def gestionar_cursos(self, accion, curso):
        #si curso es None se lanza una excepcion 
        if curso is None:
            raise ValueError("Debe proporcionar un curso para gestionar")
        #si accion es abrir se abre el curso
        if accion == "abrir":
            curso.abrir_curso()
            mensaje = f"Administrador {self.nombres} {self.apellidos} abrió el curso {curso.nombre}"
        #si accion es cerrar se cierra el curso
        elif accion == "cerrar":
            curso.cerrar_curso()
            mensaje = f"Administrador {self.nombres} {self.apellidos} cerró el curso {curso.nombre}"
        #else: se lanza una excepcion si la accion no es reconocida
        else:
            raise ValueError(f"Acción no reconocida: {accion}")

        print(mensaje)
        return mensaje
    
    #metodo sobreescrito para iniciar sesion
    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            mensaje = "Inicio de sesion como administrador correctamente para " + self.nombres + " " + self.apellidos
            print(mensaje)
            return True
        else:
            mensaje = "Contraseña incorrecta o usuario inactivo"
            print(mensaje)
            return False
    
    #metodo sobreescrito para mostrar informacion del administrador
    def mostrar_info(self):
        mensaje = (
            "Administrador: " + self.nombres + " " + self.apellidos + "\n"
            + "Cedula: " + self.cedula + "\n"
            + "Cargo: " + self.__cargo + "\n"
            + "Correo: " + self.correo
        )
        print(mensaje)
        return mensaje
