from flask import jsonify, request  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError

#! MÉTODOS HTTP PARA TABLA EMPRESA

#*GET
def obtener_empresa(id_empresa, cursor):
    """Función GET para obtener una empresa específica o todas las empresas de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_empresa == 'todos':
            cursor.execute(
            'SELECT idEmpresa, nombre, calle, numeroExterior, colonia, ciudad, estado, telefono, correo, contrasenia,  nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, pesoEstablecido FROM empresa')
        else:
            cursor.execute('SELECT idEmpresa, nombre, calle, numeroExterior, colonia, ciudad, estado, telefono, correo, contrasenia,nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, pesoEstablecido FROM empresa WHERE idEmpresa = %s', (id_empresa,))
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
                'estado': registro[6],
                'telefono': registro[7],
                'correo': registro[8],
                'contrasenia': registro[9],
                'nombreEncargado': registro[10],
                'apellidoPaternoE': registro[11],
                'apellidoMaternoE': registro[12],
                'esEntrega': registro[13],
                'pesoEstablecido': registro[14]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'data': [], 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* POST
def registrar_empresa(cursor, conexion):
    """Función POST para registrar una empresa en la base de datos"""
    registro = request.json
    try:
        cursor.execute("INSERT INTO empresa (idEmpresa, nombre, calle, numeroExterior, colonia, ciudad, estado, telefono, correo, contrasenia, nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, pesoEstablecido) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}')".format(registro['idEmpresa'].upper(), registro['nombre'].upper(), registro['calle'].upper(), registro['numeroExterior'], registro['colonia'].upper(), registro['ciudad'].upper(), registro['estado'].upper(),registro['telefono'], registro['correo'], registro['contrasenia'], registro['nombreEncargado'].upper(), registro['apellidoPaternoE'].upper(), registro['apellidoMaternoE'].upper(), registro['esEntrega'], registro['pesoEstablecido']))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 200, 'message': 'Empresa registrada'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* PUT
def actualizar_empresa(id_empresa, cursor, conexion):
    try:
        empresa = request.json
        cursor.execute('SELECT nombre, calle, numeroExterior, colonia, ciudad, estado, telefono, correo, contrasenia, nombreEncargado, apellidoPaternoE, apellidoMaternoE, esEntrega, pesoEstablecido FROM empresa WHERE idEmpresa = %s', (id_empresa,))
        if cursor.fetchone() != None:
            cursor.execute('UPDATE empresa SET nombre = %s, calle = %s, numeroExterior = %s, colonia = %s, ciudad = %s, estado = %s, telefono = %s, correo = %s, contrasenia = %s, nombreEncargado = %s, apellidoPaternoE = %s, apellidoMaternoE = %s, esEntrega = %s, pesoEstablecido = %s WHERE idEmpresa = %s', (empresa['nombre'], empresa['calle'], empresa['numeroExterior'],empresa['colonia'],empresa['ciudad'],empresa['estado'],empresa['telefono'],empresa['correo'],empresa['contrasenia'],empresa['nombreEncargado'], empresa['apellidoPaternoE'],empresa['apellidoMaternoE'],empresa['esEntrega'], empresa['pesoEstablecido'], id_empresa,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 202, 'message': 'Actualización exitosa', 'data': empresa})
        else:
            return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Solicitud incorrecta', 'details': 'La solicitud no pudo ser procesada por el servidor'}}) # Se retorna un objeto JSON con un error 500    
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* DELETE
def eliminar_empresa(id_empresa, cursor, conexion):
    """Función DELETE para eliminar una empresa específica o todas las empresas de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        cursor.execute('DELETE FROM empresa WHERE idEmpresa = %s', (id_empresa,))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 200, 'message': 'Empresa eliminada'})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500    
