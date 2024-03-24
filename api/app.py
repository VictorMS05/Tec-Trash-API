"""Módulo para la creación de la aplicación de Flask y la definición de las rutas de la API"""

from flask import Flask, request # Se importa el diccionario de configuraciones
from flask_mysqldb import MySQL # Se importa la clase MySQL de flask_mysqldb
from config import diccionario_de_configuraciones # Se importa el diccionario de configuraciones
from manejo_de_errores import solicitud_incorrecta, pagina_no_encontrada, metodo_no_permitido, error_interno_del_servidor # Se importan las funciones para manejar errores
from vistas.cliente import obtener_clientes, registrar_cliente, actualizar_cliente, eliminar_clientes
from vistas.empleado import obtener_empleado, registrar_empleado, actualizar_empleado, eliminar_empleado
from vistas.empresa import obtener_empresa, registrar_empresa, actualizar_empresa, eliminar_empresa
from vistas.desecho import obtener_desecho, registrar_desecho, actualizar_desecho, eliminar_desecho
from vistas.recoleccion import obtener_recoleccion, registrar_recoleccion, actualizar_recoleccion, eliminar_recoleccion
from vistas.entrega import obtener_entrega, registrar_entrega, actualizar_entrega, eliminar_entrega

app = Flask(__name__)  # Se crea una instancia de Flask
conexion = MySQL(app) # Se crea una instancia de MySQL con la configuración de la aplicación

#! RUTAS PARA LA TABLA CLIENTE
#* GET
@app.route('/cliente/<string:id_cliente>')  # Se define la ruta de la aplicación
def get_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla cliente"""
    cursor = conexion.connection.cursor() # Se crea un cursor para interactuar con la base de datos
    return obtener_clientes(id_cliente, cursor)
#* POST
@app.route('/cliente', methods=['POST'])  # Se define la ruta de la aplicación
def post_1():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla cliente"""
    cursor = conexion.connection.cursor()  # Se crea un cursor para interactuar con la base de datos
    return registrar_cliente(request.json, cursor, conexion)  # Se retorna el resultado de la función registrar_cliente
#* PUT
@app.route('/cliente/<string:id_cliente>', methods = ['PUT'])  # Se define la ruta de la aplicación
def put_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla cliente"""
    cursor = conexion.connection.cursor()
    return actualizar_cliente(id_cliente, cursor, conexion)
#* DELETE
@app.route('/cliente/<string:id_cliente>', methods = ['DELETE'])
def delete_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla cliente"""
    cursor = conexion.connection.cursor() # Se crea un cursor para interactuar con la base de datos
    return eliminar_clientes(id_cliente, cursor, conexion)

#! RUTAS PARA LA TABLA EMPLEADO
#* GET
@app.route('/empleado/<string:id_empleado>')  # Se define la ruta de la aplicación
def get_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return obtener_empleado(id_empleado, cursor)
#* POST
@app.route('/empleado', methods=['POST'])  # Se define la ruta de la aplicación
def post_2():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return registrar_empleado(request.json, cursor, conexion)
#* PUT
@app.route('/empleado/<string:id_empleado>', methods = ['PUT'])  # Se define la ruta de la aplicación
def put_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return actualizar_empleado(id_empleado, cursor, conexion)
#* DELETE
@app.route('/empleado/<string:id_empleado>', methods = ['DELETE'])  # Se define la ruta de la aplicación
def delete_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return eliminar_empleado(id_empleado, cursor, conexion)

#! RUTAS PARA LA TABLA EMPRESA
#* GET
@app.route('/empresa/<string:id_empresa>')  # Se define la ruta de la aplicación
def get_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return obtener_empresa(id_empresa, cursor)
#* POST
@app.route('/empresa', methods = ['POST'])  # Se define la ruta de la aplicación
def post_3():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return registrar_empresa(cursor, conexion)
#* PUT
@app.route('/empresa/<string:id_empresa>', methods = ['PUT'])  # Se define la ruta de la aplicación
def put_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return actualizar_empresa(id_empresa, cursor, conexion)
#* DELETE
@app.route('/empresa/<string:id_empresa>', methods = ['DELETE'])  # Se define la ruta de la aplicación
def delete_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return eliminar_empresa(id_empresa, cursor, conexion)

#! RUTAS PARA LA TABLA DESECHO
#* GET
@app.route('/desecho/<string:id_desecho>')  # Se define la ruta de la aplicación
def get_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return obtener_desecho(id_desecho, cursor)
#* POST
@app.route('/desecho', methods=['POST'])  # Se define la ruta de la aplicación
def post_4():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return registrar_desecho(request.json, cursor, conexion)
#* PUT
@app.route('/desecho/<string:id_desecho>', methods = ['PUT'])  # Se define la ruta de la aplicación
def put_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return actualizar_desecho(id_desecho, cursor, conexion)
#* DELETE
@app.route('/desecho/<string:id_desecho>', methods=['DELETE'])
def delete_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return eliminar_desecho(id_desecho, cursor, conexion)

#! RUTAS PARA LA TABLA RECOLECCIÓN
#* GET
@app.route('/recoleccion/<string:id_recoleccion>')  # Se define la ruta de la aplicación
def get_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return obtener_recoleccion(id_recoleccion, cursor)
#* POST
@app.route('/recoleccion', methods=['POST'])  # Se define la ruta de la aplicación
def post_5():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return registrar_recoleccion(request.json, cursor, conexion)
#* PUT
@app.route('/recoleccion/<string:id_recoleccion>', methods = ['PUT'])  # Se define la ruta de la aplicación
def put_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return actualizar_recoleccion(id_recoleccion, cursor, conexion)
#* DELETE
@app.route('/recoleccion/<string:id_recoleccion>', methods = ['DELETE'])  # Se define la ruta de la aplicación
def delete_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return eliminar_recoleccion(id_recoleccion, cursor, conexion)

#! RUTAS PARA LA TABLA ENTREGA
#* GET
@app.route('/entrega/<string:id_entrega>')  # Se define la ruta de la aplicación
def get_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return obtener_entrega(id_entrega, cursor)
#* POST
@app.route('/entrega', methods=['POST'])  # Se define la ruta de la aplicación
def post_6():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return registrar_entrega(request.json, cursor, conexion)
#* PUT
@app.route('/entrega/<string:id_entrega>', methods = ['PUT'])  # Se define la ruta de la aplicación
def put_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return actualizar_entrega(id_entrega, cursor, conexion)
#* DELETE
@app.route('/entrega/<string:id_entrega>', methods = ['DELETE'])  # Se define la ruta de la aplicación
def delete_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return eliminar_entrega(id_entrega, cursor, conexion)
    return eliminar_entrega(id_entrega, cursor, conexion)

#! EJECUCIÓN DE LA APLICACIÓN
if __name__ == '__main__':  # Si la instancia de Flask es la principal
    # Se configura la aplicación con la configuración de desarrollo
    app.config.from_object(diccionario_de_configuraciones['development'])
    # Se registra la función para manejar errores 400
    app.register_error_handler(400, solicitud_incorrecta)
    # Se registra la función para manejar errores 404
    app.register_error_handler(404, pagina_no_encontrada)
    # Se registra la función para manejar errores 405
    app.register_error_handler(405, metodo_no_permitido)
    # Se registra la función para manejar errores 500
    app.register_error_handler(500, error_interno_del_servidor)
    app.run()  # Se ejecuta la aplicación
