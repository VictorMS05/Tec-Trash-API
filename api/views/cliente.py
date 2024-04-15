"""Vista que gestiona la lógica de los métodos HTTP para la tabla cliente de la base de datos"""

# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA CLIENTE

# * GET


def obtener_clientes(id_cliente, cursor):
    """Función GET para obtener un cliente específico o todos los clientes de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_cliente == 'todos':  # Si no se recibe un id
            cursor.execute('SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, '
                            'fechaNacimiento, sexo, estadoCivil, calle, numeroExterior, '
                            'numeroInterior, colonia, codigoPostal, referencia, correo FROM '
                            'cliente')
        else:  # Si se recibe un id
            # Se ejecuta una consulta SQL con un parámetro
            cursor.execute(f'SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, '
                            f'fechaNacimiento, sexo, estadoCivil, calle, numeroExterior, '
                            f'numeroInterior, colonia, codigoPostal, referencia, correo FROM '
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


def registrar_cliente(cursor, conexion):
    """Función POST para registrar un cliente en la base de datos"""
    try:
        body = request.json  # Se obtiene el body de la petición
        # Se ejecuta una consulta SQL con parámetros
        cursor.execute('INSERT INTO cliente VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                        '%s, %s, %s, MD5(%s))', (body['telefono'], body['nombre'].upper(), 
                                                    body['apellidoPaterno'].upper(),
                                                    body['apellidoMaterno'].upper(),
                                                    body['fechaNacimiento'], body['sexo'].upper(),
                                                    body['estadoCivil'].upper(),
                                                    body['calle'].upper(), body['numeroExterior'],
                                                    body['numeroInterior'],
                                                    body['colonia'].upper(), body['codigoPostal'],
                                                    body['referencia'].upper(), body['correo'],
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
                                    'calle': body['calle'].upper(), 
                                    'numeroExterior': body['numeroExterior'], 
                                    'numeroInterior': body['numeroInterior'], 
                                    'colonia': body['colonia'].upper(), 
                                    'codigoPostal': body['codigoPostal'], 
                                    'referencia': body['referencia'].upper(), 
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
            cursor.execute('UPDATE cliente SET nombre = %s, apellidoPaterno = %s, apellidoMaterno '
                            '= %s, fechaNacimiento = %s, sexo = %s, estadoCivil = %s, calle = %s, '
                            'numeroExterior = %s, numeroInterior = %s, colonia = %s, codigoPostal '
                            '= %s, referencia = %s, correo = %s WHERE idCliente = %s', 
                            (body['nombre'].upper(), body['apellidoPaterno'].upper(),
                                body['apellidoMaterno'].upper(), body['fechaNacimiento'],
                                body['sexo'].upper(), body['estadoCivil'].upper(),
                                body['calle'].upper(), body['numeroExterior'],
                                body['numeroInterior'], body['colonia'].upper(),
                                body['codigoPostal'], body['referencia'].upper(), body['correo'],
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
                                        'calle': body['calle'].upper(), 
                                        'numeroExterior': body['numeroExterior'], 
                                        'numeroInterior': body['numeroInterior'], 
                                        'colonia': body['colonia'].upper(), 
                                        'codigoPostal': body['codigoPostal'], 
                                        'referencia': body['referencia'].upper(), 
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


def cambiar_contrasenia_cliente(id_cliente, cursor, conexion):
    """Función PATCH para cambiar la contraseña de un cliente específico en la base de datos"""
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
                                        'details': 'Falta la clave y/o valor contrasenia en el body de la '
                                                    'petición'}})
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
