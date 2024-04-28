"""Vista que gestiona la lógica de los métodos HTTP para la tabla desecho de la base de datos"""

from datetime import datetime
# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA DESECHO

# * GET


def consultar_desecho(id_desecho, cursor):
    """Función GET para consultar un desecho específico o todos los desechos de la base de datos"""
    try:
        if id_desecho == 'todos':
            cursor.execute('SELECT * FROM desecho')
        else:
            cursor.execute('SELECT * FROM desecho WHERE idDesecho = %s', (id_desecho,))
        desechos = cursor.fetchall()
        diccionario = []
        for registro in desechos:
            arreglo = {
                'idDesecho': registro[0],
                'idCliente': registro[1],
                'idRecoleccion': registro[2],
                'idEntrega': registro[3],
                'nombre': registro[4],
                'modelo': registro[5],
                'marca': registro[6],
                'pesoEstimado': registro[7],
                'pesoReal': registro[8],
                'color': registro[9],
                'estatusFuncional': registro[10],
                'fechaRegistro': registro[11],
                'fechaActualizacion': registro[12],
                'pago': registro[13],
                'estatusRecoleccion': registro[14]
            }
            diccionario.append(arreglo)
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


def insertar_desecho(cursor, conexion):
    """Función POST para insertar un desecho en la base de datos"""
    try:
        body = request.json
        cursor.execute('INSERT INTO desecho (idCliente, nombre, modelo, marca, pesoEstimado, '
                        'fechaRegistro, estatusRecoleccion) VALUES (%s, %s, %s, %s, %s, '
                        'CURRENT_TIMESTAMP(), "SIN ASIGNAR")', (body['idCliente'],
                                                                body['nombre'].upper(),
                                                                body['modelo'].upper(),
                                                                body['marca'].upper(),
                                                                body['pesoEstimado']))
        conexion.connection.commit()
        return jsonify({'success': True,
                        'status': 201, 
                        'message': 'El desecho se ha registrado exitosamente', 
                        'data': {'idCliente': body['idCliente'],
                                    'nombre': body['nombre'].upper(), 
                                    'modelo': body['modelo'].upper(), 
                                    'marca': body['marca'].upper(), 
                                    'peso': body['pesoEstimado'], 
                                    'fechaRegistro': datetime.now(), 
                                    'estatusRecoleccion': 'SIN ASIGNAR'}})
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


def actualizar_desecho(id_desecho, cursor, conexion):
    """Función PUT para actualizar un desecho específico en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idDesecho) > 0 FROM desecho WHERE idDesecho = %s',
                        (id_desecho,))
        if cursor.fetchone()[0]:
            cursor.execute('UPDATE desecho SET idCliente = %s, nombre = %s, modelo = %s, '
                            'marca = %s, pesoEstimado = %s, pesoReal = %s, color = %s, '
                            'estatusFuncional = %s, fechaActualizacion = CURRENT_TIMESTAMP(), '
                            'pago = %s WHERE idDesecho = %s', (body['idCliente'],
                                                                body['nombre'].upper(),
                                                                body['modelo'].upper(),
                                                                body['marca'].upper(),
                                                                body['pesoEstimado'],
                                                                body['pesoReal'],
                                                                body['color'].upper(),
                                                                body['estatusFuncional'],
                                                                body['pago'], id_desecho,))
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'El desecho {id_desecho} se ha actualizado exitosamente', 
                            'data': {'idDesecho': id_desecho,
                                        'idCliente': body['idCliente'], 
                                        'nombre': body['nombre'].upper(), 
                                        'modelo': body['modelo'].upper(), 
                                        'marca': body['marca'].upper(), 
                                        'pesoEstablecido': body['pesoEstimado'],
                                        'pesoReal': body['pesoReal'],
                                        'color': body['color'].upper(), 
                                        'estatusFuncional': body['estatusFuncional'], 
                                        'pago': body['pago']}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Desecho no encontrado', 
                                    'details': f'No se encontró el desecho {id_desecho} en la base '
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


def eliminar_desecho(id_desecho, cursor, conexion):
    """Función DELETE para eliminar un desecho específico o todos los desechos de la base de 
    datos"""
    try:
        cursor.execute('SELECT COUNT(idDesecho) > 0 FROM desecho WHERE idDesecho = %s',
                        (id_desecho,))
        if cursor.fetchone()[0]:
            cursor.execute('DELETE FROM desecho WHERE idDesecho = %s', (id_desecho,))
            conexion.connection.commit()
            # Se retorna un objeto JSON con un mensaje de éxito
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'El desecho {id_desecho} se ha eliminado exitosamente'})
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Desecho no encontrado', 
                                    'details': f'No se encontró el desecho {id_desecho} en la base '
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


def completar_registro_desecho(id_desecho, cursor, conexion):
    """Función PATCH para completar los datos de un desecho específico durante una recolección en la 
    base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idDesecho) > 0 FROM desecho WHERE idDesecho = %s',
                        (id_desecho,))
        if cursor.fetchone()[0]:
            cursor.execute('UPDATE desecho SET pesoReal = %s, color = %s, estatusFuncional = %s, '
                            'fechaActualizacion = CURRENT_TIMESTAMP(), pago = %s WHERE '
                            'idDesecho = %s', (body['pesoReal'], body['color'].upper(),
                                                body['estatusFuncional'], body['pago'],
                                                id_desecho,))
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'Se ha completado el registro del desecho {id_desecho} '
                                        f'exitosamente',
                            'data': {'idDesecho': id_desecho,
                                        'pesoReal': body['pesoReal'], 
                                        'color': body['color'].upper(), 
                                        'estatusFuncional': body['estatusFuncional'],
                                        'fechaActualizacion': datetime.now(),
                                        'pago': body['pago']}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Desecho no encontrado', 
                                    'details': f'No se encontró el desecho {id_desecho} en la base '
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


def asignar_recoleccion_entrega_desecho(id_desecho, cursor, conexion):
    """Función PATCH para asignar un desecho específico a una recolección o entrega en la base de 
    datos"""
    try:
        body = request.json
        cursor.execute('SELECT idDesecho FROM desecho WHERE idDesecho = %s', (id_desecho,))
        if cursor.fetchone() is not None:
            if 'idRecoleccion' in body or 'estatusRecoleccion' in body:
                cursor.execute('UPDATE desecho SET idRecoleccion = %s, estatusRecoleccion = %s '
                                'WHERE idDesecho = %s', (body['idRecoleccion'],
                                                            body['estatusRecoleccion'],
                                                            id_desecho,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'El desecho {id_desecho} se ha asignado a una '
                                            'recolección exitosamente', 
                                'data': {'idDesecho': id_desecho,
                                            'idRecoleccion': body['idRecoleccion'], 
                                            'estatusRecoleccion': body['estatusRecoleccion']}})
            if 'idEntrega' in body:
                cursor.execute('UPDATE desecho SET idEntrega = %s WHERE idDesecho = %s',
                                (body['idEntrega'], id_desecho,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'El desecho {id_desecho} se ha asignado a una entrega '
                                            f'exitosamente',
                                'data': {'idDesecho': id_desecho,
                                            'idEntrega': body['idEntrega']}})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición inválida', 
                                        'details': 'No se especificó un campo válido para '
                                                    'actualizar el desecho'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Desecho no encontrado', 
                                    'details': f'No se encontró el desecho {id_desecho} en la base '
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
