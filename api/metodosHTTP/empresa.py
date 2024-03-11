from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA EMPRESA
def obtener_empresa(id_empresa, cursor):
    """Función GET para obtener una empresa específica o todas las empresas de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_empresa == 'todos':
            cursor.execute(
            'SELECT idEmpresa, nombre, calle, numeroExterior, colonia, ciudad, telefono, correo, nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, pesoEstablecido FROM empresa')
        else:
            cursor.execute('SELECT idEmpresa, nombre, calle, numeroExterior, colonia, ciudad, telefono, correo, nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, pesoEstablecido FROM empresa WHERE idEmpresa = %s', (id_empresa,))
        empresas = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in empresas:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idEmpresa': registro[0],
                'nombre': registro[1],
                'calle': registro[2],
                'numeroExterior': registro[3],
                'colonia': registro[4],
                'ciudad': registro[5],
                'telefono': registro[6],
                'correo': registro[7],
                'nombreEncargado': registro[8],
                'apellidoPaternoE': registro[9],
                'apellidoMaternoE': registro[10],
                'esEntrega': registro[11],
                'pesoEstablecido': registro[12]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario, 'error': 'No hay error'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
    
def eliminar_empresa(id_empresa, cursor):
    """Función DELETE para eliminar una empresa específica o todas las empresas de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_empresa == 'todos':
            cursor.execute(
            'DELETE FROM empresa')
        else:
            cursor.execute('DELETE FROM empresa WHERE idEmpresa = %s', (id_empresa,))
        return jsonify({'success': True, 'status': 200, 'message': 'Empresa eliminada', 'data': [], 'error': 'No hay error'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
