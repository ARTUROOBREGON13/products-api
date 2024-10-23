import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

class Config:
    # Configuraciones de MySQL
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')  # Cambia esto si no usas root
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'mydatabase')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))  # Puerto por defecto de MySQL
    JWT_SECRET = os.getenv('JWT_SECRET', 'tu_clave_secreta')
    SWAGGER_URL = os.getenv('SWAGGER_URL', '/api')
    DEBUG = True  # O False en producción
