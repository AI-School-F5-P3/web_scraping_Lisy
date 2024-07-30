import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

def create_log_connection():
    """Crea y retorna una conexión a la base de datos de logs."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('LOG_DB_HOST'),
            database=os.getenv('LOG_DB_NAME'),
            user=os.getenv('LOG_DB_USER'),
            password=os.getenv('LOG_DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos de logs: {e}")
        return None

def log_to_database(level, message):
    """Registra un mensaje en la base de datos de logs."""
    log_connection = create_log_connection()
    if not log_connection:
        print("No se pudo establecer la conexión a la base de datos de logs.")
        return
    
    try:
        cursor = log_connection.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT IGNORE INTO logs (timestamp, level, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (timestamp, level, message))
        log_connection.commit()
    except Error as e:
        print(f"Error al registrar log en la base de datos de logs: {e}")
    finally:
        if log_connection.is_connected():
            cursor.close()
            log_connection.close()
