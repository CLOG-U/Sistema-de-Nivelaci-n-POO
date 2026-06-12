from Usuario import Usuario
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
    
    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            print("Inicio de sesion como administrador correctamente para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False

#metodo sobreescrito aplica polimorfismo 
    def mostrar_info(self):
        print("Administrador: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Cargo: " + self.__cargo)
        print("Correo: " + self.correo)
