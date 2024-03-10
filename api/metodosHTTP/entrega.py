from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA ENTREGA
def obtener_entrega(id_entrega, cursor):
    """Función GET para obtener una entrega específica o todas las entregas de la base de datos"""
    try:
        if id_entrega == 'todos':
            cursor.execute(
            'SELECT idEntrega, idEmpresa, idEmpleado, costo, fechaEntrega FROM entrega')
        else:
            cursor.execute('SELECT idEntrega, idEmpresa, idEmpleado, costo, fechaEntrega FROM entrega WHERE idEntrega = %s', (id_entrega,))
        entregas = cursor.fetchall()
        diccionario = []
        for registro in entregas:
            arreglo = {
                'idEntrega': registro[0],
                'idEmpresa': registro[1],
                'idEmpleado': registro[2],
                'costo': registro[3],
                'fechaEntrega': registro[4]
            }
            diccionario.append(arreglo)
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario, 'error': 'No hay error'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
