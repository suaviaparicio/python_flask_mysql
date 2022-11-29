import json
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninjas import Ninjas

class Dojos:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # Creamos esta lista para que luego podamos agregar todos los ninjas que están asociadas a un Dojo
        self.ninjas = []

    @classmethod  # Este método guarda los datos para crear un nuevo dojo
    def guardar_dojo(cls, data):
        query = "INSERT INTO dojos ( nombre , created_at , updated_at ) VALUES (%(fnombre)s,NOW(),NOW());"
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)

    @classmethod
    def obtener_dojos(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)

        lista_dojos = []

        for d in results:
            lista_dojos.append(cls(d))
        return lista_dojos
        

    # @classmethod
    # def get_dojos_with_ninjas( cls , data ):
    #     query = "SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s;"
    #     results = connectToMySQL('esquema_dojos_y_ninjas').query_db( query , data )

    #     dojo = cls( results[0] )
    #     for row_from_db in results:

    #         ninja_data = {
    #             "id" : row_from_db["ninjas.id"],
    #             "nombre" : row_from_db["ninjas.nombre"],
    #             "apellido" : row_from_db["ninjas.apellido"],
    #             "edad" : row_from_db["ninjas.edad"],
    #             "created_at" : row_from_db["ninjas.created_at"],
    #             "updated_at" : row_from_db["ninjas.updated_at"]
    #         }
    #         dojo.ninjas.append( ninjas.Ninjas( ninja_data ) )
    #     return dojo

    @classmethod
    def get_dojos_with_ninjas(cls, id):
        query = """
        SELECT * FROM ninjas
        JOIN dojos ON ninjas.dojo_id = dojos.id
        WHERE dojos.id = %(id)s;
        """
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query, {'id': id})

        lista_ninjas = []

        for u in results:
            print(u)
            # lista_ninjas = {
            #     'ninja_id': u['id'],
            #     'dojo_id': u['dojos.id'],
            #     'nombre': u['nombre'],
            #     'apellido': u['apellido'],
            #     'created_at': u['dojos.created_at'],
            #     'updated_at': u['dojos.updated_at']
            # }
            # lista_ninjas.append(cls(u))
        print(lista_ninjas)
        print(type(lista_ninjas))
        # return lista_ninjas
        # print(type(lista_ninjas))
        return cls(lista_ninjas)

    #     return json.dump({
    #     "id": id,
    #     "nombre": nombre,
    #     "apellido": apellido,
    #     "edad": edad,
    #     "created_at": datetime.datetime(2022, 11, 15, 16, 37, 50),
    #     "updated_at": datetime.datetime(2022, 11, 15, 16, 37, 50),
    #     "dojo_id": dojo.id,
    #     "dojos_id": id,
    #     "dojos_nombre": dojos.nombre,
    #     "dojos_created_at": datetime.datetime(2022, 11, 15, 16, 32, 10),
    #     "dojos_updated_at": datetime.datetime(2022, 11, 15, 16, 32, 10),
    # })

