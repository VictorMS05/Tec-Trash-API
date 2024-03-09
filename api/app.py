from flask import Flask
from config import diccionario_de_configuraciones # Se importa el diccionario de configuraciones

app = Flask(__name__) # Se crea una instancia de Flask

@app.route('/') # Se define la ruta de la aplicación
def index():
    """"Esta función se ejecutará cuando el usuario entre a la ruta /"""
    return 'Sharon <3' # Se retorna un mensaje

if __name__ == '__main__': # Si la instancia de Flask es la principal
    app.config.from_object(diccionario_de_configuraciones['development']) # Se configura la aplicación con la configuración de desarrollo
    app.run() # Se ejecuta la aplicación
