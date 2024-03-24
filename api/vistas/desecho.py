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
                'SELECT idDesecho, idCliente, idRecoleccion, idEntrega, nombre, modelo, marca, peso, color, estatusFuncional, fechaRegistro, fechaFinal, pago, estatusRecoleccion, estatusEntrega FROM desecho')
        else:
            cursor.execute('SELECT idDesecho, idRecoleccion, idEntrega, nombre, modelo, marca peso, color, estatusFuncional, fechaRegistro, fechaFinal, pago, estatusRecoleccion, estatusEntrega FROM desecho WHERE idDesecho = %s', (id_desecho,))
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
                'fechaFinal': registro[11],
                'pago': registro[12],
                'estatusRecoleccion': registro[13],
                'estatusEntrega': registro[14]
            }
            diccionario.append(arreglo)
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * POST


def registrar_desecho(body, cursor, conexion):
    """Función POST para registrar un desecho en la base de datos"""
    try:
        cursor.execute('INSERT INTO desecho (idCliente, idRecoleccion, idEntrega, nombre, modelo, marca, peso, color, estatusFuncional, fechaRegistro, pago, estatusRecoleccion, estatusEntrega) VALUES (%s, NULL, NULL, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), %s, "NO RECOLECTADO", "NO ENTREGADO")',
                       (body['idCliente'], body['nombre'].upper(), body['modelo'].upper(), body['marca'].upper(), body['peso'], body['color'].upper(), body['estatusFuncional'], body['pago']))
        conexion.connection.commit()
        cursor.execute('SELECT * FROM desecho WHERE idCliente = %s AND nombre = %s AND modelo = %s AND marca = %s AND peso = %s AND color = %s AND estatusFuncional = %s AND pago = %s',
                       (body['idCliente'], body['nombre'].upper(), body['modelo'].upper(), body['marca'].upper(), body['peso'], body['color'].upper(), body['estatusFuncional'], body['pago']))
        return jsonify({'success': True, 'status': 201, 'message': 'El desecho se ha registrado exitosamente', 'data': {'idCliente': body['idCliente'], 'nombre': body['nombre'].upper(), 'modelo': body['modelo'].upper(), 'marca': body['marca'].upper(), 'peso': body['peso'], 'color': body['color'].upper(), 'estatusFuncional': body['estatusFuncional'], 'fechaRegistro': datetime.now(), 'pago': body['pago'], 'estatusRecoleccion': 'NO RECOLECTADO', 'estatusEntrega': 'NO ENTREGADO'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})

# * PUT


def actualizar_desecho(id_desecho, cursor, conexion):
    """Función PUT para actualizar un desecho específico en la base de datos"""
    try:
        desecho = request.json
        cursor.execute(
            'SELECT idDesecho FROM desecho WHERE idDesecho = %s', (id_desecho,))
        if cursor.fetchone() is not None:
            cursor.execute('UPDATE desecho SET idCliente = %s, nombre = %s, modelo = %s, marca = %s, peso = %s, color = %s, estatusFuncional = %s, pago = %s WHERE idDesecho = %s', (
                desecho['idCliente'], desecho['nombre'].upper(), desecho['modelo'].upper(), desecho['marca'].upper(), desecho['peso'], desecho['color'].upper(), desecho['estatusFuncional'], desecho['pago'], id_desecho,))
            conexion.connection.commit()
            cursor.execute(
                'SELECT idCliente, nombre, modelo, marca, peso, color, estatusFuncional, pago FROM desecho WHERE idDesecho = %s', (id_desecho,))
            return jsonify({'success': True, 'status': 200, 'message': 'El desecho se ha actualizado exitosamente', 'data': {'idCliente': desecho['idCliente'], 'nombre': desecho['nombre'].upper(), 'modelo': desecho['modelo'].upper(), 'marca': desecho['marca'].upper(), 'peso': desecho['peso'], 'color': desecho['color'].upper(), 'estatusFuncional': desecho['estatusFuncional'], 'pago': desecho['pago']}})
        else:
            # Se retorna un objeto JSON con un error 404
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Desecho no encontrado', 'details': f'No se encontró el desecho {id_desecho} en la base de datos'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})

# * DELETE


def eliminar_desecho(id_desecho, cursor, conexion):
    """Función DELETE para eliminar un desecho específico o todos los desechos de la base de datos"""
    try:
        cursor.execute(
            'SELECT idDesecho FROM desecho WHERE idDesecho = %s', (id_desecho,))
        if cursor.fetchone() is not None:
            cursor.execute(
                'DELETE FROM desecho WHERE idDesecho = %s', (id_desecho,))
            conexion.connection.commit()
            # Se retorna un objeto JSON con un mensaje de éxito
            return jsonify({'success': True, 'status': 200, 'message': f'El desecho {id_desecho} se ha eliminado exitosamente'})
        else:
            # Se retorna un objeto JSON con un error 404
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Desecho no encontrado', 'details': f'El desecho {id_desecho} no existe'}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})
