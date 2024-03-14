from flask import jsonify  # Se importa la clase Flask y la función jsonify
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError
from werkzeug.security import generate_password_hash

#! MÉTODOS HTTP PARA TABLA CLIENTE

#* GET
def obtener_clientes(id_cliente, cursor):
    """Función GET para obtener un cliente específico o todos los clientes de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_cliente == 'todos':  # Si no se recibe un id
            cursor.execute(
            'SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, calle, numeroExterior, colonia, codigoPostal, telefono, correo FROM cliente')
        else:  # Si se recibe un id
            cursor.execute('SELECT idCliente, nombre, apellidoPaterno, apellidoMaterno, calle, numeroExterior, colonia, codigoPostal, telefono, correo FROM cliente WHERE idCliente = %s', (id_cliente,))  # Se ejecuta una consulta SQL con un parámetro
        clientes = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in clientes:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idCliente': registro[0],
                'nombre': registro[1],
                'apellidoPaterno': registro[2],
                'apellidoMaterno': registro[3],
                'calle': registro[4],
                'numeroExterior': registro[5],
                'colonia': registro[6],
                'codigoPostal': registro[7],
                'telefono': registro[8],
                'correo': registro[9]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True, 'status': 200, 'message': 'Consulta exitosa', 'data': diccionario})
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500

#* POST
def registrar_cliente(body, cursor, conexion):
    """Función POST para registrar un cliente en la base de datos"""
    try:
        # Se ejecuta una consulta SQL con parámetros
        contrasenia_encriptada = generate_password_hash(body['contrasenia'], method='pbkdf2:sha256')
        cursor.execute('INSERT INTO cliente VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (body['idCliente'].upper(), body['nombre'].upper(), body['apellidoPaterno'].upper(), body['apellidoMaterno'].upper(), body['calle'].upper(), body['numeroExterior'], body['colonia'].upper(), body['codigoPostal'], body['telefono'], body['correo'], contrasenia_encriptada))
        conexion.connection.commit()  # Se confirma la transacción
        return jsonify({'success': True, 'status': 201, 'message': 'Registro exitoso'})  # Se retorna un objeto JSON con un mensaje de éxito
    except OperationalError as e:
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)}) # Se retorna un objeto JSON con un error 500