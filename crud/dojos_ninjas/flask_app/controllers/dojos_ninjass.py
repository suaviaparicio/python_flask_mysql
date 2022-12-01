from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.dojos import Dojos 
from flask_app.models.ninjas import Ninjas

@app.route("/")
def index():
    return redirect("/dojos")

@app.route("/dojos")
def dojos():
    dojos = Dojos.obtener_dojos()
    return render_template("dojo.html", dojos=dojos)

#En este paso rescato los valores del formulario del html
@app.route("/dojo/crear", methods = ['POST'])  # Esta ruta es la que puse en dojo.html para el formulario 
def agregar_dojo():
    nombre = request.form['nombre'] # 'nombre' es el name que se le puso al input del html para relacionarlos y es el mismo que está en el modelo 'dojos' en el método 'guardar_dojo'
    print(f'añadiendo el dojo ' + nombre ) # Para saber en la terminal si me está llegando la entrada - 
    Dojos.guardar_dojo(nombre) #En este paso llamo al modelo desde 'dojos.py), donde le doy la clase = 'Dojos' no se la doy dentro de los paréntesis y el otro parámetro 'nombre'
    return redirect('/')


@app.route("/ninjas")
def crear_ninja():
    dojos = Dojos.obtener_dojos()
    ninjas = Ninjas.get_all()
    return render_template("ninja.html", dojos=dojos, ninjas=ninjas)


@app.route("/ninja/crear", methods = ['POST']) 
def agregar_ninja():
    nombre = request.form['nombre'] # 'nombre' es el name que se le puso al input del html para relacionarlos y es el mismo que está en el modelo 'ninjas' en el método 'guardar_ninja'
    apellido = request.form['apellido']
    edad = request.form['edad']
    dojo_id = request.form['dojo_id']
    Ninjas.guardar_ninja(nombre, apellido, edad, dojo_id) #En este paso llamo al modelo desde 'ninjas.py', donde le doy la clase = 'Ninjas' no se la doy dentro de los paréntesis y los otros parámetros
    return redirect('/ninjas')


@app.route("/dojos/<int:id>")
def mostrar_dojo(id):
    print(f"El dojo con ID {id} será mostrado")
    ninjas = Ninjas.get(id)
    dojos = Ninjas.get(id)
    print(ninjas)
    print(dojos)
    return render_template('ninja_id.html', ninjas=ninjas, dojos=dojos)
