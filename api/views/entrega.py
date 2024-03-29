"""Vista que gestiona la lógica de los métodos HTTP para la tabla entrega de la base de datos"""

# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA ENTREGA

# * GET


def obtener_entrega(id_entrega, cursor):
    """Función GET para obtener una entrega específica o todas las entregas de la base de datos"""
    try:
        if id_entrega == 'todos':
            cursor.execute(
                'SELECT idEntrega, idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega FROM entrega')
        else:
            cursor.execute(
                'SELECT idEntrega, idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega FROM entrega WHERE idEntrega = %s', (id_entrega,))
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
        # Se retorna un objeto JSON con un error 500
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)})

# * POST


def registrar_entrega(cursor, conexion):
    """Función POST para registrar una entrega en la base de datos"""
    try:
        body = request.json
        cursor.execute('INSERT INTO entrega (idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP(), NULL)',
                       (body['idEmpresa'].upper(), body['idEmpleado'].upper(), body['pesoFinal'], body['costo']))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 201, 'message': 'Registro exitoso'})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'success': False, 'status': 500, 'message': 'Error en la base de datos', 'error': str(e)})

# *PUT


def actualizar_entrega(id_entrega, cursor, conexion):
    """Función PUT para actualizar una entrega específica en la base de datos"""
    try:
        entrega = request.json
        cursor.execute(
            'SELECT idEmpresa, idEmpleado, pesoFinal, costo, fechaRegistro, fechaEntrega FROM entrega WHERE idEntrega = %s', (id_entrega,))
        if cursor.fetchone() != None:
            cursor.execute('UPDATE entrega SET idEmpresa = %s, idEmpleado = %s, pesoFinal = %s, costo = %s, fechaRegistro = %s, fechaEntrega = %s WHERE idEntrega = %s', (
                entrega['idEmpresa'].upper(), entrega['idEmpleado'].upper(), entrega['pesoFinal'], entrega['costo'], entrega['fechaRegistro'], entrega['fechaEntrega'], id_entrega,))
            conexion.connection.commit()
            return jsonify({'success': True, 'status': 202, 'message': 'Actualización exitosa', 'data': entrega})
        else:
            # Se retorna un objeto JSON con un error 404
            return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Entrega no encontrada', 'details': f'No se encontró la entrega {id_entrega} en la base de datos'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})

# * DELETE


def eliminar_entrega(id_entrega, cursor, conexion):
    """Función DELETE para eliminar una entrega específico o todos las entregas de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        cursor.execute(
            'DELETE FROM entrega WHERE idEntrega = %s', (id_entrega,))
        conexion.connection.commit()
        return jsonify({'success': True, 'status': 200, 'message': 'Entrega eliminado'})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})

# * PATCH


def finalizar_entrega(id_entrega, cursor, conexion):
    """Función PATCH para finalizar una entrega específica en la base de datos"""
    try:
        body = request.json
        cursor.execute(f'SELECT fechaEntrega FROM entrega WHERE idEntrega = {id_entrega}')
        fecha_entrega = cursor.fetchone()
        if fecha_entrega[0] is not None:
            if 'estatus' in body:
                if body['estatus'].upper() == 'EN PROCESO' and fecha_entrega[0] is None:
                    cursor.execute('UPDATE entrega SET estatus = %s WHERE idEntrega = %s', (body['estatus'].upper(), id_entrega,))
                    conexion.connection.commit()
                    return jsonify({'success': True, 'status': 200, 'message': 'La entrega ha comenzado exitosamente', 'data': {'idEntrega': id_entrega, 'estatus': body['estatus'].upper()}})
                if body['estatus'].upper() == 'EN PROCESO' and fecha_entrega[0] is not None:
                    return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Entrega ya realizada', 'details': f'La entrega {id_entrega} ya fue realizada el {fecha_entrega[0]}'}})
                if body['estatus'].upper() == 'REALIZADA' and fecha_entrega is None:
                    cursor.execute('UPDATE entrega SET estatus = %s, fechaEntrega = CURRENT_TIMESTAMP() WHERE idEntrega = %s', (body['estatus'].upper(), id_entrega,))
                    conexion.connection.commit()
                    return jsonify({'success': True, 'status': 200, 'message': 'Entrega exitosa', 'data': {'idEntrega': id_entrega, 'estatus': body['estatus'].upper(), 'fechaEntrega': fecha_entrega[0]}})
                if body['estatus'].upper() == 'REALIZADA' and fecha_entrega is not None:
                    return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Entrega ya realizada', 'details': f'La entrega {id_entrega} ya fue realizada el {fecha_entrega[0]}'}})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Petición inválida', 'details': 'Falta la clave estatus en el body de la petición'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Entrega no encontrada', 'details': f'No se encontró la entrega {id_entrega} en la base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Petición inválida', 'details': f'Falta la clave {str(e)} en el body de la petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Error de integridad MySQL', 'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error en la base de datos', 'details': str(e)}})
