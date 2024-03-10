from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA EMPLEADO
def obtener_empleado(id_empleado, cursor):
    """Función GET para obtener un empleado específico o todos los empleados de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_empleado == 'todos':
            cursor.execute(
            'SELECT idEmpleado, nombre, apellidoPaterno, apellidoMaterno, telefono, correo FROM empleado')
        else:
            cursor.execute('SELECT idEmpleado, nombre, apellidoPaterno, apellidoMaterno, telefono, correo FROM empleado WHERE idEmpleado = %s', (id_empleado,))
        empleados = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in empleados:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idEmpleado': registro[0],
                'nombre': registro[1],
                'apellidoPaterno': registro[2],
                'apellidoMaterno': registro[3],
                'telefono': registro[4],
                'correo': registro[5]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario, 'error': 'No hay error'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500
