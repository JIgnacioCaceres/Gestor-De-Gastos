import pyodbc

# Configuración de la conexión a SQL Server
SERVER = 'localhost'  # Cambia a tu servidor
DATABASE = 'ControlDeGastos'
USERNAME = 'sa'
PASSWORD = '2580'

def conectar():
    try:
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes"
        )
        print("Conexión exitosa a la base de datos")
        return conexion
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
