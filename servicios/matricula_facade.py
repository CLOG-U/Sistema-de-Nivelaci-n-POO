#importamos la clase Matricula del módulo modelos.matricula
from modelos.matricula import Matricula


class MatriculaFacade:
    #el constructor recibe el periodo, curso y estudiante como parámetros
    def __init__(self, periodo, curso, estudiante):
        self.__periodo = periodo
        self.__curso = curso
        self.__estudiante = estudiante
    
    #creamos el método matricula
    def matricular(self, id_matricula, fecha, tipo):
        #compruebamos si el periodo está cerrado, si esta cerrado no se puede matricular y se retorna False
        if self.__periodo.estado == "Cerrado":
            print("No se puede matricular, el periodo está cerrado")
            return False
        self.__curso.agregar_estudiante(self.__estudiante)     #si el periodo está abierto, se agrega el estudiante al curso y se crea una instancia de Matricula
        
        #creamos una instancia de Matricula con los parámetros id_matricula, fecha, tipo y el nombre del periodo
        matricula = Matricula(id_matricula, fecha, tipo, self.__periodo.nombre)
        matricula.procesar_matricula()    #llamamos al método procesar_matricula de la instancia de Matricula
        self.__estudiante.matricula = matricula    #asignamos la instancia de Matricula al atributo matricula del estudiante
        
        #se imprime un mensaje indicando que la matrícula se completó correctamente
        print("Matricula completada para " + self.__estudiante.nombres)
        return True
