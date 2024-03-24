from datetime import datetime
from flask import jsonify, request  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA RECOLECCION

#*GET
def obtener_recoleccion(id_recoleccion, cursor):
    """Función GET para obtener una recolección específica o todas las recolecciones de la base de datos"""
    try:
        if id_recoleccion == 'todos':
            cursor.execute(
            'SELECT * FROM recoleccion')
        else:
            cursor.execute('SELECT * FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
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
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}}) # Se retorna un objeto JSON con un error 500

#* POST
def registrar_recoleccion(body, cursor, conexion):
    """Función POST para registrar una recolección en la base de datos"""
    try:
        cursor.execute('INSERT INTO recoleccion (idEmpleado, pesoFinal, costoFinal, fechaRegistro, fechaRecoleccion) VALUES (%s, %s, %s, CURRENT_TIMESTAMP(), NULL)', (body['idEmpleado'].upper(), body['pesoFinal'], body['costoFinal']))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 201, 'message': 'La recolección se ha registrado exitosamente', 'data': {'idEmpleado': body['idEmpleado'].upper(), 'pesoFinal': body['pesoFinal'], 'costoFinal': body['costoFinal'], 'fechaRegistro': datetime.now()}})
    except IntegrityError as e:
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}}) # Se retorna un objeto JSON con un error 500

#* PUT
def actualizar_recoleccion(id_recoleccion, cursor, conexion):
    """Función PUT para actualizar una recolección específica en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT idRecoleccion FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
        if cursor.fetchone() is not None:
            cursor.execute('UPDATE recoleccion SET idEmpleado = %s, pesoFinal = %s, costoFinal = %s WHERE idRecoleccion = %s', (body['idEmpleado'].upper(), body['pesoFinal'], body['costoFinal'], id_recoleccion,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 200, 'message': 'La recolección se ha actualizado exitosamente', 'data': {'idRecoleccion': id_recoleccion, 'idEmpleado': body['idEmpleado'].upper(), 'pesoFinal': body['pesoFinal'], 'costoFinal': body['costoFinal']}})
        else:
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Recoleccion no encontrada', 'details': 'No se encontró la recolección en la base de datos'}}) # Se retorna un objeto JSON con un error 404
    except IntegrityError as e:
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}}) # Se retorna un objeto JSON con un error 500

#* DELETE
def eliminar_recoleccion(id_recoleccion, cursor, conexion):
    """Función DELETE para eliminar una recolección específica o todas las recolecciones de la base de datos"""
    try:
        cursor.execute('SELECT idRecoleccion FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
        if cursor.fetchone() is not None:
            cursor.execute('DELETE FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 200, 'message': f'La recolección {id_recoleccion} se ha eliminado exitosamente'})  # Se retorna un objeto JSON con un mensaje de éxito
        else:
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Recolección no encontrada', 'details': f'La recolección {id_recoleccion} no existe'}}) # Se retorna un objeto JSON con un error 404
    except OperationalError as e:
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}}) # Se retorna un objeto JSON con un error 500
