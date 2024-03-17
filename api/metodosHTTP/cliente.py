from flask import jsonify, request  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError
from werkzeug.security import generate_password_hash

#! MÉTODOS HTTP PARA TABLA CLIENTE

#* GET
def obtener_clientes(id_cliente, cursor):
    """Función GET para obtener un cliente específico o todos los clientes de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_cliente == 'todos':  # Si no se recibe un id
            cursor.execute(
            'SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, calle, numeroExterior, colonia, codigoPostal, telefono, correo, contrasenia FROM cliente')
        else:  # Si se recibe un id
            cursor.execute('SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, calle, numeroExterior, colonia, codigoPostal, correo, contrasenia FROM cliente WHERE idCliente = %s', (id_cliente,))  # Se ejecuta una consulta SQL con un parámetro
        clientes = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in clientes:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idCliente': registro[0],
                'nombre': registro[1],
                'apellidoPaterno': registro[2],
                'apellidoMaterno': registro[3],
                'calle': registro[4],
                'numeroExterior': registro[5],
                'colonia': registro[6],
                'codigoPostal': registro[7],
                'correo': registro[8],
                'contrasenia': registro[9]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* POST
def registrar_cliente(body, cursor, conexion):
    """Función POST para registrar un cliente en la base de datos"""
    try:
        # Se ejecuta una consulta SQL con parámetros
        print("Gus: " + body['idCliente'])
        contrasenia_encriptada = generate_password_hash(body['contrasenia'], method='pbkdf2:sha256')
        print("Sharon: " + body['idCliente'])
        cursor.execute('INSERT INTO cliente VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (body['idCliente'], body['nombre'].upper(), body['apellidoPaterno'].upper(), body['apellidoMaterno'].upper(), body['calle'].upper(), body['numeroExterior'], body['colonia'].upper(), body['codigoPostal'], body['correo'], contrasenia_encriptada))
        print("Yureli: " + body['idCliente'])
        conexion.connection.commit()  # Se confirma la transacción
        return jsonify({'success': True, 'status': 201, 'message': 'Registro exitoso'})  # Se retorna un objeto JSON con un mensaje de éxito
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500    

#* DELETE
def eliminar_clientes(id_cliente, cursor, conexion):
    """Función DELETE para eliminar un cliente específico o todos los clientes de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        cursor.execute('DELETE FROM empresa WHERE idEmpresa = %s', (id_cliente,))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 200, 'message': 'Cliente eliminado'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
    
#* PUT
def actualizar_cliente(id_cliente, cursor, conexion):
    try:
        cliente = request.json
        cursor.execute('SELECT nombre, apellidoPaterno, apellidoMaterno, calle, numeroExterior, colonia, codigoPostal, correo, contrasenia FROM cliente WHERE idCliente = %s', (id_cliente,))
        if cursor.fetchone() != None:
            cursor.execute('UPDATE cliente SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, calle = %s, numeroExterior = %s, colonia = %s, codigoPostal = %s, correo = %s WHERE idCliente = %s', (cliente['nombre'], cliente['apellidoPaterno'], cliente['apellidoMaterno'], cliente['calle'],cliente['numeroExterior'],cliente['colonia'],cliente['codigoPostal'],cliente['correo'], cliente['contrasenia'], id_cliente,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 202, 'message': 'Actualización exitosa', 'data': cliente})
        else:
            return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Solicitud incorrecta', 'details': 'La solicitud no pudo ser procesada por el servidor'}}) # Se retorna un objeto JSON con un error 500    
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500