class DevelopmentConfig(): # Clase de configuración para desarrollo
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tectrash'
    MYSQL_PORT = 3306

diccionario_de_configuraciones = { # Diccionario de configuraciones
    'development': DevelopmentConfig # Configuración de desarrollo
}
