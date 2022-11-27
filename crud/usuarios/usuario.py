
from mysqlconnection import connectToMySQL
# modelar la clase después de la tabla friend de nuestra base de datos

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        # self.nombre_completo = self.nombre + " " + self.apellido
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"

        results = connectToMySQL('usuarios_esquema').query_db(query)

        lista_usuarios = []

        for u in results:
            lista_usuarios.append(cls(u))
        return lista_usuarios

    
    @classmethod    #Este método es para guardasr los datos que ingresa el usuario en el formulario
    def save(cls, data):
        query = "INSERT INTO usuarios ( nombre, apellido, email, created_at) VALUES ( %(fnombre)s,%(lapellido)s,%(femail)s,NOW());"
        result = connectToMySQL('usuarios_esquema').query_db(query, data)
        return result
    
    @classmethod    #Este método es para borrar los datos que indicamos
    def delete(cls, id):
        query = "DELETE FROM usuarios WHERE ID=%(id)s;"
        data = {
            'id': id
        }
        result = connectToMySQL('usuarios_esquema').query_db(query, data)
        return result
    
    @classmethod    #Este método es para mostrar los datos que indicamos
    def show(cls, id):
        query = "SELECT * FROM usuarios WHERE ID=%(id)s;"
        data = {
        'id': id
        }
        result = connectToMySQL('usuarios_esquema').query_db(query, data)
        return result[0]


    @classmethod 
    def save_edit(cls, data):
        query = "INSERT INTO usuarios ( nombre, apellido, email, created_at) VALUES ( %(fnombre)s,%(lapellido)s,%(femail)s,NOW());"
        result = connectToMySQL('usuarios_esquema').query_db(query, data)
        return result
