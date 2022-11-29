from flask_app.config.mysqlconnection import connectToMySQL


class Ninjas:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.edad = data['edad'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM ninjas;
        """
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)

        lista_ninjas = []

        for u in results:
            lista_ninjas.append(cls(u))
        return lista_ninjas
    
    # @classmethod
    # def get_all(cls):
    #     query = """
    #     SELECT * FROM ninjas
    #     JOIN dojos ON ninjas.dojo_id = dojos.id;
    #     """
    #     results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)

    #     lista_ninjas = []

    #     for u in results:
    #         lista_ninjas.append(cls(u))
    #     return lista_ninjas

    @classmethod
    def get(cls, id):
        query = """
        SELECT * FROM ninjas
        JOIN dojos ON ninjas.dojo_id = dojos.id
        WHERE dojos.id=%(id)s;
        """
        data = {
            'id': id
        }

        results = connectToMySQL(
            'esquema_dojos_y_ninjas').query_db(query, data)
        dojo = cls(results[0])
        return dojo

    @classmethod  # Este método es para guardar los datos que ingresa el usuario en el formulario
    def guardar_ninja(cls, data):
        query = "INSERT INTO ninjas ( nombre, apellido, edad, dojo_id, created_at) VALUES ( %(fnombre)s,%(lapellido)s,%(fedad)s,%(dojo_id)sNOW());"
        result = connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)
        return result
