class CargaAcademica:

    def __init__(self, id_carga, estudiante, periodo, total_asignaturas, total_creditos, estado=True):
        self.__id_carga = id_carga
        self.__estudiante = estudiante
        self.__periodo = periodo
        self.__total_asignaturas = total_asignaturas
        self.__total_creditos = total_creditos
        self.__estado = estado

    @property
    def id_carga(self):
        return self.__id_carga

    @property
    def estudiante(self):
        return self.__estudiante

    @property
    def periodo(self):
        return self.__periodo

    @property
    def total_asignaturas(self):
        return self.__total_asignaturas

    @property
    def total_creditos(self):
        return self.__total_creditos

    @property
    def estado(self):
        return self.__estado

    @total_creditos.setter
    def total_creditos(self, valor):
        if valor < 0:
            print("Los creditos no pueden ser negativos")
        else:
            self.__total_creditos = valor

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    def generar_carga(self):
        print("Carga academica de " + self.__estudiante.nombres + " " + self.__estudiante.apellidos)
        print("Periodo: " + self.__periodo)
        print(str(self.__total_asignaturas) + " asignaturas " + str(self.__total_creditos) + " creditos")

