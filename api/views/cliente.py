"""Vista que gestiona la lógica de los métodos HTTP para la tabla cliente de la base de datos"""

# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA CLIENTE

# * GET


def consultar_clientes(id_cliente, cursor):
    """Función GET para consultar un cliente específico o todos los clientes de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_cliente == 'todos':  # Si no se recibe un id
            cursor.execute('SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, '
                            'fechaNacimiento, sexo, estadoCivil, calle1, numeroExterior1, '
                            'numeroInterior1, colonia1, codigoPostal1, referencia1, calle2, '
                            'numeroExterior2, numeroInterior2, colonia2, codigoPostal2, '
                            'referencia2, calle3, numeroExterior3, numeroInterior3, colonia3, '
                            'codigoPostal3, referencia3, correo FROM cliente')
        else:  # Si se recibe un id
            # Se ejecuta una consulta SQL con un parámetro
            cursor.execute(f'SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, '
                            f'fechaNacimiento, sexo, estadoCivil, calle1, numeroExterior1, '
                            f'numeroInterior1, colonia1, codigoPostal1, referencia1, calle2, '
                            f'numeroExterior2, numeroInterior2, colonia2, codigoPostal2, '
                            f'referencia2, calle3, numeroExterior3, numeroInterior3, colonia3, '
                            f'codigoPostal3, referencia3, correo FROM '
                            f'cliente WHERE idCliente = {id_cliente}')
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
                'calle1': registro[7],
                'numeroExterior1': registro[8],
                'numeroInterior1': registro[9],
                'colonia1': registro[10],
                'codigoPostal1': registro[11],
                'referencia1': registro[12],
                'calle2': registro[13],
                'numeroExterior2': registro[14],
                'numeroInterior2': registro[15],
                'colonia2': registro[16],
                'codigoPostal2': registro[17],
                'referencia2': registro[18],
                'calle3': registro[19],
                'numeroExterior3': registro[20],
                'numeroInterior3': registro[21],
                'colonia3': registro[22],
                'codigoPostal3': registro[23],
                'referencia3': registro[24],
                'correo': registro[25]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True,
                        'status': 200, 
                        'message': 'Consulta exitosa', 
                        'data': diccionario})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * POST


def insertar_cliente(cursor, conexion):
    """Función POST para insertar un cliente en la base de datos"""
    try:
        body = request.json  # Se obtiene el body de la petición
        # Se ejecuta una consulta SQL con parámetros
        cursor.execute('INSERT INTO cliente (idCliente, nombre, apellidoPaterno, apellidoMaterno, '
                        'fechaNacimiento, sexo, estadoCivil, calle1, numeroExterior1, '
                        'numeroInterior1, colonia1, codigoPostal1, referencia1, correo, '
                        'contrasenia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                        '%s, %s, %s, MD5(%s))', (body['telefono'], body['nombre'].upper(),
                                                    body['apellidoPaterno'].upper(),
                                                    body['apellidoMaterno'].upper(),
                                                    body['fechaNacimiento'], body['sexo'].upper(),
                                                    body['estadoCivil'].upper(),
                                                    body['calle1'].upper(), body['numeroExterior1'],
                                                    body['numeroInterior1'],
                                                    body['colonia1'].upper(), body['codigoPostal1'],
                                                    body['referencia1'].upper(), body['correo'],
                                                    body['contrasenia']))
        conexion.connection.commit()  # Se confirma la transacción
        # Se retorna un objeto JSON con un mensaje de éxito
        return jsonify({'success': True,
                        'status': 201, 
                        'message': 'El cliente se ha registrado exitosamente', 
                        'data': {'nombre': body['nombre'].upper(), 
                                    'apellidoPaterno': body['apellidoPaterno'].upper(), 
                                    'apellidoMaterno': body['apellidoMaterno'].upper(), 
                                    'fechaNacimiento': body['fechaNacimiento'], 
                                    'sexo': body['sexo'].upper(), 
                                    'estadoCivil': body['estadoCivil'].upper(), 
                                    'calle': body['calle1'].upper(), 
                                    'numeroExterior': body['numeroExterior1'], 
                                    'numeroInterior': body['numeroInterior1'], 
                                    'colonia': body['colonia1'].upper(), 
                                    'codigoPostal': body['codigoPostal1'], 
                                    'referencia': body['referencia1'].upper(),  
                                    'telefono': body['telefono'], 
                                    'correo': body['correo']}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * PUT


def actualizar_cliente(id_cliente, cursor, conexion):
    """Función PUT para actualizar un cliente específico en la base de datos"""
    try:
        body = request.json  # Se obtiene el body de la petición
        cursor.execute(f'SELECT COUNT(idCliente) > 0 FROM cliente WHERE idCliente = {id_cliente}')
        if cursor.fetchone()[0]:
            cursor.execute('UPDATE cliente SET nombre = %s, apellidoPaterno = %s, '
                            'apellidoMaterno = %s, fechaNacimiento = %s, sexo = %s, '
                            'estadoCivil = %s, calle1 = %s, numeroExterior1 = %s, '
                            'numeroInterior1 = %s, colonia1 = %s, codigoPostal1 = %s, '
                            'referencia1 = %s, calle2 = %s, numeroExterior2 = %s, '
                            'numeroInterior2 = %s, colonia2 = %s, codigoPostal2 = %s, '
                            'referencia2 = %s, calle3 = %s, numeroExterior3 = %s, '
                            'numeroInterior3 = %s, colonia3 = %s, codigoPostal3 = %s, '
                            'referencia3 = %s, correo = %s WHERE idCliente = %s', 
                            (body['nombre'].upper(), body['apellidoPaterno'].upper(),
                                body['apellidoMaterno'].upper(), body['fechaNacimiento'],
                                body['sexo'].upper(), body['estadoCivil'].upper(),
                                body['calle1'].upper(), body['numeroExterior1'],
                                body['numeroInterior1'], body['colonia1'].upper(),
                                body['codigoPostal1'], body['referencia1'].upper(),
                                body['calle2'].upper(), body['numeroExterior2'],
                                body['numeroInterior2'], body['colonia2'].upper(),
                                body['codigoPostal2'], body['referencia2'].upper(),
                                body['calle3'].upper(), body['numeroExterior3'],
                                body['numeroInterior3'], body['colonia3'].upper(),
                                body['codigoPostal3'], body['referencia3'].upper(), body['correo'],
                                id_cliente,))
            telefono = id_cliente
            if body['telefono'] != id_cliente and body['telefono'] != '':
                cursor.execute('UPDATE cliente SET idCliente = %s WHERE idCliente = %s',
                                (body['telefono'], id_cliente,))
                telefono = body['telefono']
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'El cliente {telefono} se ha actualizado exitosamente', 
                            'data': {'nombre': body['nombre'].upper(), 
                                    'apellidoPaterno': body['apellidoPaterno'].upper(), 
                                    'apellidoMaterno': body['apellidoMaterno'].upper(), 
                                    'fechaNacimiento': body['fechaNacimiento'], 
                                    'sexo': body['sexo'].upper(), 
                                    'estadoCivil': body['estadoCivil'].upper(), 
                                    'calle1': body['calle1'].upper(), 
                                    'numeroExterior1': body['numeroExterior1'], 
                                    'numeroInterior1': body['numeroInterior1'], 
                                    'colonia1': body['colonia1'].upper(), 
                                    'codigoPostal1': body['codigoPostal1'], 
                                    'referencia1': body['referencia1'].upper(), 
                                    'calle2': body['calle2'].upper(), 
                                    'numeroExterior2': body['numeroExterior2'], 
                                    'numeroInterior2': body['numeroInterior2'], 
                                    'colonia2': body['colonia2'].upper(), 
                                    'codigoPostal2': body['codigoPostal2'], 
                                    'referencia2': body['referencia2'].upper(),  
                                    'calle3': body['calle3'].upper(), 
                                    'numeroExterior3': body['numeroExterior3'], 
                                    'numeroInterior3': body['numeroInterior3'], 
                                    'colonia3': body['colonia3'].upper(), 
                                    'codigoPostal3': body['codigoPostal3'], 
                                    'referencia3': body['referencia3'].upper(),  
                                    'telefono': telefono, 
                                    'correo': body['correo']}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Cliente no encontrado', 
                                    'details': f'No se encontró el cliente {id_cliente} en la '
                                                f'base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * DELETE


def eliminar_cliente(id_cliente, cursor, conexion):
    """Función DELETE para eliminar un cliente específico o todos los clientes de la base de 
    datos"""
    try:
        cursor.execute(f'SELECT COUNT(idCliente) > 0 FROM cliente WHERE idCliente = {id_cliente}')
        if cursor.fetchone()[0]:
            # Se ejecuta una consulta SQL
            cursor.execute('DELETE FROM cliente WHERE idCliente = %s', (id_cliente,))
            conexion.connection.commit()
            # Se retorna un objeto JSON con un mensaje de éxito
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'El cliente {id_cliente} se ha dado de baja exitosamente'})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Cliente no encontrado', 
                                    'details': f'No se encontró el cliente {id_cliente} en la '
                                                f'base de datos'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * PATCH


def insertar_direccion_cliente(id_cliente, cursor, conexion):
    """Función PATCH para insertar una dirección a un cliente específico en la base de datos"""
    try:
        body = request.json
        cursor.execute(f'SELECT COUNT(idCliente) > 0 FROM cliente WHERE idCliente = {id_cliente}')
        if cursor.fetchone()[0]:
            if 'calle2' in body and body['calle2'] != '':
                cursor.execute('UPDATE cliente SET calle2 = %s, numeroExterior2 = %s, '
                                'numeroInterior2 = %s, colonia2 = %s, codigoPostal2 = %s, '
                                'referencia2 = %s WHERE idCliente = %s', 
                                (body['calle2'].upper(), body['numeroExterior2'],
                                    body['numeroInterior2'], body['colonia2'].upper(),
                                    body['codigoPostal2'], body['referencia2'].upper(),
                                    id_cliente,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'Se ha insertado la dirección 2 del cliente '
                                            f'{id_cliente} exitosamente',
                                'data': {'calle2': body['calle2'].upper(), 
                                            'numeroExterior2': body['numeroExterior2'],
                                            'numeroInterior2': body['numeroInterior2'], 
                                            'colonia2': body['colonia2'].upper(),
                                            'codigoPostal2': body['codigoPostal2'], 
                                            'referencia2': body['referencia2'].upper()}})
            if 'calle3' in body and body['calle3'] != '':
                cursor.execute('UPDATE cliente SET calle3 = %s, numeroExterior3 = %s, '
                                'numeroInterior3 = %s, colonia3 = %s, codigoPostal3 = %s, '
                                'referencia3 = %s WHERE idCliente = %s', 
                                (body['calle3'].upper(), body['numeroExterior3'],
                                    body['numeroInterior3'], body['colonia3'].upper(),
                                    body['codigoPostal3'], body['referencia3'].upper(),
                                    id_cliente,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'Se ha insertado la dirección 3 del cliente '
                                            f'{id_cliente} exitosamente',
                                'data': {'calle3': body['calle3'].upper(),
                                            'numeroExterior3': body['numeroExterior3'],
                                            'numeroInterior3': body['numeroInterior3'], 
                                            'colonia3': body['colonia3'].upper(),
                                            'codigoPostal3': body['codigoPostal3'], 
                                            'referencia3': body['referencia3'].upper()}})
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición inválida', 
                                        'details': 'Falta la clave y/o valor calle2 y/o calle3 en '
                                                    'el body de la petición'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Cliente no encontrado', 
                                    'details': f'No se encontró el cliente {id_cliente} en la '
                                                f'base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})


def eliminar_direccion_cliente(id_cliente, numero_direccion, cursor, conexion):
    """Función PATCH para eliminar una dirección de un cliente específico en la base de datos"""
    try:
        cursor.execute(f'SELECT COUNT(idCliente) > 0 FROM cliente WHERE idCliente = {id_cliente}')
        if cursor.fetchone()[0]:
            if numero_direccion == 2:
                cursor.execute('UPDATE cliente SET calle2 = NULL, numeroExterior2 = NULL, '
                                'numeroInterior2 = NULL, colonia2 = NULL, codigoPostal2 = NULL, '
                                'referencia2 = NULL WHERE idCliente = %s', (id_cliente,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'Se ha eliminado la dirección 2 del cliente '
                                            f'{id_cliente} exitosamente'})
            if numero_direccion == 3:
                cursor.execute('UPDATE cliente SET calle3 = NULL, numeroExterior3 = NULL, '
                                'numeroInterior3 = NULL, colonia3 = NULL, codigoPostal3 = NULL, '
                                'referencia3 = NULL WHERE idCliente = %s', (id_cliente,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'Se ha eliminado la dirección 3 del cliente '
                                            f'{id_cliente} exitosamente'})
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición inválida', 
                                        'details': 'El número de dirección debe ser 2 o 3'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Cliente no encontrado', 
                                    'details': f'No se encontró el cliente {id_cliente} en la '
                                                f'base de datos'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})


def actualizar_contrasenia_cliente(id_cliente, cursor, conexion):
    """Función PATCH para actualizar la contraseña de un cliente específico en la base de datos"""
    try:
        body = request.json
        cursor.execute(f'SELECT COUNT(idCliente) > 0 FROM cliente WHERE idCliente = {id_cliente}')
        if cursor.fetchone()[0]:
            if 'contrasenia' in body and body['contrasenia'] != '':
                cursor.execute('UPDATE cliente SET contrasenia = MD5(%s) WHERE idCliente = %s',
                                (body['contrasenia'], id_cliente,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'Se ha actualizado la contraseña del cliente '
                                            f'{id_cliente} exitosamente'})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición inválida', 
                                        'details': 'Falta la clave y/o valor contrasenia en el '
                                                    'body de la petición'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Cliente no encontrado', 
                                    'details': f'No se encontró el cliente {id_cliente} en la '
                                                f'base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * POST (Iniciar sesión)


def iniciar_sesion_cliente(cursor):
    """Función POST para iniciar sesión de un cliente"""
    try:
        body = request.json  # Se obtiene el body de la petición
        cursor.execute('SELECT COUNT(idCliente) > 0 FROM cliente WHERE correo = %s AND contrasenia '
                        '= MD5(%s)', (body['correo'], body['contrasenia']))
        if cursor.fetchone()[0]:
            return jsonify({'success': True, 'status': 200, 'message': 'Inicio de sesión exitoso'})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente',
                                    'message': 'Cliente no encontrado',
                                    'details': 'El cliente no existe o la contraseña es '
                                                'incorrecta'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente',
                                    'message': 'Petición inválida',
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor',
                                    'message': 'Error en la base de datos',
                                    'details': str(e)}})
