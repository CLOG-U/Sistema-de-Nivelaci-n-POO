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

            conexion_str = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                "Trusted_Connection=yes;"
                "Encrypt=no;"
            )
            
            self.conn = pyodbc.connect(conexion_str)
            self.cursor = self.conn.cursor()
            
        except pyodbc.Error as e:
            print(f"Error crítico al conectar a SQL Server: {e}")
            raise e

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
