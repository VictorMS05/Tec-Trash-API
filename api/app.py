"""Módulo para la creación de la aplicación de Flask y la definición de las rutas de la API"""

from flask import Flask  # Se importa el diccionario de configuraciones
from flask_mysqldb import MySQL  # Se importa la clase MySQL de flask_mysqldb
# Se importa el diccionario de configuraciones
from config import diccionario_de_configuraciones
# Se importan las funciones para manejar errores
from errors.manejo_de_errores import solicitud_incorrecta, pagina_no_encontrada, metodo_no_permitido, tipo_de_medio_no_soportado, error_interno_del_servidor
from views.cliente import obtener_clientes, registrar_cliente, actualizar_cliente, eliminar_cliente, cambiar_contrasenia_cliente, iniciar_sesion_cliente
from views.empleado import obtener_empleado, registrar_empleado, actualizar_empleado, eliminar_empleado, cambiar_contrasenia_empleado, iniciar_sesion_empleado
from views.empresa import obtener_empresa, registrar_empresa, actualizar_empresa, eliminar_empresa, cambiar_contrasenia_empresa
from views.desecho import obtener_desecho, registrar_desecho, actualizar_desecho, eliminar_desecho, asignar_recoleccion_entrega_desecho
from views.recoleccion import obtener_recoleccion, registrar_recoleccion, actualizar_recoleccion, eliminar_recoleccion, finalizar_recoleccion
from views.entrega import obtener_entrega, registrar_entrega, actualizar_entrega, eliminar_entrega, finalizar_entrega

app = Flask(__name__)  # Se crea una instancia de Flask
# Se crea una instancia de MySQL con la configuración de la aplicación
conexion = MySQL(app)

#! RUTAS PARA LA TABLA CLIENTE

# * GET


@app.route('/cliente/<string:id_cliente>')
def get_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla cliente"""
    cursor = conexion.connection.cursor(
    )  # Se crea un cursor para interactuar con la base de datos
    return obtener_clientes(id_cliente, cursor)

# * POST


@app.route('/cliente', methods=['POST'])
def post_1():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla cliente"""
    cursor = conexion.connection.cursor(
    )  # Se crea un cursor para interactuar con la base de datos
    # Se retorna el resultado de la función registrar_cliente
    return registrar_cliente(cursor, conexion)

# * PUT


@app.route('/cliente/<string:id_cliente>', methods=['PUT'])
def put_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla cliente"""
    cursor = conexion.connection.cursor()
    return actualizar_cliente(id_cliente, cursor, conexion)

# * DELETE


@app.route('/cliente/<string:id_cliente>', methods=['DELETE'])
def delete_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla cliente"""
    cursor = conexion.connection.cursor(
    )  # Se crea un cursor para interactuar con la base de datos
    return eliminar_cliente(id_cliente, cursor, conexion)

# * PATCH


@app.route('/cliente/<string:id_cliente>', methods=['PATCH'])
def patch_1(id_cliente):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PATCH para la tabla cliente"""
    cursor = conexion.connection.cursor()
    return cambiar_contrasenia_cliente(id_cliente, cursor, conexion)

# * POST (Iniciar sesión)


@app.route('/cliente/iniciar-sesion', methods=['POST'])
def iniciar_sesion_1():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para iniciar sesión como cliente"""
    cursor = conexion.connection.cursor()
    return iniciar_sesion_cliente(cursor)

#! RUTAS PARA LA TABLA EMPLEADO

# * GET


@app.route('/empleado/<string:id_empleado>')
def get_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return obtener_empleado(id_empleado, cursor)

# * POST


@app.route('/empleado', methods=['POST'])
def post_2():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return registrar_empleado(cursor, conexion)

# * PUT


@app.route('/empleado/<string:id_empleado>', methods=['PUT'])
def put_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return actualizar_empleado(id_empleado, cursor, conexion)

# * DELETE


@app.route('/empleado/<string:id_empleado>', methods=['DELETE'])
def delete_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return eliminar_empleado(id_empleado, cursor, conexion)

# * PATCH


@app.route('/empleado/<string:id_empleado>', methods=['PATCH'])
def patch_2(id_empleado):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PATCH para la tabla empleado"""
    cursor = conexion.connection.cursor()
    return cambiar_contrasenia_empleado(id_empleado, cursor, conexion)

# * POST (Iniciar sesión)


@app.route('/empleado/iniciar-sesion', methods=['POST'])
def iniciar_sesion_2():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para iniciar sesión como empleado"""
    cursor = conexion.connection.cursor()
    return iniciar_sesion_empleado(cursor)

#! RUTAS PARA LA TABLA EMPRESA

# * GET


@app.route('/empresa/<string:id_empresa>')
def get_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return obtener_empresa(id_empresa, cursor)

# * POST


@app.route('/empresa', methods=['POST'])
def post_3():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return registrar_empresa(cursor, conexion)

# * PUT


@app.route('/empresa/<string:id_empresa>', methods=['PUT'])
def put_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return actualizar_empresa(id_empresa, cursor, conexion)

# * DELETE


@app.route('/empresa/<string:id_empresa>', methods=['DELETE'])
def delete_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return eliminar_empresa(id_empresa, cursor, conexion)

# * PATCH


@app.route('/empresa/<string:id_empresa>', methods=['PATCH'])
def patch_3(id_empresa):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PATCH para la tabla empresa"""
    cursor = conexion.connection.cursor()
    return cambiar_contrasenia_empresa(id_empresa, cursor, conexion)

#! RUTAS PARA LA TABLA DESECHO

# * GET


@app.route('/desecho/<string:id_desecho>')
def get_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return obtener_desecho(id_desecho, cursor)

# * POST


@app.route('/desecho', methods=['POST'])
def post_4():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return registrar_desecho(cursor, conexion)

# * PUT


@app.route('/desecho/<string:id_desecho>', methods=['PUT'])
def put_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return actualizar_desecho(id_desecho, cursor, conexion)

# * DELETE


@app.route('/desecho/<string:id_desecho>', methods=['DELETE'])
def delete_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return eliminar_desecho(id_desecho, cursor, conexion)

# * PATCH


@app.route('/desecho/<string:id_desecho>', methods=['PATCH'])
def patch_4(id_desecho):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PATCH para la tabla desecho"""
    cursor = conexion.connection.cursor()
    return asignar_recoleccion_entrega_desecho(id_desecho, cursor, conexion)

#! RUTAS PARA LA TABLA RECOLECCIÓN

# * GET


@app.route('/recoleccion/<string:id_recoleccion>')
def get_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return obtener_recoleccion(id_recoleccion, cursor)

# * POST


@app.route('/recoleccion', methods=['POST'])
def post_5():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return registrar_recoleccion(cursor, conexion)

# * PUT


@app.route('/recoleccion/<string:id_recoleccion>', methods=['PUT'])
def put_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return actualizar_recoleccion(id_recoleccion, cursor, conexion)

# * DELETE


@app.route('/recoleccion/<string:id_recoleccion>', methods=['DELETE'])
def delete_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return eliminar_recoleccion(id_recoleccion, cursor, conexion)

# * PATCH


@app.route('/recoleccion/<string:id_recoleccion>', methods=['PATCH'])
def patch_5(id_recoleccion):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PATCH para la tabla recolección"""
    cursor = conexion.connection.cursor()
    return finalizar_recoleccion(id_recoleccion, cursor, conexion)

#! RUTAS PARA LA TABLA ENTREGA

# * GET


@app.route('/entrega/<string:id_entrega>')
def get_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método GET para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return obtener_entrega(id_entrega, cursor)

# * POST


@app.route('/entrega', methods=['POST'])
def post_6():
    """Función para ejecutar la conexión a la base de datos y ejecutar el método POST para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return registrar_entrega(cursor, conexion)

# * PUT


@app.route('/entrega/<string:id_entrega>', methods=['PUT'])
def put_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PUT para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return actualizar_entrega(id_entrega, cursor, conexion)

# * DELETE


@app.route('/entrega/<string:id_entrega>', methods=['DELETE'])
def delete_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método DELETE para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return eliminar_entrega(id_entrega, cursor, conexion)

# * PATCH


@app.route('/entrega/<string:id_entrega>', methods=['PATCH'])
def patch_6(id_entrega):
    """Función para ejecutar la conexión a la base de datos y ejecutar el método PATCH para la tabla entrega"""
    cursor = conexion.connection.cursor()
    return finalizar_entrega(id_entrega, cursor, conexion)


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
    # Se registra la función para manejar errores 415
    app.register_error_handler(415, tipo_de_medio_no_soportado)
    # Se registra la función para manejar errores 500
    app.register_error_handler(500, error_interno_del_servidor)
    app.run()  # Se ejecuta la aplicación
