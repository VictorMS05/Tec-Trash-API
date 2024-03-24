"""Módulo para gestionar la lógica del manejo de errores en la API"""

from flask import jsonify  # Se importa la clase Flask y la función jsonify

#* Función para manejar errores 400
def solicitud_incorrecta(error):  # Función para manejar errores 400
    """Función para manejar errores 400"""
    print(error)
    return jsonify({'error': {'code': 400, 'type': 'Error del cliente', 'message': 'Solicitud incorrecta', 'details': 'La solicitud no pudo ser procesada por el servidor'}})  # Se retorna un objeto JSON con un error 400

#* Función para manejar errores 404
def pagina_no_encontrada(error):  # Función para manejar errores 404
    """Función para manejar errores 404"""
    print(error)
    return jsonify({'error': {'code': 404, 'type': 'Error del cliente', 'message': 'Página no encontrada', 'details': 'La URL solicitada no fue encontrada en el servidor'}})  # Se retorna un objeto JSON con un error 404

#* Función para manejar errores 405
def metodo_no_permitido(error):  # Función para manejar errores 405
    """Función para manejar errores 405"""
    print(error)
    return jsonify({'error': {'code': 405, 'type': 'Error del cliente', 'message': 'Método no permitido', 'details': 'El método no está permitido para la URL solicitada'}}) # Se retorna un objeto JSON con un error 405

#* Función para manejar errores 500
def error_interno_del_servidor(error):  # Función para manejar errores 500
    """Función para manejar errores 500"""
    print(error)
    return jsonify({'error': {'code': 500, 'type': 'Error del servidor', 'message': 'Error interno del servidor', 'details': 'El servidor encontró un error interno y no pudo completar la solicitud'}}) # Se retorna un objeto JSON con un error 500
