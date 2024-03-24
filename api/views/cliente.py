"""Vista que gestiona la lógica de los métodos HTTP para la tabla cliente de la base de datos"""

# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError
from werkzeug.security import generate_password_hash

#! MÉTODOS HTTP PARA TABLA CLIENTE

# * GET


def obtener_clientes(id_cliente, cursor):
    """Función GET para obtener un cliente específico o todos los clientes de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_cliente == 'todos':  # Si no se recibe un id
            cursor.execute(
                'SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, fechaNacimiento, sexo, estadoCivil, calle, numeroExterior, numeroInterior, colonia, codigoPostal, referencia, correo FROM cliente')
        else:  # Si se recibe un id
            # Se ejecuta una consulta SQL con un parámetro
            cursor.execute('SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, fechaNacimiento, sexo, estadoCivil, calle, numeroExterior, numeroInterior, colonia, codigoPostal, referencia, correo FROM cliente WHERE idCliente = %s', (id_cliente,))
        clientes = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in clientes:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idCliente': registro[0],
                'nombre': registro[1],
                'apellidoPaterno': registro[2],
                'apellidoMaterno': registro[3],
                'fechaNacimiento': registro[4],
                'sexo': registro[5],
                'estadoCivil': registro[6],
                'calle': registro[7],
                'numeroExterior': registro[8],
                'numeroInterior': registro[9],
                'colonia': registro[10],
                'codigoPostal': registro[11],
                'referencia': registro[12],
                'correo': registro[13]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * POST


def registrar_cliente(body, cursor, conexion):
    """Función POST para registrar un cliente en la base de datos"""
    try:
        # Se ejecuta una consulta SQL con parámetros
        contrasenia_encriptada = generate_password_hash(
            body['contrasenia'], method='pbkdf2:sha256')
        cursor.execute('INSERT INTO cliente VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (body['telefono'], body['nombre'].upper(), body['apellidoPaterno'].upper(), body['apellidoMaterno'].upper(), body['fechaNacimiento'], body['sexo'].upper(
        ), body['estadoCivil'].upper(), body['calle'].upper(), body['numeroExterior'], body['numeroInterior'], body['colonia'].upper(), body['codigoPostal'], body['referencia'].upper(), body['correo'], contrasenia_encriptada))
        conexion.connection.commit()  # Se confirma la transacción
        # Se retorna un objeto JSON con un mensaje de éxito
        return jsonify({'success': True, 'status': 201, 'message': 'El cliente se ha registrado exitosamente', 'data': {'nombre': body['nombre'].upper(), 'apellidoPaterno': body['apellidoPaterno'].upper(), 'apellidoMaterno': body['apellidoMaterno'].upper(), 'fechaNacimiento': body['fechaNacimiento'], 'sexo': body['sexo'].upper(), 'estadoCivil': body['estadoCivil'].upper(), 'calle': body['calle'].upper(), 'numeroExterior': body['numeroExterior'], 'numeroInterior': body['numeroInterior'], 'colonia': body['colonia'].upper(), 'codigoPostal': body['codigoPostal'], 'referencia': body['referencia'].upper(), 'telefono': body['telefono'], 'correo': body['correo']}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})

# * PUT


def actualizar_cliente(id_cliente, cursor, conexion):
    """Función PUT para actualizar un cliente específico en la base de datos"""
    try:
        cliente = request.json
        contrasenia_encriptada = generate_password_hash(
            cliente['contrasenia'], method='pbkdf2:sha256')
        cursor.execute(
            'SELECT idCliente FROM cliente WHERE idCliente = %s', (id_cliente,))
        if cursor.fetchone() is not None:
            cursor.execute('UPDATE cliente SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, fechaNacimiento = %s, sexo = %s, estadoCivil = %s, calle = %s, numeroExterior = %s, numeroInterior = %s, colonia = %s, codigoPostal = %s, referencia = %s, correo = %s, contrasenia = %s WHERE idCliente = %s', (cliente['nombre'].upper(), cliente['apellidoPaterno'].upper(
            ), cliente['apellidoMaterno'].upper(), cliente['fechaNacimiento'], cliente['sexo'].upper(), cliente['estadoCivil'].upper(), cliente['calle'].upper(), cliente['numeroExterior'], cliente['numeroInterior'], cliente['colonia'].upper(), cliente['codigoPostal'], cliente['referencia'].upper(), cliente['correo'], contrasenia_encriptada, id_cliente,))
            if cliente['telefono'] != id_cliente:
                cursor.execute(
                    'UPDATE cliente SET idCliente = %s WHERE idCliente = %s', (cliente['telefono'], id_cliente,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 200, 'message': 'El cliente se ha actualizado exitosamente', 'data': {'nombre': cliente['nombre'].upper(), 'apellidoPaterno': cliente['apellidoPaterno'].upper(), 'apellidoMaterno': cliente['apellidoMaterno'].upper(), 'fechaNacimiento': cliente['fechaNacimiento'], 'sexo': cliente['sexo'].upper(), 'estadoCivil': cliente['estadoCivil'].upper(), 'calle': cliente['calle'].upper(), 'numeroExterior': cliente['numeroExterior'], 'numeroInterior': cliente['numeroInterior'], 'colonia': cliente['colonia'].upper(), 'codigoPostal': cliente['codigoPostal'], 'referencia': cliente['referencia'].upper(), 'telefono': cliente['telefono'], 'correo': cliente['correo']}})
        else:
            # Se retorna un objeto JSON con un error 404
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Cliente no encontrado', 'details': f'No se encontró el cliente {id_cliente} en la base de datos'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})

# * DELETE


def eliminar_clientes(id_cliente, cursor, conexion):
    """Función DELETE para eliminar un cliente específico o todos los clientes de la base de datos"""
    try:
        cursor.execute(
            'SELECT idCliente FROM cliente WHERE idCliente = %s', (id_cliente,))
        if cursor.fetchone() is not None:
            # Se ejecuta una consulta SQL
            cursor.execute(
                'DELETE FROM cliente WHERE idCliente = %s', (id_cliente,))
            conexion.connection.commit()
            # Se retorna un objeto JSON con un mensaje de éxito
            return jsonify({'success': True, 'status': 200, 'message': f'El cliente {id_cliente} se ha dado de baja exitosamente'})
        else:
            # Se retorna un objeto JSON con un error 404
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Cliente no encontrado', 'details': f'El cliente {id_cliente} no existe'}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})
