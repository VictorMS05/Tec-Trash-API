"""Vista que gestiona la lógica de los métodos HTTP para la tabla recoleccion de la base de datos"""

from datetime import datetime
# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA RECOLECCION

# *GET


def obtener_recoleccion(id_recoleccion, cursor):
    """Función GET para obtener una recolección específica o todas las recolecciones de la base de datos"""
    try:
        if id_recoleccion == 'todos':
            cursor.execute(
                'SELECT * FROM recoleccion')
        else:
            cursor.execute(
                'SELECT * FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
        recolecciones = cursor.fetchall()
        diccionario = []
        for registro in recolecciones:
            arreglo = {
                'idRecoleccion': registro[0],
                'idEmpleado': registro[1],
                'pesoFinal': registro[2],
                'costoFinal': registro[3],
                'fechaRegistro': registro[4],
                'fechaRecoleccion': registro[5]
            }
            diccionario.append(arreglo)
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * POST


def registrar_recoleccion(body, cursor, conexion):
    """Función POST para registrar una recolección en la base de datos"""
    try:
        cursor.execute('INSERT INTO recoleccion (idEmpleado, pesoFinal, costoFinal, fechaRegistro, fechaRecoleccion) VALUES (%s, %s, %s, CURRENT_TIMESTAMP(), NULL)',
                       (body['idEmpleado'].upper(), body['pesoFinal'], body['costoFinal']))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 201, 'message': 'La recolección se ha registrado exitosamente', 'data': {'idEmpleado': body['idEmpleado'].upper(), 'pesoFinal': body['pesoFinal'], 'costoFinal': body['costoFinal'], 'fechaRegistro': datetime.now()}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})

# * PUT


def actualizar_recoleccion(id_recoleccion, cursor, conexion):
    """Función PUT para actualizar una recolección específica en la base de datos"""
    try:
        body = request.json
        cursor.execute(
            'SELECT idRecoleccion FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
        if cursor.fetchone() is not None:
            cursor.execute('UPDATE recoleccion SET idEmpleado = %s, pesoFinal = %s, costoFinal = %s WHERE idRecoleccion = %s',
                           (body['idEmpleado'].upper(), body['pesoFinal'], body['costoFinal'], id_recoleccion,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 200, 'message': 'La recolección se ha actualizado exitosamente', 'data': {'idRecoleccion': id_recoleccion, 'idEmpleado': body['idEmpleado'].upper(), 'pesoFinal': body['pesoFinal'], 'costoFinal': body['costoFinal']}})
        else:
            # Se retorna un objeto JSON con un error 404
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Recoleccion no encontrada', 'details': f'No se encontró la recolección {id_recoleccion} en la base de datos'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})

# * DELETE


def eliminar_recoleccion(id_recoleccion, cursor, conexion):
    """Función DELETE para eliminar una recolección específica o todas las recolecciones de la base de datos"""
    try:
        cursor.execute(
            'SELECT idRecoleccion FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
        if cursor.fetchone() is not None:
            cursor.execute(
                'DELETE FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
            conexion.connection.commit()
            # Se retorna un objeto JSON con un mensaje de éxito
            return jsonify({'success': True, 'status': 200, 'message': f'La recolección {id_recoleccion} se ha eliminado exitosamente'})
        else:
            # Se retorna un objeto JSON con un error 404
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Recolección no encontrada', 'details': f'La recolección {id_recoleccion} no existe'}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})
