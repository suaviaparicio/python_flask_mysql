from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuarios import Usuario


@app.route("/")
def index():
    return redirect("/registrar")


@app.route("/registrar")
def registro_inicio():
    return render_template("sesion_registro.html")


@app.route("/registro", methods = ['POST'])
def registro():
    # 0. validar el formulario (Viene de 'Validar(form)' en el modelo): (La primer validación es en el front end que se agregar en el formulario del HTML)
    if not Usuario.validar(request.form):
        return redirect('/')  # Se redirige al formulario inicial para que la persona diligencie nuevamente los datos
    Usuario.check_email(request.form) # Es otra manera de chequear si el email ya existe. Para este caso, lo estamos haciendo en la función 'validar' del controlador

    # 1. Creamos al usuario
    Usuario.guardar_usuario(request.form['nombre'], request.form['apellido'], request.form['email'], request.form['contraseña']) # Ya no es necesario tener el 'confirmar_contraseña' porque ya se hizo la validación en el modelo
    # 2. Le damos feedback al usuario
    flash("¡El usuario ha sido creado con éxito! Por favor, inicia sesión en la siguiente pantalla para disfrutar de los servicios.")  # Agregar el parámetro 'warning' cuando implemente toast
    return redirect("/registrar")


#En este paso rescato los valores del formulario del html
@app.route("/login", methods = ['POST'])  # Esta ruta es la que puse en dojo.html para el formulario 
def iniciar_sesion():
    # 1. Recuperar el usuario de la base de datos
    usuario =  Usuario.get_with_credentials(request.form['email'], request.form['contraseña']) # Ya no es necesario tener el 'confirmar_contraseña' porque ya se hizo la validación en el modelo
    
    # 2. Si el usuario es None
    if usuario is None:
        return redirect("/registrar")
    
    flash('El usuario ingresó con éxito')
    return redirect('/home')


@app.route("/home")
def home():
    return render_template("home.html")
