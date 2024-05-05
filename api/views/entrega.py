"""Vista que gestiona la lógica de los métodos HTTP para la tabla entrega de la base de datos"""

from datetime import datetime
# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA ENTREGA

# * GET


def consultar_entrega(id_entrega, cursor):
    """Función GET para consultar una entrega específica o todas las entregas de la base de datos"""
    try:
        if id_entrega == 'todos':
            cursor.execute('SELECT * FROM entrega')
        else:
            cursor.execute('SELECT * FROM entrega WHERE idEntrega = %s', (id_entrega,))
        entregas = cursor.fetchall()
        diccionario = []
        for registro in entregas:
            arreglo = {
                'idEntrega': registro[0],
                'idEmpresa': registro[1],
                'idEmpleado': registro[2],
                'pesoFinal': registro[3],
                'costo': registro[4],
                'estatus': registro[5],
                'fechaRegistro': registro[6],
                'fechaProgramada': registro[7],
                'fechaEntrega': registro[8]
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


def insertar_entrega(cursor, conexion):
    """Función POST para insertar una entrega en la base de datos"""
    try:
        body = request.json
        cursor.execute('INSERT INTO entrega (idEmpresa, idEmpleado, pesoFinal, costo, estatus, '
                        'fechaRegistro, fechaProgramada) VALUES (%s, %s, %s, %s, "PROGRAMADA", '
                        'CURRENT_TIMESTAMP(), %s)', (body['idEmpresa'].upper(),
                                                        body['idEmpleado'].upper(),
                                                        body['pesoFinal'], body['costo'],
                                                        body['fechaProgramada']))
        conexion.connection.commit()
        return jsonify({'success': True,
                        'status': 201, 
                        'message': 'La entrega se ha registrado exitosamente', 
                        'data': {'idEmpresa': body['idEmpresa'].upper(),
                                    'idEmpleado': body['idEmpleado'].upper(), 
                                    'pesoFinal': body['pesoFinal'], 
                                    'costo': body['costo'], 
                                    'estatus': 'PROGRAMADA', 
                                    'fechaRegistro': datetime.now(), 
                                    'fechaProgramada': body['fechaProgramada']}})
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

# *PUT


def actualizar_entrega(id_entrega, cursor, conexion):
    """Función PUT para actualizar una entrega específica en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idEmpresa) > 0 FROM entrega WHERE idEntrega = %s',
                        (id_entrega,))
        if cursor.fetchone()[0]:
            cursor.execute('UPDATE entrega SET idEmpresa = %s, idEmpleado = %s, pesoFinal = %s, '
                            'costo = %s WHERE idEntrega = %s', (body['idEmpresa'].upper(),
                                                                body['idEmpleado'].upper(),
                                                                body['pesoFinal'], body['costo'],
                                                                body['estatus'],
                                                                body['fechaRegistro'],
                                                                body['fechaProgramada'],
                                                                body['fechaEntrega'], id_entrega,))
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 201, 
                            'message': f'La entrega {id_entrega} se ha actualizado exitosamente', 
                            'data': {'idEntrega': id_entrega,
                                        'idEmpresa': body['idEmpresa'].upper(),
                                        'idEmpleado': body['idEmpleado'].upper(), 
                                        'pesoFinal': body['pesoFinal'], 
                                        'costo': body['costo']}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Entrega no encontrada', 
                                    'details': f'No se encontró la entrega {id_entrega} en la base '
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


def eliminar_entrega(id_entrega, cursor, conexion):
    """Función DELETE para eliminar una entrega específico o todos las entregas de la base de 
    datos"""
    try:
        cursor.execute('SELECT COUNT(idEntrega) > 0 FROM entrega WHERE idEntrega = %s',
                        (id_entrega,))
        if cursor.fetchone()[0]:
            # Se ejecuta una consulta SQL
            cursor.execute('DELETE FROM entrega WHERE idEntrega = %s', (id_entrega,))
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'La entrega {id_entrega} ha sido eliminada exitosamente'})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Entrega no encontrada', 
                                    'details': f'No se encontró la entrega {id_entrega} en la base '
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


def finalizar_entrega(id_entrega, cursor, conexion):
    """Función PATCH para finalizar una entrega específica en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idEntrega) > 0 FROM entrega WHERE idEntrega = %s',
                        (id_entrega,))
        if cursor.fetchone()[0]:
            if 'estatus' in body:
                cursor.execute('SELECT fechaEntrega FROM entrega WHERE idEntrega = %s',
                                (id_entrega,))
                fecha_entrega = cursor.fetchone()[0]
                if body['estatus'].upper() == 'EN PROCESO' and fecha_entrega is None:
                    cursor.execute('UPDATE entrega SET estatus = %s WHERE idEntrega = %s',
                                    (body['estatus'].upper(), id_entrega,))
                    conexion.connection.commit()
                    return jsonify({'success': True,
                                    'status': 200, 
                                    'message': f'La entrega {id_entrega} ha comenzado '
                                                f'exitosamente',
                                    'data': {'idEntrega': id_entrega,
                                                'estatus': body['estatus'].upper()}})
                if body['estatus'].upper() == 'EN PROCESO' and fecha_entrega is not None:
                    return jsonify({'error': {'code': 400,
                                                'type': 'Error del cliente',
                                                'message': 'Entrega ya realizada',
                                                'details': f'La entrega {id_entrega} ya fue '
                                                            f'realizada el {fecha_entrega}'}})
                if body['estatus'].upper() == 'REALIZADA' and fecha_entrega is None:
                    cursor.execute('UPDATE entrega SET estatus = %s, fechaEntrega = '
                                    'CURRENT_TIMESTAMP() WHERE idEntrega = %s',
                                    (body['estatus'].upper(), id_entrega,))
                    conexion.connection.commit()
                    return jsonify({'success': True,
                                    'status': 200,
                                    'message': f'La entrega {id_entrega} ha finalizado '
                                                f'exitosamente',
                                    'data': {'idEntrega': id_entrega,
                                                'estatus': body['estatus'].upper(),
                                                'fechaEntrega': datetime.now()}})
                if body['estatus'].upper() == 'REALIZADA' and fecha_entrega is not None:
                    return jsonify({'error': {'code': 400,
                                                'type': 'Error del cliente', 
                                                'message': 'Entrega ya realizada', 
                                                'details': f'La entrega {id_entrega} ya fue '
                                                            f'realizada el '
                                                            f'{fecha_entrega[0]}'}})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición inválida', 
                                        'details': 'Falta la clave estatus en el body de la '
                                                    'petición'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Entrega no encontrada', 
                                    'details': f'No se encontró la entrega {id_entrega} en la '
                                                f'base de datos'}})
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
