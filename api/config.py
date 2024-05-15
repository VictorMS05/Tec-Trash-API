"""Módulo de la configuración de la aplicación"""

import os
from dotenv import load_dotenv

class DevelopmentConfig():
    """Clase de configuración para desarrollo"""
    load_dotenv()
    DEBUG = True
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_PORT = os.getenv('MYSQL_PORT')

diccionario_de_configuraciones = { # Diccionario de configuraciones
    'development': DevelopmentConfig # Configuración de desarrollo
}
