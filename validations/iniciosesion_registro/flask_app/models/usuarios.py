from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email'] 
        self.contraseña = data['contraseña']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # MÉTODO PARA VALIDAR
    @classmethod # Este método es estático, por lo tanto, no puede recibir el parámetro de 'clase'
    def validar(cls, form): # Esta función solo se va a encargar de validar el formulario... Con 'cls' puedo llamar una función, dentro de la misma clase como 'cls.check_email. Por esto lo convertí en @classmethod
        # 1. Validamos el nombre
        is_valid = True
        if form['nombre'].strip() == '':
            is_valid = False
            flash('Debes ingresar un nombre') # Agregar el parámetro 'error' cuando implemente toast

        # 2. Validamos la contraseña
        if form['contraseña'].strip() == '':
            is_valid = False
            flash('Debes ingresar una contraseña') # Agregar el parámetro 'error' cuando implemente toast
        
        # 2. Validamos que las contraseñas coincidan
        if form['contraseña'] != form['confirma_contraseña']:
            is_valid = False
            flash('Las contraseñas deben coincidir') # Agregar el parámetro 'error' cuando implemente toast

        # 2. Validamos que no exita un usuario con el mismo email (Se puede poner en la BD como 'unique value', pero es mejor validarlo primero en el formulario)
        if not cls.check_email(form['email']):
            is_valid = False
            flash('El email ingresado ya está registrado, por favor verifica tus datos') # Agregar el parámetro 'error' cuando implemente toast
        return is_valid

    @classmethod
    def check_email(cls, email):    # Quiero llamar esta función dentro de la función 'validar'. Retorna si el email existe a través de True o False. Todos los métodos de clase, neceitan un parámetro 'cls'
        query = """SELECT * FROM usuarios
                WHERE email = %(email)s;""" # Hago la consulta a la base de datos
        data = {
            'email': email
        }
        results = connectToMySQL('esquema_registro_usuarios').query_db(query, data) 

        if len(results) == 0:
            return True
        else:
            return False


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL('esquema_registro_usuarios').query_db(query)

        usuarios = []

        for result in results:
            new_usuario = cls(result)
            usuarios.append(new_usuario)
        return usuarios
    

    @classmethod  # Este método es para guardar los datos que ingresa el usuario en el formulario
    def guardar_usuario(cls, nombre, apellido, email, contraseña):
        query = """INSERT INTO usuarios (nombre, apellido, email, contraseña) 
                VALUES ( %(nombre)s,%(apellido)s,%(email)s,%(contraseña)s);"""
        data = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'contraseña': contraseña  
        }
        new_user_id = connectToMySQL('esquema_registro_usuarios').query_db(query, data) # Porque el query de insert, devuelve desde la BD el ID del usuario
        
        # Retornamos el ID del usuario recientemente creado
        return new_user_id


    @classmethod
    def get_with_credentials(cls, data): # ¿por qué nos e le pasa la data? ******************
        # 1. obtener el usuario
        query = """SELECT * FROM usuarios
                    WHERE email = %(email)s;"""
        # data = {
        #     'email': email,
        #     'contraseña': contraseña
        # }
        results = connectToMySQL('esquema_registro_usuarios').query_db(query, data)

        # Comprobar que el usuario exista
        if len(results) < 1:
            return False

        # Si llegamos hasta este punto sin caer en un 'if', todo está bien
        return cls(results[0])  # Le estoy aplicando la clase Usuario, para que me devuelva un objeto del tipo Usuario
