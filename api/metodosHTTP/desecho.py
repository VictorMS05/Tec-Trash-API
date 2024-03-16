from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA DESECHO

#* GET
def obtener_desecho(id_desecho, cursor):
    """Función GET para obtener un desecho específico o todos los desechos de la base de datos"""
    try:
        if id_desecho == 'todos':
            cursor.execute(
            'SELECT idDesecho, idCliente, idRecoleccion, idEntrega, nombre, modelo, marca, peso, color, estatusFuncional, fechaRegistro, fechaFinal, pago, estatusRecoleccion FROM desecho')
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
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* POST
def registrar_desecho(body, cursor, conexion):
    """Función POST para registrar un desecho en la base de datos"""
    try:
        cursor.execute('INSERT INTO desecho (idCliente, idRecoleccion, idEntrega, nombre, modelo, marca, peso, color, estatusFuncional, fechaRegistro, fechaFinal, pago, estatusRecoleccion) VALUES (%s, NULL, NULL, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), %s, %s, "No recolectado", "No entregado")', (body['idCliente'].upper(), body['nombre'].upper(), body['modelo'].upper(), body['marca'].upper(), body['peso'], body['color'].upper(), body['estatusFuncional'], body['fechaFinal'], body['pago']))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 201, 'message': 'Registro exitoso'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)})

#* DELETE
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
