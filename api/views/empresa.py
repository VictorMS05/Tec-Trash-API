"""Vista que gestiona la lógica de los métodos HTTP para la tabla empresa de la base de datos"""

# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA EMPRESA

# *GET


def consultar_empresa(id_empresa, cursor):
    """Función GET para consultar una empresa específica o todas las empresas de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_empresa == 'todos':
            cursor.execute('SELECT idEmpresa, nombre, calle, numeroExterior, numeroInterior, '
                            'colonia, codigoPostal, ciudad, estado, referencia, telefono, correo, '
                            'nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, '
                            'pesoEstablecido FROM empresa')
        else:
            cursor.execute('SELECT idEmpresa, nombre, calle, numeroExterior, numeroInterior, '
                            'colonia, codigoPostal, ciudad, estado, referencia, telefono, correo, '
                            'nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, '
                            'pesoEstablecido FROM empresa WHERE idEmpresa = %s', (id_empresa,))
        empresas = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in empresas:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idEmpresa': registro[0],
                'nombre': registro[1],
                'calle': registro[2],
                'numeroExterior': registro[3],
                'numeroInterior': registro[4],
                'colonia': registro[5],
                'codigoPostal': registro[6],
                'ciudad': registro[7],
                'estado': registro[8],
                'referencia': registro[9],
                'telefono': registro[10],
                'correo': registro[11],
                'nombreEncargado': registro[12],
                'apellidoPaternoE': registro[13],
                'apellidoMaternoE': registro[14],
                'esEntrega': registro[15],
                'pesoEstablecido': registro[16]
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


def insertar_empresa(cursor, conexion):
    """Función POST para insertar una empresa en la base de datos"""
    try:
        body = request.json  # Se obtiene el cuerpo de la petición
        # Se ejecuta una consulta SQL con parámetros
        cursor.execute('INSERT INTO empresa VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                        '%s, MD5(%s), %s, %s, %s, %s, %s)', (body['rfc'].upper(),
                                                            body['nombre'].upper(),
                                                            body['calle'].upper(),
                                                            body['numeroExterior'],
                                                            body['numeroInterior'],
                                                            body['colonia'].upper(),
                                                            body['codigoPostal'],
                                                            body['ciudad'].upper(),
                                                            body['estado'].upper(),
                                                            body['referencia'].upper(),
                                                            body['telefono'],
                                                            body['correo'],
                                                            body['contrasenia'],
                                                            body['nombreEncargado'].upper(),
                                                            body['apellidoPaternoE'].upper(),
                                                            body['apellidoMaternoE'].upper(),
                                                            body['esEntrega'],
                                                            body['pesoEstablecido']))
        conexion.connection.commit()  # Se confirma la transacción
        # Se retorna un objeto JSON con un mensaje de éxito
        return jsonify({'success': True,
                        'status': 201, 
                        'message': 'La empresa se ha registrado exitosamente', 
                        'data': {'rfc': body['rfc'].upper(), 
                                'nombre': body['nombre'].upper(), 
                                'calle': body['calle'].upper(), 
                                'numeroExterior': body['numeroExterior'], 
                                'numeroInterior': body['numeroInterior'],
                                'colonia': body['colonia'].upper(), 
                                'codigoPostal': body['codigoPostal'],
                                'ciudad': body['ciudad'].upper(), 
                                'estado': body['estado'].upper(), 
                                'referencia': body['referencia'].upper(),
                                'telefono': body['telefono'], 
                                'correo': body['correo'], 
                                'nombreEncargado': body['nombreEncargado'].upper(), 
                                'apellidoPaternoE': body['apellidoPaternoE'].upper(), 
                                'apellidoMaternoE': body['apellidoMaternoE'].upper(), 
                                'esEntrega': body['esEntrega'], 
                                'pesoEstablecido': body['pesoEstablecido']}})
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


def actualizar_empresa(id_empresa, cursor, conexion):
    """Función PUT para actualizar una empresa específica en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idEmpresa) > 0 FROM empresa WHERE idEmpresa = %s',
                        (id_empresa,))
        if cursor.fetchone()[0]:
            cursor.execute('UPDATE empresa SET nombre = %s, calle = %s, numeroExterior = %s, '
                            'numeroInterior = %s, colonia = %s, codigoPostal = %s, ciudad = %s, '
                            'estado = %s, referencia = %s, telefono = %s, correo = %s, '
                            'nombreEncargado = %s, apellidoPaternoE = %s, apellidoMaternoE = %s, '
                            'esEntrega = %s, pesoEstablecido = %s WHERE idEmpresa = %s',
                            (body['nombre'].upper(), body['calle'].upper(), body['numeroExterior'],
                                body['numeroInterior'], body['colonia'].upper(),
                                body['codigoPostal'], body['ciudad'].upper(),
                                body['estado'].upper(), body['referencia'].upper(),
                                body['telefono'], body['correo'], body['nombreEncargado'].upper(),
                                body['apellidoPaternoE'].upper(), body['apellidoMaternoE'].upper(),
                                body['esEntrega'], body['pesoEstablecido'], id_empresa,))
            rfc = id_empresa
            if body['rfc'] != id_empresa and body['rfc'] != '':
                cursor.execute('UPDATE empresa SET rfc = %s WHERE idEmpresa = %s',
                                (body['rfc'], id_empresa,))
                rfc = body['rfc']
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'La empresa {id_empresa} se ha actualizado exitosamente', 
                            'data': {'rfc': rfc,
                                        'nombre': body['nombre'].upper(),
                                        'calle': body['calle'].upper(),
                                        'numeroExterior': body['numeroExterior'],
                                        'numeroInterior': body['numeroInterior'],
                                        'colonia': body['colonia'].upper(),
                                        'codigoPostal': body['codigoPostal'],
                                        'ciudad': body['ciudad'].upper(),
                                        'estado': body['estado'].upper(),
                                        'referencia': body['referencia'].upper(),
                                        'telefono': body['telefono'],
                                        'correo': body['correo'],
                                        'nombreEncargado': body['nombreEncargado'].upper(),
                                        'apellidoPaternoE': body['apellidoPaternoE'].upper(),
                                        'apellidoMaternoE': body['apellidoMaternoE'].upper(),
                                        'esEntrega': body['esEntrega'],
                                        'pesoEstablecido': body['pesoEstablecido']}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empresa no encontrada', 
                                    'details': f'No se encontró la empresa {id_empresa} en la base '
                                                f'de datos'}})
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


def eliminar_empresa(id_empresa, cursor, conexion):
    """Función DELETE para eliminar una empresa específica o todas las empresas de la base de 
    datos"""
    try:
        cursor.execute('SELECT COUNT(idEmpresa) > 0 FROM empresa WHERE idEmpresa = %s',
                        (id_empresa,))
        if cursor.fetchone()[0]:
            # Se ejecuta una consulta SQL
            cursor.execute('DELETE FROM empresa WHERE idEmpresa = %s', (id_empresa,))
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'La empresa {id_empresa} se ha eliminado exitosamente'})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empresa no encontrada', 
                                    'details': f'No se encontró la empresa {id_empresa} en la base '
                                                f'de datos'}})
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


def actualizar_contrasenia_empresa(id_empresa, cursor, conexion):
    """Función PATCH para actualizar la contraseña de una empresa específica en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idEmpresa) > 0 FROM empresa WHERE idEmpresa = %s',
                        (id_empresa,))
        if cursor.fetchone()[0]:
            if 'contrasenia' in body and body['contrasenia'] != '':
                cursor.execute('UPDATE empresa SET contrasenia = MD5(%s) WHERE idEmpresa = %s',
                                (body['contrasenia'], id_empresa,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'Se ha actualizado la contraseña de la empresa '
                                            f'{id_empresa} exitosamente'})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición incorrecta', 
                                        'details': 'Falta la clave y/o valor contrasenia en el '
                                                    'body de la petición'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empresa no encontrada', 
                                    'details': f'No se encontró la empresa {id_empresa} en la base '
                                                f'de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el '
                                                f'body de la petición'}})
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


def iniciar_sesion_empresa(cursor):
    """Función POST para iniciar sesión de una empresa en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idEmpresa) > 0 FROM empresa WHERE correo = %s '
                        'AND contrasenia = MD5(%s)', (body['correo'], body['contrasenia'],))
        if cursor.fetchone()[0]:
            cursor.execute('SELECT idEmpresa, nombre FROM empresa WHERE correo = %s',
                            (body['correo'],))
            return jsonify({'success': True,
                            'status': 200,
                            'message': 'Inicio de sesión exitoso',
                            'data': cursor.fetchone()[0]})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empresa no encontrada', 
                                    'details': 'No se encontró la empresa en la base de datos'}})
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
