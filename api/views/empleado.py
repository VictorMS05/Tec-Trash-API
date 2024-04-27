"""Vista que gestiona la lógica de los métodos HTTP para la tabla empleado de la base de datos"""

# Se importa la clase Flask y la función jsonify
from flask import jsonify, request
# Se importa la clase OperationalError de MySQLdb
from MySQLdb import OperationalError, IntegrityError

#! MÉTODOS HTTP PARA TABLA EMPLEADO

# * GET


def consultar_empleado(id_empleado, cursor):
    """Función GET para obtener un empleado específico o todos los empleados de la base de datos"""
    try:
        # Se ejecuta una consulta SQL
        if id_empleado == 'todos':
            cursor.execute('SELECT idEmpleado, nombre, apellidoPaterno, apellidoMaterno, '
                            'fechaNacimiento, nss, telefono, correo, esAdministrador, '
                            'contactoEmergenciaNombre, contactoEmergenciaApellidoP, '
                            'contactoEmergenciaApellidoM, contactoEmergenciaParentesco, '
                            'contactoEmergenciaTelefono FROM empleado')
        else:
            cursor.execute('SELECT idEmpleado, nombre, apellidoPaterno, apellidoMaterno, '
                            'fechaNacimiento, nss, telefono, correo, esAdministrador, '
                            'contactoEmergenciaNombre, contactoEmergenciaApellidoP, '
                            'contactoEmergenciaApellidoM, contactoEmergenciaParentesco, '
                            'contactoEmergenciaTelefono FROM empleado WHERE idEmpleado = %s',
                            (id_empleado,))
        empleados = cursor.fetchall()  # Se obtienen todos los registros de la consulta
        diccionario = []  # Se crea un diccionario vacío
        for registro in empleados:  # Se recorren los registros obtenidos
            arreglo = {  # Se crea un arreglo con los datos de un registro
                'idEmpleado': registro[0],
                'nombre': registro[1],
                'apellidoPaterno': registro[2],
                'apellidoMaterno': registro[3],
                'fechaNacimiento': registro[4],
                'nss': registro[5],
                'telefono': registro[6],
                'correo': registro[7],
                'esAdministrador': registro[8],
                'contactoEmergenciaNombre': registro[9],
                'contactoEmergenciaApellidoP': registro[10],
                'contactoEmergenciaApellidoM': registro[11],
                'contactoEmergenciaParentesco': registro[12],
                'contactoEmergenciaTelefono': registro[13]
            }
            diccionario.append(arreglo)  # Se agrega el arreglo al diccionario
            # Se retorna un objeto JSON con el diccionario obtenido
        return jsonify({'success': True,
                        'status': 200, 
                        'message': 'Consulta exitosa', 
                        'data': diccionario})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * POST


def insertar_empleado(cursor, conexion):
    """Función POST para registrar un empleado en la base de datos"""
    try:
        body = request.json  # Se obtiene el cuerpo de la petición
        # Se ejecuta una consulta SQL con parámetros
        cursor.execute('INSERT INTO empleado VALUES (%s, %s, %s, %s, %s, %s, %s, %s, MD5(%s), %s, '
                        '%s, %s, %s, %s, %s)',
                        (body['rfc'].upper(), body['nombre'].upper(),
                            body['apellidoPaterno'].upper(), body['apellidoMaterno'].upper(),
                            body['fechaNacimiento'], body['nss'], body['telefono'], body['correo'],
                            body['contrasenia'], body['esAdministrador'],
                            body['contactoEmergenciaNombre'].upper(),
                            body['contactoEmergenciaApellidoP'].upper(),
                            body['contactoEmergenciaApellidoM'].upper(),
                            body['contactoEmergenciaParentesco'].upper(),
                            body['contactoEmergenciaTelefono']))
        conexion.connection.commit()  # Se confirma la transacción
        # Se retorna un objeto JSON con un mensaje de éxito
        return jsonify({'success': True,
                        'status': 201, 
                        'message': 'El empleado se ha registrado exitosamente', 
                        'data': {'rfc': body['rfc'].upper(),
                                    'nombre': body['nombre'].upper(), 
                                    'apellidoPaterno': body['apellidoPaterno'].upper(), 
                                    'apellidoMaterno': body['apellidoMaterno'].upper(),
                                    'fechaNacimiento': body['fechaNacimiento'],
                                    'nss': body['nss'], 
                                    'telefono': body['telefono'], 
                                    'correo': body['correo'], 
                                    'esAdministrador': body['esAdministrador'],
                                    'contactoEmergenciaNombre': (
                                        body['contactoEmergenciaNombre'].upper()
                                    ),
                                    'contactoEmergenciaApellidoP': (
                                        body['contactoEmergenciaApellidoP'].upper()
                                    ),
                                    'contactoEmergenciaApellidoM': (
                                        body['contactoEmergenciaApellidoM'].upper()
                                    ),
                                    'contactoEmergenciaParentesco': (
                                        body['contactoEmergenciaParentesco'].upper()
                                    ),
                                    'contactoEmergenciaTelefono': (
                                        body['contactoEmergenciaTelefono']
                                    )}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# *PUT


def actualizar_empleado(id_empleado, cursor, conexion):
    """Función PUT para actualizar un empleado específico en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idEmpleado) > 0 FROM empleado WHERE idEmpleado = %s',
                        (id_empleado,))
        if cursor.fetchone()[0]:
            cursor.execute('UPDATE empleado SET nombre = %s, apellidoPaterno = %s, '
                            'apellidoMaterno = %s, fechaNacimiento = %s, nss = %s, telefono = %s, '
                            'correo = %s, esAdministrador = %s, contactoEmergenciaNombre = %s, '
                            'contactoEmergenciaApellidoP = %s, contactoEmergenciaApellidoM = %s, '
                            'contactoEmergenciaParentesco = %s, contactoEmergenciaTelefono = %s ',
                            (body['nombre'].upper(), body['apellidoPaterno'].upper(),
                                body['apellidoMaterno'].upper(), body['fechaNacimiento'],
                                body['nss'], body['telefono'], body['correo'],
                                body['esAdministrador'], body['contactoEmergenciaNombre'].upper(),
                                body['contactoEmergenciaApellidoP'].upper(),
                                body['contactoEmergenciaApellidoM'].upper(),
                                body['contactoEmergenciaParentesco'].upper(),
                                body['contactoEmergenciaTelefono']))
            rfc = id_empleado
            if body['rfc'] != id_empleado and body['rfc'] != '':
                cursor.execute('UPDATE empleado SET idEmpleado = %s WHERE idEmpleado = %s',
                                (body['rfc'], id_empleado,))
                rfc = body['rfc']
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'El empleado {rfc} se ha actualizado exitosamente', 
                            'data': {'rfc': rfc,
                                        'nombre': body['nombre'].upper(), 
                                        'apellidoPaterno': body['apellidoPaterno'].upper(), 
                                        'apellidoMaterno': body['apellidoMaterno'].upper(),
                                        'fechaNacimiento': body['fechaNacimiento'],
                                        'nss': body['nss'], 
                                        'telefono': body['telefono'], 
                                        'correo': body['correo'], 
                                        'esAdministrador': body['esAdministrador'],
                                        'contactoEmergenciaNombre': (
                                            body['contactoEmergenciaNombre'].upper()
                                        ),
                                        'contactoEmergenciaApellidoP': (
                                            body['contactoEmergenciaApellidoP'].upper()
                                        ),
                                        'contactoEmergenciaApellidoM': (
                                            body['contactoEmergenciaApellidoM'].upper()
                                        ),
                                        'contactoEmergenciaParentesco': (
                                            body['contactoEmergenciaParentesco'].upper()
                                        ),
                                        'contactoEmergenciaTelefono': (
                                            body['contactoEmergenciaTelefono']
                                        )}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empleado no encontrado', 
                                    'details': f'No se encontró el empleado {id_empleado} en la '
                                                f'base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * DELETE


def eliminar_empleado(id_empleado, cursor, conexion):
    """Función DELETE para eliminar un empleado específico o todos los empleados de la base de 
    datos"""
    try:
        cursor.execute('SELECT COUNT(idEmpleado) > 0 FROM empleado WHERE idEmpleado = %s',
                        (id_empleado,))
        if cursor.fetchone()[0]:
            # Se ejecuta una consulta SQL
            print(id_empleado)
            cursor.execute('DELETE FROM empleado WHERE idEmpleado = %s', (id_empleado,))
            conexion.connection.commit()
            return jsonify({'success': True,
                            'status': 200, 
                            'message': f'El empleado {id_empleado} se ha eliminado exitosamente'})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empleado no encontrado', 
                                    'details': f'No se encontró el empleado {id_empleado} en la '
                                                f'base de datos'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * PATCH


def actualizar_contrasenia_empleado(id_empleado, cursor, conexion):
    """Función PATCH para cambiar la contraseña de un empleado específico en la base de datos"""
    try:
        body = request.json
        cursor.execute('SELECT COUNT(idEmpleado) > 0 FROM empleado WHERE idEmpleado = %s',
                        (id_empleado,))
        if cursor.fetchone()[0]:
            if 'contrasenia' in body and body['contrasenia'] != '':
                cursor.execute('UPDATE empleado SET contrasenia = MD5(%s) WHERE idEmpleado = %s',
                                (body['contrasenia'], id_empleado,))
                conexion.connection.commit()
                return jsonify({'success': True,
                                'status': 200, 
                                'message': f'Se ha actualizado la contraseña del empleado '
                                            f'{id_empleado} exitosamente'})
            # Se retorna un objeto JSON con un error 400
            return jsonify({'error': {'code': 400,
                                        'type': 'Error del cliente', 
                                        'message': 'Petición incorrecta', 
                                        'details': 'Falta la clave y/o valor contrasenia en el body de la '
                                                    'petición'}})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empleado no encontrado', 
                                    'details': f'No se encontró el empleado {id_empleado} en la '
                                                f'base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except IntegrityError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Error de integridad MySQL', 
                                    'details': str(e)}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})

# * POST (Iniciar sesión)


def iniciar_sesion_empleado(cursor):
    """Función POST para iniciar sesión de un empleado"""
    try:
        body = request.json  # Se obtiene el cuerpo de la petición
        cursor.execute('SELECT COUNT(idEmpleado) > 0 FROM empleado WHERE correo = %s AND contrasenia'
                        ' = MD5(%s)', (body['correo'], body['contrasenia']))
        if cursor.fetchone()[0]:
            return jsonify({'success': True, 'status': 200, 'message': 'Inicio de sesión exitoso'})
        # Se retorna un objeto JSON con un error 404
        return jsonify({'error': {'code': 404,
                                    'type': 'Error del cliente', 
                                    'message': 'Empleado no encontrado', 
                                    'details': 'No se encontró el empleado en la base de datos'}})
    except KeyError as e:
        # Se retorna un objeto JSON con un error 400
        return jsonify({'error': {'code': 400,
                                    'type': 'Error del cliente', 
                                    'message': 'Petición inválida', 
                                    'details': f'Falta la clave {str(e)} en el body de la '
                                                f'petición'}})
    except OperationalError as e:
        # Se retorna un objeto JSON con un error 500
        return jsonify({'error': {'code': 500,
                                    'type': 'Error del servidor', 
                                    'message': 'Error en la base de datos', 
                                    'details': str(e)}})
