class PeriodoAcademico:

    def __init__(self, id_periodo, nombre, fecha_inicio, fecha_fin, estado="Cerrado"):  # Inicializa los datos principales del período académico.
        self.__id_periodo = id_periodo
        self.__nombre = nombre
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__estado = estado
#usamos propiedades para acceder a los atributos privados 
    # Métodos Getter (lectura)
    @property
    def id_periodo(self):
        return self.__id_periodo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    @property
    def estado(self):
        return self.__estado
# Método Setter (modificación)
    @estado.setter
    def estado(self, valor):
        self.__estado = valor
#se cambia el estado del periodo a abierto 
    def abrir_periodo(self):
        self.__estado = "Abierto"
        print("Periodo " + self.__nombre + " abierto")
#se cambia el estado del periodo a cerrado
    def cerrar_periodo(self):
        self.__estado = "Cerrado"
        print("Periodo " + self.__nombre + " cerrado")

#Muestra la información principal del período académico, incluyendo las fechas de inicio, fin y su estado.
    def listar_periodos(self):
        print("Periodo: " + self.__nombre + " del " + self.__fecha_inicio + " al " + self.__fecha_fin + " estado: " + self.__estado)
