from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)     # estamos creando un objeto llamado bcrypt, que se realiza invocando la función Bcrypt con nuestra aplicación como argumento

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
        return redirect("/")  # Se redirige al formulario inicial para que la persona diligencie nuevamente los datos

    #Usuario.check_email(request.form) # Es otra manera de chequear si el email ya existe. Para este caso, lo estamos haciendo en la función 'validar' del controlador

    contraseña_hash = bcrypt.generate_password_hash(request.form['contraseña']) # Se pasa la contraseña encriptada
    # 1. Creamos al usuario
    id = Usuario.guardar_usuario(request.form['nombre'], request.form['apellido'], request.form['email'], contraseña_hash) # Ya no es necesario tener el 'confirmar_contraseña' porque ya se hizo la validación en el modelo
    # 2. Le damos feedback al usuario
    flash("¡El usuario ha sido creado con éxito! Por favor, inicia sesión en la siguiente pantalla para disfrutar de los servicios.")  # Agregar el parámetro 'warning' cuando implemente toast
    # 3. Guardamos el nuevo usuario en session
    session['usuario'] = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'id': id
    }
    return redirect("/registrar")


#En este paso rescato los valores del formulario del html
@app.route("/login", methods = ['POST'])  # Esta ruta es la que puse en dojo.html para el formulario 
def iniciar_sesion():

    data = {
        'email': request.form['email']
    }
    # 1. Recuperar el usuario de la base de datos
    usuario =  Usuario.get_with_credentials(data) # Ya no es necesario tener el 'confirmar_contraseña' porque ya se hizo la validación en el modelo
    # 2. Comprobar que el usuario exista en la base de datos
    if not usuario:
        flash('El email no existe, o la contraseña es incorrecta') # Agregar el parámetro 'error' cuando implemente toast
        return redirect("/")
    # 3. Verificar que las contraseñas coincidan. 
    if not bcrypt.check_password_hash(usuario.contraseña, request.form['contraseña']):
        flash('El email no existe, o la contraseña es incorrecta' )  # Agregar el parámetro 'error' cuando implemente toast
        return redirect("/")
    # 4. Si las contraseñas coinciden, se informa al usuario que hizo log in con éxito y se configura la información que queremos guardar en la session
    flash('El usuario ingresó con éxito')

    # Guardamos los datos en session (creamos la propiedad 'usuario' en la sesión)
    session['usuario'] = {
        'nombre': usuario.nombre,
        'email': usuario.email,
        'id': usuario.id
    }
    return redirect("/home")


@app.route("/home")
def home():
    return render_template("home.html")


# Para cerrar la sesión, utilizamos la propiedad 'usuario' guardada en session
@app.route("/logout")          
def logout():
    session['usuario'] = None
    return redirect("/registrar")
