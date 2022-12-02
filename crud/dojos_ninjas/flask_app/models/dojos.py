import json
from flask_app.config.mysqlconnection import connectToMySQL

class Dojos:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.ninjas = [] # Creamos esta lista para que luego podamos agregar todos los ninjas que están asociadas a un Dojo

    @classmethod  # Este método guarda los datos para crear un nuevo dojo
    def guardar_dojo(cls, nombre): # Este 'nombre' es el mismo texto que llega desde el formulario (request.form[nombre]) del controlador
        query = """INSERT INTO dojos (nombre) 
                VALUES (%(nombre)s);"""
        data = {
            'nombre': nombre
        }
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)


    @classmethod
    def obtener_dojos(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query) # Esto me devuelve un arreglo de diccionarios

        dojos = [] #lista vacía parea ir agregando los dojos que se convertirán en OBJETOS. Este nombre es el que va a ir en el for loop del html

        for result in results:
            new_dojo = cls(result)
            dojos.append(new_dojo) # Esto es para crear los objetos que llegan en 'results' como diccionarios
        return dojos  # Lista de objetos
    
    
    @classmethod
    def obtener_uno(cls, id):
        query = """SELECT * FROM dojos
                    WHERE id = %(id)s;"""
        data = {
            'id': id
        }
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data) # Esto me devuelve un arreglo de diccionarios

        dojos = [] #lista vacía parea ir agregando los dojos que se convertirán en OBJETOS. Este nombre es el que va a ir en el for loop del html

        for result in results:
            new_dojo = cls(result)
            dojos.append(new_dojo) # Esto es para crear los objetos que llegan en 'results' como diccionarios
        return dojos[0]  # Lista de objetos


