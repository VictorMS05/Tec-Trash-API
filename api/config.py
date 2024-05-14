"""Módulo de la configuración de la aplicación"""

from dotenv import load_dotenv

class DevelopmentConfig():
    """Clase de configuración para desarrollo"""
    DEBUG = True
    MYSQL_HOST = load_dotenv().get('MYSQL_HOST')
    MYSQL_USER = load_dotenv().get('MYSQL_USER')
    MYSQL_PASSWORD = load_dotenv().get('MYSQL_PASSWORD')
    MYSQL_DB = load_dotenv().get('MYSQL_DB')
    MYSQL_PORT = 3306

diccionario_de_configuraciones = { # Diccionario de configuraciones
    'development': DevelopmentConfig # Configuración de desarrollo
}
