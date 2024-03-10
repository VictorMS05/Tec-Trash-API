from flask import Flask # Se importa el diccionario de configuraciones
from flask_mysqldb import MySQL # Se importa la clase MySQL de flask_mysqldb
from config import diccionario_de_configuraciones # Se importa la función para manejar errores 404
from manejo_de_errores import pagina_no_encontrada
from metodosHTTP.cliente import obtener_clientes
from metodosHTTP.empleado import obtener_empleado
from metodosHTTP.empresa import obtener_empresa
from metodosHTTP.desecho import obtener_desecho
from metodosHTTP.entrega import obtener_entrega
from metodosHTTP.recoleccion import obtener_recoleccion

app = Flask(__name__)  # Se crea una instancia de Flask
conexion = MySQL(app) # Se crea una instancia de MySQL con la configuración de la aplicación

#! RUTAS PARA LA TABLA CLIENTE
#* GET
@app.route('/api/cliente/<string:id_cliente>')  # Se define la ruta de la aplicación
def get_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla cliente"""
    cursor = conexion.connection.cursor() # Se crea un cursor para interactuar con la base de datos
    return obtener_clientes(id_cliente, cursor)

#! RUTAS PARA LA TABLA EMPLEADO
#* GET
@app.route('/api/empleado/<string:id_empleado>')  # Se define la ruta de la aplicación
def get_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return obtener_empleado(id_empleado, cursor)

#! RUTAS PARA LA TABLA EMPRESA
#* GET
@app.route('/api/empresa/<string:id_empresa>')  # Se define la ruta de la aplicación
def get_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return obtener_empresa(id_empresa, cursor)

#! RUTAS PARA LA TABLA DESECHO
#* GET
@app.route('/api/desecho/<string:id_desecho>')  # Se define la ruta de la aplicación
def get_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return obtener_desecho(id_desecho, cursor)

#! RUTAS PARA LA TABLA RECOLECCIÓN
#* GET
@app.route('/api/recoleccion/<string:id_recoleccion>')  # Se define la ruta de la aplicación
def get_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return obtener_recoleccion(id_recoleccion, cursor)

#! RUTAS PARA LA TABLA ENTREGA
#* GET
@app.route('/api/entrega/<string:id_entrega>')  # Se define la ruta de la aplicación
def get_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return obtener_entrega(id_entrega, cursor)

#! EJECUCIÓN DE LA APLICACIÓN
if __name__ == '__main__':  # Si la instancia de Flask es la principal
    # Se configura la aplicación con la configuración de desarrollo
    app.config.from_object(diccionario_de_configuraciones['development'])
    # Se registra la función para manejar errores 404
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()  # Se ejecuta la aplicación
