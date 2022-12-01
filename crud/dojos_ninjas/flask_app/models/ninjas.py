from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.dojos import Dojos 


class Ninjas:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.edad = data['edad'] 
        self.dojo = data['dojo_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)

        ninjas = []

        for result in results:
            new_ninja = cls(result)
            ninjas.append(new_ninja)
        return ninjas
    

    @classmethod  # Este método es para guardar los datos que ingresa el usuario en el formulario
    def guardar_ninja(cls, nombre, apellido, edad, dojo_id):
        query = """INSERT INTO ninjas (nombre, apellido, edad, dojo_id) 
                VALUES ( %(nombre)s,%(apellido)s,%(edad)s,%(dojo_id)s);"""
        data = {
            'nombre': nombre,
            'apellido': apellido,
            'edad': str(edad),
            'dojo_id': str(dojo_id)
        }
        result = connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)
        return result


    @classmethod
    def get(cls, id):
        query = """
        SELECT * FROM ninjas
        JOIN dojos ON ninjas.dojo_id = dojos.id;
        """

        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)

        ninjas = []
        # import pdb; pdb.set_trace() # Esto hace una pausa para poder ver qué trae results

        #Iterar sobre los resultados de la base de datos y crear instancias (objetos)
        for result in results: # results es una lista de diccionarios
            #Por cada diccionario en results, creo un Ninja
            new_ninja = cls(result)
            #Por cada diccionario en results, creo un Dojo    
            dojo = Dojos({
                'id': result['dojos.id'],
                'nombre': result['dojos.nombre'],
                'created_at': result['dojos.created_at'],
                'updated_at': result['dojos.updated_at']
            })
            new_ninja.dojo = dojo # Con esto, uno ambos objetos
            
            ninjas.append(new_ninja)

            return ninjas

