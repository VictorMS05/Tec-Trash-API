from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA DESECHO
def obtener_desecho(id_desecho, cursor):
    """Función GET para obtener un desecho específico o todos los desechos de la base de datos"""
    try:
        if id_desecho == 'todos':
            cursor.execute(
            'SELECT idDesecho, idCliente, idRecoleccion, idEntrega, nombre, modelo, marca, peso, color, estatusFuncional, fechaRegistro, fechaFinal, pago, estatusRecoleccion FROM desecho')
        else:
            cursor.execute('SELECT idDesecho, idRecoleccion, idEntrega, nombre, modelo, marca peso, color, estatusFuncional, fechaRegistro, fechaFinal, pago, estatusRecoleccion FROM desecho WHERE idDesecho = %s', (id_desecho,))
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
                'estatusRecoleccion': registro[13]
            }
            diccionario.append(arreglo)
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario, 'error': 'No hay error'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500

def eliminar_desecho(id_desecho, cursor):
    """Función DELETE para eliminar un desecho específico o todos los desechos de la base de datos"""
    try:
        if id_desecho == 'todos':
            cursor.execute(
            'DELETE FROM desecho')
        else:
            cursor.execute('DELETE FROM desecho WHERE idDesecho = %s', (id_desecho,))
        
        return jsonify({'success': True, 'status': 200, 'message': 'Desecho eliminado', 'data': [], 'error': 'No hay error'})
    
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500