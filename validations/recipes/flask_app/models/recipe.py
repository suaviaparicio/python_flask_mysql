from datetime import datetime
from flask import flash
from flask_app.config.connection import connectToMySQL
from flask_app import bcrypt


class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.updated_at = data['user_id']

        self.recipes = [] # Creamos esta lista agregar todas las recetas que están asociadas a un usuario


    @classmethod
    def validate(cls, form):
        is_valid = True
        if len(form['name']) < 3:
            is_valid = False
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'error')
        
        if len(form['description']) < 3:
            is_valid = False
            flash('La descripción debe tener al menos 3 caracteres', 'error')

        if len(form['instructions']) < 3:
            is_valid = False
            flash('Las instrucciones deben tener al menos 3 caracteres', 'error')
        
        hoy = datetime.now().strftime('%y-%m-%d')  # El .strftime permite darle el formato de la fecha 
        recipe_date = form['date_made']

        if recipe_date > hoy:
            flash('No puedes agregar una fecha futura', 'warning')
            is_valid = False
        
        return is_valid


    @classmethod
    def save_recipe(cls, name, description, instructions, date_made, under, user_id): # Este 'nombre' es el mismo texto que llega desde el formulario (request.form[nombre]) del controlador
        query = """INSERT INTO recipes (name, description, instructions, date_made, under, user_id) 
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s, %(user_id)s);"""
        data = {
            'name': name,
            'description': description,
            'instructions': instructions,
            'date_made': date_made,
            'under': under,
            'user_id': user_id
        }
        print(data)

        new_recipe = connectToMySQL('recipes_scheme').query_db(query, data)

        return new_recipe


    @classmethod
    def get_recipes(cls):
        query = """SELECT recipes.id, recipes.name, recipes.under, users.id AS user_id, users.first_name AS user_name, users.last_name AS user_lastname
                    FROM recipes
                    JOIN users ON users.id = recipes.user_id;"""

        results = connectToMySQL('recipes_scheme').query_db(query)

        recipes = [] 

        for result in results:
            recipes.append(result)  #(cls(result)) 
        return recipes 
    
    
    @classmethod
    def get_recipe(cls, recipe_id):
        query = """SELECT recipes.id AS recipe_id, recipes.name, recipes.description, recipes.instructions, recipes.under, recipes.date_made,
                    users.first_name AS user_first_name, users.last_name AS user_lastname
                    FROM recipes
                    JOIN users ON users.id = recipes.user_id
                    WHERE recipes.id = %(recipe_id)s;"""
        data = {
            'recipe_id': recipe_id
        }
        results = connectToMySQL('recipes_scheme').query_db(query, data) 

        return results[0] 


    @classmethod
    def edit_recipe(cls, name, description, instructions, date_made, under, recipe_id): # Este 'nombre' es el mismo texto que llega desde el formulario (request.form[nombre]) del controlador
        query = """UPDATE recipes 
                    SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under=%(under)s
                    WHERE recipes.id = %(recipe_id)s;"""

        data = {
            'name': name,
            'description': description,
            'instructions': instructions,
            'date_made': date_made,
            'under': under,
            'recipe_id': recipe_id
        }

        connectToMySQL('recipes_scheme').query_db(query, data)


    @classmethod
    def delete_recipe(cls, recipe_id):
        query = """DELETE FROM recipes
                    WHERE recipes.id = %(recipe_id)s;"""
        data = {
            'recipe_id': recipe_id
        }
        connectToMySQL('recipes_scheme').query_db(query, data) 
