from flask import jsonify, request  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA ENTREGA

#* GET
def obtener_entrega(id_entrega, cursor):
    """Función GET para obtener una entrega específica o todas las entregas de la base de datos"""
    try:
        if id_entrega == 'todos':
            cursor.execute(
            'SELECT idEntrega, idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega FROM entrega')
        else:
            cursor.execute('SELECT idEntrega, idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega FROM entrega WHERE idEntrega = %s', (id_entrega,))
        entregas = cursor.fetchall()
        diccionario = []
        for registro in entregas:
            arreglo = {
                'idEntrega': registro[0],
                'idEmpresa': registro[1],
                'idEmpleado': registro[2],
                'pesoFinal': registro[3],
                'costo': registro[4],
                'fechaRegistro': registro[5],
                'fechaEntrega': registro[6]
            }
            diccionario.append(arreglo)
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* POST
def registrar_entrega(body, cursor, conexion):
    """Función POST para registrar una entrega en la base de datos"""
    try:
        cursor.execute('INSERT INTO entrega (idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP(), NULL)', (body['idEmpresa'].upper(), body['idEmpleado'].upper(), body['pesoFinal'], body['costo']))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 201, 'message': 'Registro exitoso'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500
    
#*PUT
def actualizar_entrega(id_entrega, cursor, conexion):
    try:
        entrega = request.json
        cursor.execute('SELECT idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega FROM entrega WHERE idEntrega = %s', (id_entrega,))
        if cursor.fetchone() != None:
            cursor.execute('UPDATE entrega SET idEmpresa = %s, idEmpleado = %s, pesoFinal = %s, costo = %s, fechaRegistro = %s, fechaEntrega = %s WHERE idEntrega = %s', (entrega['idEmpresa'].upper(), entrega['idEmpleado'].upper(), entrega['pesoFinal'], entrega['costo'],entrega['fechaRegistro'], entrega['fechaEntrega'], id_entrega,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 202, 'message': 'Actualización exitosa', 'data': entrega})
        else:
            return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Solicitud incorrecta', 'details': 'La solicitud no pudo ser procesada por el servidor'}}) # Se retorna un objeto JSON con un error 500    
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* PUT
def actualizar_entrega(id_entrega, body, cursor, conexion):
    """Función PUT para actualizar una entrega específica en la base de datos"""

#* DELETE
def eliminar_entrega(id_entrega, cursor, conexion):
    """Función DELETE para eliminar una entrega específico o todos las entregas de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        cursor.execute('DELETE FROM entrega WHERE idEntrega = %s', (id_entrega,))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 200, 'message': 'Entrega eliminado'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
