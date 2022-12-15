from flask import request, redirect, render_template, Blueprint, flash, session
from flask_app.models.users import User
from flask_app.decorators import login_required
from flask_app.models.recipe import Recipe

recipes = Blueprint('recipes', __name__, template_folder='templates')



# @recipes.route('/')
# def home():
#     if session['user'] is not None:
#         return redirect('/recipes')
#     recipes = Recipe.get_all_recipes()
#     return render_template('home.html', recipes=recipes)


@recipes.route('/addrecipe')
def add_recipe():
    return render_template('addrecipe.html', user=session['user'])


@recipes.route('/addrecipe', methods=['POST'])
def register_recipe():
    if not Recipe.validate(request.form):
        return redirect('/recipes')

    Recipe.save_recipe(request.form['name'], request.form['description'],
                        request.form['instructions'], request.form['date_made'], request.form['under'], session['user']['id']) 
    flash('La Receta fue agregada con éxito', 'success')
    return redirect('/recipes')


@recipes.route('/recipes')
@login_required
def get_recipes_for_registered_users():
    all_recipes = Recipe.get_recipes_for_registered_users() # all_recipes es como lo voy a llamar en el HTML cuando itere para renderizar la información
    return render_template('recipes.html', all_recipes=all_recipes, user=session['user']) # Solo aca llamo la información del usuario desde la sesión


@recipes.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.get_recipe(recipe_id)
    return render_template('viewrecipe.html', recipe=recipe,  user=session['user'])


@recipes.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    edit_recipe = Recipe.get_recipe(recipe_id)
    print(edit_recipe)
    return render_template('editrecipe.html', edit_recipe=edit_recipe,  user=session['user'])


@recipes.route('/editrecipe', methods=['POST'])
def modified_recipe(recipe_id):
    if not Recipe.validate(request.form):
        return redirect('/recipes')


    Recipe.edit_recipe(request.form['name'], request.form['description'],request.form['instructions'], 
                        request.form['date_made'], request.form['under'], recipe_id)

    flash('La receta fue editada con éxito', 'success')
    return redirect('/recipes')







