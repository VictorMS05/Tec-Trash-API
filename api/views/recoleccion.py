"""Vista que gestiona la lógica de los métodos HTTP para la tabla recoleccion de la base de datos"""

from datetime import datetime
# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA RECOLECCION

# *GET


def consultar_recoleccion(id_recoleccion, cursor):
    """Función GET para consultar una recolección específica o todas las recolecciones de la base de 
    datos"""
    try:
        if id_recoleccion == 'todos':
            cursor.execute('SELECT * FROM recoleccion')
        else:
            cursor.execute(f'SELECT * FROM recoleccion WHERE idRecoleccion = {id_recoleccion}')
        recolecciones = cursor.fetchall()
        diccionario = []
        for registro in recolecciones:
            arreglo = {
                'idRecoleccion': registro[0],
                'idEmpleado': registro[1],
                'pesoFinal': registro[2],
                'costoFinal': registro[3],
                'estatus': registro[4],
                'fechaRegistro': registro[5],
                'fechaProgramada': registro[6],
                'fechaRecoleccion': registro[7]
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


def insertar_recoleccion(cursor, conexion):
    """Función POST para insertar una recolección en la base de datos"""
    try:
        body = request.json
        cursor.execute('INSERT INTO recoleccion (idEmpleado, pesoFinal, costoFinal, estatus, '
                        'fechaRegistro, fechaProgramada) VALUES (%s, %s, %s, "PROGRAMADA", '
                        'CURRENT_TIMESTAMP(), %s)', (body['idEmpleado'].upper(), body['pesoFinal'],
                                                        body['costoFinal'],
                                                        body['fechaProgramada']))
        conexion.connection.commit()
        return jsonify({'success': True,
                        'status': 201, 
                        'message': 'La recolección se ha registrado exitosamente', 
                        'data': {'idEmpleado': body['idEmpleado'].upper(),
                                    'pesoFinal': body['pesoFinal'], 
                                    'costoFinal': body['costoFinal'], 
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

# * PUT


def actualizar_recoleccion(id_recoleccion, cursor, conexion):
    """Función PUT para actualizar una recolección específica en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idRecoleccion) > 0 FROM recoleccion WHERE idRecoleccion = %s',
                        (id_recoleccion,))
        if cursor.fetchone()[0]:
            cursor.execute('UPDATE recoleccion SET idEmpleado = %s, pesoFinal = %s, '
                            'costoFinal = %s WHERE idRecoleccion = %s', (body['idEmpleado'].upper(),
                                                                            body['pesoFinal'],
                                                                            body['costoFinal'],
                                                                            id_recoleccion,))
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'La recolección {id_recoleccion} se ha actualizado '
                                        f'exitosamente',
                            'data': {'idRecoleccion': id_recoleccion,
                                        'idEmpleado': body['idEmpleado'].upper(), 
                                        'pesoFinal': body['pesoFinal'], 
                                        'costoFinal': body['costoFinal']}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Recoleccion no encontrada', 
                                    'details': f'No se encontró la recolección {id_recoleccion} en '
                                                f'la base de datos'}})
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


def eliminar_recoleccion(id_recoleccion, cursor, conexion):
    """Función DELETE para eliminar una recolección específica o todas las recolecciones de la base 
    de datos"""
    try:
        cursor.execute('SELECT COUNT(idRecoleccion) > 0 FROM recoleccion WHERE idRecoleccion = %s',
                        (id_recoleccion,))
        if cursor.fetchone()[0]:
            cursor.execute('DELETE FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
            conexion.connection.commit()
            # Se retorna un objeto JSON con un mensaje de éxito
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'La recolección {id_recoleccion} se ha eliminado '
                                        f'exitosamente'})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Recolección no encontrada', 
                                    'details': f'La recolección {id_recoleccion} no existe'}})
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


def finalizar_recoleccion(id_recoleccion, cursor, conexion):
    """Función PATCH para finalizar una recolección específica en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idRecoleccion) FROM recoleccion WHERE idRecoleccion = %s',
                        (id_recoleccion,))
        if cursor.fetchone()[0]:
            if 'estatus' in body:
                cursor.execute('SELECT fechaRecoleccion FROM recoleccion WHERE idRecoleccion = %s',
                                (id_recoleccion,))
                fecha_recoleccion = cursor.fetchone()[0]
                if body['estatus'].upper() == 'EN PROCESO' and fecha_recoleccion is None:
                    cursor.execute('UPDATE recoleccion SET estatus = %s WHERE idRecoleccion = %s',
                                    (body['estatus'].upper(), id_recoleccion,))
                    conexion.connection.commit()
                    return jsonify({'success': True,
                                    'status': 200, 
                                    'message': f'La recolección {id_recoleccion} ha comenzado '
                                                f'exitosamente',
                                    'data': {'idRecoleccion': id_recoleccion,
                                                'estatus': body['estatus'].upper()}})
                if body['estatus'].upper() == 'EN PROCESO' and fecha_recoleccion is not None:
                    return jsonify({'error': {'code': 400,
                                                'type': 'Error del cliente', 
                                                'message': 'Recoleccion ya realizada', 
                                                'details': f'La recolección {id_recoleccion} ya '
                                                            f'fue realizada el '
                                                            f'{fecha_recoleccion}'}})
                if body['estatus'].upper() == 'REALIZADA' and fecha_recoleccion is None:
                    cursor.execute('UPDATE recoleccion SET estatus = %s, '
                                    'fechaRecoleccion = CURRENT_TIMESTAMP() WHERE idRecoleccion = '
                                    '%s', (body['estatus'].upper(), id_recoleccion,))
                    conexion.connection.commit()
                    return jsonify({'success': True,
                                    'status': 200, 
                                    'message': f'La recolección {id_recoleccion} ha finalizado '
                                                f'exitosamente',
                                    'data': {'idRecoleccion': id_recoleccion,
                                                'estatus': body['estatus'].upper(), 
                                                'fechaRecoleccion': datetime.now()}})
                if body['estatus'].upper() == 'REALIZADA' and fecha_recoleccion is not None:
                    return jsonify({'error': {'code': 400,
                                                'type': 'Error del cliente', 
                                                'message': 'Recoleccion ya realizada', 
                                                'details': f'La recolección {id_recoleccion} ya '
                                                            f'fue realizada el '
                                                            f'{fecha_recoleccion[0]}'}})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición inválida', 
                                        'details': 'Falta la clave y/o atributo estatus en el body '
                                                    'de la petición'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Recoleccion no encontrada', 
                                    'details': f'No se encontró la recolección {id_recoleccion} en '
                                                f'la base de datos'}})
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
