# from datetime import datetime
from flask import flash
from flask_app.config.connection import connectToMySQL
from flask_app import bcrypt


# create_table = '''
# create table if not exists users  (
#     id int auto_increment primary key,
#     name varchar(100) not null,
#     email varchar(255) not null unique,
#     password varchar(255) not null,
#     avatar text
# )
# '''
# connectToMySQL().query_db(create_table)


class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def validate(cls, form):
        is_valid = True
        # 1. validamos el nombre
        if form['first_name'].strip() == '':
            is_valid = False
            flash('Debes ingresar un nombre', 'error')
        
        if len(form['first_name']) < 2:
            is_valid = False
            flash('El Nombre debe tener al menos 2 caracteres', 'error')

        if len(form['last_name']) < 2:
            is_valid = False
            flash('El Apellido debe tener al menos 2 caracteres', 'error')

        # 2. validamos la contraseña
        if form['password'].strip() == '':
            is_valid = False
            flash('Debes ingresar una contraseña', 'error')

        # 3. validamos que las contraseñas coincidan
        if form['password'] != form['password_confirm']:
            is_valid = False
            flash('Las contraseñas debe coincidir', 'error')

        # 4. validamos que no exista previamente otro usuario con el mismo email
        if not cls.check_email(form['email']):
            is_valid = False
            flash('El email ingresado ya se encuentra registrado', 'error')

        return is_valid


    @classmethod
    def check_email(cls, email):
        query = '''
            select * from users where email=%(email)s
        '''
        data = {
            'email': email
        }

        results = connectToMySQL('recipes_scheme').query_db(query, data)

        if len(results) == 0:
            return True
        else:
            return False


    @classmethod
    def create(cls, first_name, last_name, email, password):
        query = '''
            insert into users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        '''
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': bcrypt.generate_password_hash(password)
        }
        new_user_id = connectToMySQL('recipes_scheme').query_db(query, data)
        # retornamos el ID del usuario recientemente creado
        return new_user_id


    @classmethod
    def change_password(cls, email, old_password, new_password, new_password_confirm):
        # 1. Chequear que ambas contraseñas muevas coincidan
        if new_password != new_password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return

        # 2. Recupero el usuario con su contraseña antigua
        user = cls.get_with_credentials(email, old_password)
        if user is None:
            return

        # 3. Actualizo la contraseña
        query = '''update users set password=%(new_password)s  where email=%(email)s'''

        data = {
            'email': email,
            'new_password': bcrypt.generate_password_hash(new_password)
        }
        # 4. Le doy feedback al usuario
        flash('Contraseña fue actualizada con éxito', 'success')

        return connectToMySQL('recipes_scheme').query_db(query, data)


    @classmethod
    def get_with_credentials(cls, email, password):
        # 1. Obtenemos el usuario
        query = '''SELECT * FROM users where email=%(email)s'''

        data = {
            'email': email
        }

        results = connectToMySQL('recipes_scheme').query_db(query, data)

        if len(results) == 0:
            flash('Email inexistente o contraseña incorrecta', 'error')
            return None

        # 2. Verificar que las contraseñas coincidan
        encriptada = results[0]['password']

        if not bcrypt.check_password_hash(encriptada, password):
            flash('Email inexistente o contraseña incorrecta', 'error')
            return None

        # si llegamos hasta acá, todo está OK
        return cls(results[0])
