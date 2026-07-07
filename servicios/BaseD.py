import pyodbc
class ConexionDB:
    def __init__(self):
        self.server = "localhost"  
        self.database = "PROYECTOPOO"
        
        self.driver = "{ODBC Driver 17 for SQL Server}"
        
        self.conn = None
        self.cursor = None
