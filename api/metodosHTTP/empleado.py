from flask import jsonify, request  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError
from werkzeug.security import generate_password_hash

#! MÉTODOS HTTP PARA TABLA EMPLEADO

#* GET
def obtener_empleado(id_empleado, cursor):
    """Función GET para obtener un empleado específico o todos los empleados de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_empleado == 'todos':
            cursor.execute(
            'SELECT idEmpleado, nombre, apellidoPaterno, apellidoMaterno, telefono, correo FROM empleado')
        else:
            cursor.execute('SELECT idEmpleado, nombre, apellidoPaterno, apellidoMaterno, telefono, correo FROM empleado WHERE idEmpleado = %s', (id_empleado,))
        empleados = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in empleados:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idEmpleado': registro[0],
                'nombre': registro[1],
                'apellidoPaterno': registro[2],
                'apellidoMaterno': registro[3],
                'telefono': registro[4],
                'correo': registro[5]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)})

#* POST
def registrar_empleado(body, cursor, conexion):
    """Función POST para registrar un empleado en la base de datos"""
    try:
        contrasenia_encriptada = generate_password_hash(body['contrasenia'], method='pbkdf2:sha256')
        # Se ejecuta una consulta SQL con parámetros
        cursor.execute('INSERT INTO empleado VALUES (%s, %s, %s, %s, %s, %s, %s)', (body['idEmpleado'].upper(), body['nombre'].upper(), body['apellidoPaterno'].upper(), body['apellidoMaterno'].upper(), body['telefono'], body['correo'], contrasenia_encriptada))
        conexion.connection.commit()  # Se confirma la transacción
        return jsonify({'success': True, 'status': 201, 'message': 'Registro exitoso'})  # Se retorna un objeto JSON con un mensaje de éxito
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)})
    
#*PUT
def actualizar_empleado(id_empleado, cursor, conexion):
    try:
        empleado = request.json
        contrasenia_encriptada = generate_password_hash(empleado['contrasenia'], method='pbkdf2:sha256')
        cursor.execute('SELECT nombre, apellidoPaterno, apellidoMaterno, telefono, correo, contrasenia FROM empleado WHERE idEmpleado = %s', (id_empleado,))
        if cursor.fetchone() != None:
            cursor.execute('UPDATE empleado SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, telefono = %s, correo = %s, contrasenia = %s WHERE idEmpleado = %s', (empleado['nombre'].upper(), empleado['apellidoPaterno'].upper(), empleado['apellidoMaterno'].upper(), empleado['telefono'],empleado['correo'].upper(), contrasenia_encriptada, id_empleado,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 202, 'message': 'Actualización exitosa', 'data': empleado})
        else:
            return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Solicitud incorrecta', 'details': 'La solicitud no pudo ser procesada por el servidor'}}) # Se retorna un objeto JSON con un error 500    
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* PUT
def actualizar_empleado(id_empleado, cursor, conexion):
    """Función PUT para actualizar un empleado específico en la base de datos"""

#* DELETE
def eliminar_empleado(id_empleado, cursor, conexion):
    """Función DELETE para eliminar un empleado específico o todos los empleados de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        cursor.execute('DELETE FROM empleado WHERE idEmpleado = %s', (id_empleado,))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 200, 'message': 'Empleado eliminado'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500