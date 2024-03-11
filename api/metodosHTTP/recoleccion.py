from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA RECOLECCION
def obtener_recoleccion(id_recoleccion, cursor):
    """Función GET para obtener una recolección específica o todas las recolecciones de la base de datos"""
    try:
        if id_recoleccion == 'todos':
            cursor.execute(
            'SELECT idRecoleccion, idEmpleado, idEmpleado, pesoFinal fechaRegistro, fechaRecoleccion FROM recoleccion')
        else:
            cursor.execute('SELECT idRecoleccion, idEmpleado, pesoFinal, fechaRegistro, fechaRecoleccion FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
        recolecciones = cursor.fetchall()
        diccionario = []
        for registro in recolecciones:
            arreglo = {
                'idRecoleccion': registro[0],
                'idEmpleado': registro[1],
                'pesoFinal': registro[2],
                'fechaRegistro': registro[3],
                'fechaRecoleccion': registro[4]
            }
            diccionario.append(arreglo)
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario, 'error': 'No hay error'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
    
def eliminar_recoleccion(id_recoleccion, cursor):
    """Función DELETE para eliminar una recolección específica o todas las recolecciones de la base de datos"""
    try:
        if id_recoleccion == 'todos':
            cursor.execute(
            'DELETE FROM recoleccion')
        else:
            cursor.execute('DELETE FROM recoleccion WHERE idRecoleccion = %s', (id_recoleccion,))
        return jsonify({'success': True, 'status': 200, 'message': 'Recoleccion eliminada', 'data': [], 'error': 'No hay error'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
