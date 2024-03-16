from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA ENTREGA

#* GET
def obtener_entrega(id_entrega, cursor):
    """Función GET para obtener una entrega específica o todas las entregas de la base de datos"""
    try:
        if id_entrega == 'todos':
            cursor.execute(
            'SELECT idEntrega, idEmpresa, idEmpleado, costo, fechaEntrega FROM entrega')
        else:
            cursor.execute('SELECT idEntrega, idEmpresa, idEmpleado, costo, fechaRegistro, fechaEntrega FROM entrega WHERE idEntrega = %s', (id_entrega,))
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
