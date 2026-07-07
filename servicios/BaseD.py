import pyodbc
class ConexionDB:
    def __init__(self):
        self.server = "localhost"  
        self.database = "PROYECTOPOO"
        
        self.driver = "{ODBC Driver 17 for SQL Server}"
        
        self.conn = None
        self.cursor = None
        
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
