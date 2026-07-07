import pyodbc
# Clase encargada de administrar la conexión con la base de datos.
class ConexionDB:
    def __init__(self):
        # Nombre del servidor donde está instalado SQL Server.
        self.server = "localhost"  
        # Nombre de la base de datos a la que se desea conectar.
        self.database = "PROYECTOPOO"
        
        self.driver = "{ODBC Driver 17 for SQL Server}"
        # Variable donde se almacenará la conexión con SQL Server.
        # Inicialmente no existe conexión.
        self.conn = None
         # Variable donde se almacenará el cursor para ejecutar consultas SQL.
        self.cursor = None
     # Método que establece la conexión con la base de datos.
    def conectar(self):
        try:
            # Cadena de conexión con los datos necesarios.
            conexion_str = (
                f"DRIVER={self.driver};"  # Driver ODBC
                f"SERVER={self.server};"  # Servidor SQL
                f"DATABASE={self.database};" # Base de datos
                "Trusted_Connection=yes;"
                "Encrypt=no;"
            )
            # Crea la conexión utilizando la cadena anterior.
            self.conn = pyodbc.connect(conexion_str)
             # Crea un cursor para poder ejecutar instrucciones SQL.
            self.cursor = self.conn.cursor()
         # Captura cualquier error que ocurra durante la conexión.
        except pyodbc.Error as e:
            # Muestra un mensaje indicando que ocurrió un error.
            print(f"Error crítico al conectar a SQL Server: {e}")
            raise e
     # Método encargado de cerrar la conexión con la base de datos.
    def cerrar(self):
         # Si existe un cursor, lo cierra.
        if self.cursor:
            self.cursor.close()
        # Si existe una conexión, la cierra.
        if self.conn:
            self.conn.close()
