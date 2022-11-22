# importar la función que devolverá una instancia de una conexión
from mysqlconnection import connectToMySQL
# modelar la clase después de la tabla friend de nuestra base de datos


class Friend:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.occupation = data['occupation']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # ahora usamos métodos de clase para consultar nuestra base de datos

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM friends;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('primer_flask').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de friends
        friends = []
        # Iterar sobre los resultados de la base de datos y crear instancias de friends con cls
        for friend in results:
            friends.append(cls(friend))
        return friends
