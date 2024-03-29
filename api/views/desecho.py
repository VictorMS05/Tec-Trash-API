"""Vista que gestiona la lógica de los métodos HTTP para la tabla desecho de la base de datos"""

from datetime import datetime
# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA DESECHO

# * GET


def obtener_desecho(id_desecho, cursor):
    """Función GET para obtener un desecho específico o todos los desechos de la base de datos"""
    try:
        if id_desecho == 'todos':
            cursor.execute(
                'SELECT * FROM desecho')
        else:
            cursor.execute(
                f'SELECT * FROM desecho WHERE idDesecho = {id_desecho}')
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
                'peso': registro[7],
                'color': registro[8],
                'estatusFuncional': registro[9],
                'fechaRegistro': registro[10],
                'pago': registro[11],
                'estatusRecoleccion': registro[12]
            }
            diccionario.append(arreglo)
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * POST


def registrar_desecho(cursor, conexion):
    """Función POST para registrar un desecho en la base de datos"""
    try:
        body = request.json
        cursor.execute('INSERT INTO desecho (idCliente, idRecoleccion, idEntrega, nombre, modelo, marca, peso, color, estatusFuncional, fechaRegistro, pago, estatusRecoleccion) VALUES (%s, NULL, NULL, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), %s, "SIN ASIGNAR")', (body['idCliente'], body['nombre'].upper(), body['modelo'].upper(), body['marca'].upper(), body['peso'], body['color'].upper(), body['estatusFuncional'], body['pago']))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 201, 'message': 'El desecho se ha registrado exitosamente', 'data': {'idCliente': body['idCliente'], 'nombre': body['nombre'].upper(), 'modelo': body['modelo'].upper(), 'marca': body['marca'].upper(), 'peso': body['peso'], 'color': body['color'].upper(), 'estatusFuncional': body['estatusFuncional'], 'fechaRegistro': datetime.now(), 'pago': body['pago']}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Petición inválida', 'details': f'Falta la clave {str(e)} en el body de la petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * PUT


def actualizar_desecho(id_desecho, cursor, conexion):
    """Función PUT para actualizar un desecho específico en la base de datos"""
    try:
        body = request.json
        cursor.execute(
            f'SELECT idDesecho FROM desecho WHERE idDesecho = {id_desecho}')
        if cursor.fetchone() is not None:
            cursor.execute('UPDATE desecho SET idCliente = %s, nombre = %s, modelo = %s, marca = %s, peso = %s, color = %s, estatusFuncional = %s, pago = %s WHERE idDesecho = %s', (body['idCliente'], body['nombre'].upper(), body['modelo'].upper(), body['marca'].upper(), body['peso'], body['color'].upper(), body['estatusFuncional'], body['pago'], id_desecho,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 200, 'message': 'El desecho se ha actualizado exitosamente', 'data': {'idDesecho': id_desecho, 'idCliente': body['idCliente'], 'nombre': body['nombre'].upper(), 'modelo': body['modelo'].upper(), 'marca': body['marca'].upper(), 'peso': body['peso'], 'color': body['color'].upper(), 'estatusFuncional': body['estatusFuncional'], 'pago': body['pago']}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Desecho no encontrado', 'details': f'No se encontró el desecho {id_desecho} en la base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Petición inválida', 'details': f'Falta la clave {str(e)} en el body de la petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * DELETE


def eliminar_desecho(id_desecho, cursor, conexion):
    """Función DELETE para eliminar un desecho específico o todos los desechos de la base de datos"""
    try:
        cursor.execute(
            f'SELECT idDesecho FROM desecho WHERE idDesecho = {id_desecho}')
        if cursor.fetchone() is not None:
            cursor.execute(
                f'DELETE FROM desecho WHERE idDesecho = {id_desecho}')
            conexion.connection.commit()
            # Se retorna un objeto JSON con un mensaje de éxito
            return jsonify({'success': True, 'status': 200, 'message': f'El desecho {id_desecho} se ha eliminado exitosamente'})
        return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Desecho no encontrado', 'details': f'El desecho {id_desecho} no existe'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * PATCH


def asignar_recoleccion_entrega_desecho(id_desecho, cursor, conexion):
    """Función PATCH para asignar un desecho específico a una recolección o entrega en la base de datos"""
    try:
        body = request.json
        cursor.execute(
            f'SELECT idDesecho FROM desecho WHERE idDesecho = {id_desecho}')
        if cursor.fetchone() is not None:
            if 'idRecoleccion' in body or 'estatusRecoleccion' in body:
                cursor.execute('UPDATE desecho SET idRecoleccion = %s, estatusRecoleccion = %s WHERE idDesecho = %s', (body['idRecoleccion'], body['estatusRecoleccion'], id_desecho,))
                conexion.connection.commit()
                return jsonify({'success': True, 'status': 200, 'message': 'El desecho se ha asignado a una recolección exitosamente', 'data': {'idDesecho': id_desecho, 'idRecoleccion': body['idRecoleccion'], 'estatusRecoleccion': body['estatusRecoleccion']}})
            if 'idEntrega' in body:
                cursor.execute('UPDATE desecho SET idEntrega = %s WHERE idDesecho = %s', (body['idEntrega'], id_desecho,))
                conexion.connection.commit()
                return jsonify({'success': True, 'status': 200, 'message': 'El desecho se ha asignado a una entrega exitosamente', 'data': {'idDesecho': id_desecho, 'idEntrega': body['idEntrega']}})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Petición inválida', 'details': 'No se especificó un campo válido para actualizar el desecho'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Desecho no encontrado', 'details': f'No se encontró el desecho {id_desecho} en la base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Petición inválida', 'details': f'Falta la clave {str(e)} en el body de la petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})
