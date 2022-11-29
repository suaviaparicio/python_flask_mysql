from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.dojos import Dojos 
from flask_app.models.ninjas import Ninjas

@app.route("/")
def index():
    return redirect("/dojos")

@app.route("/dojos")
def dojos():
    return render_template("dojo.html", dojos=Dojos.obtener_dojos())

@app.route("/dojo/crear", methods = ['POST'])  # Esta ruta es la que puse en dojo.html para el formulario 
def agregar_dojo():
    print(request.form) # Es una manera de probar que si están llegando los datos que ingresa el usuario
    Dojos.guardar_dojo(request.form)
    return redirect('/')

@app.route("/dojos/<int:id>")
def mostrar_dojo(id):
    print(f"El dojo con ID {id} será mostrado")
    ninjas=Dojos.get_dojos_with_ninjas(id)
    print(ninjas)
    return render_template('ninja_id.html', ninjas=ninjas, id=id)



@app.route("/ninjas")
def crear_ninja():
    return render_template("ninja.html")