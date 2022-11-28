from flask import Flask, render_template, request, redirect, session

from usuario import Usuario

app = Flask(__name__)

app.secret_key = 'keep it secret, keep it safe'

@app.route("/")
def index():
    return redirect("/usuarios")

@app.route("/usuarios")
def usuarios_actuales():
    # # llamar al método de clase get all para obtener todos los usuarioa
    # usuarios = Usuario.get_all()
    return render_template("usuarios.html", usuarios=Usuario.get_all())
    
    
@app.route("/usuario/nuevo")
def usuario_nuevo():
    return render_template('usuario_nuevo.html')

@app.route("/usuario/crear", methods = ['POST'])  # Esta ruta es la que puse en usuario_nuevo.html al crear el formulario donde el usuario ingresa los datos
def agregar_usuarios():
    print(request.form) # Es una manera de probar que si están llegando los datos que ingresa el usuario
    Usuario.save(request.form)
    # Usuario.create(request.form['nombre', request.form['apellido'], request.form['email'], request.form['created_at']])
    return redirect('/usuarios')


@app.route("/usuario/eliminar/<int:id>")  # Esta ruta es la que puse en usuario_nuevo.html al crear el formulario donde el usuario ingresa los datos
def eliminar_usuarios(id):
    print(f"eliminando al usuario {id}")
    Usuario.delete(id)
    return redirect('/usuarios')


@app.route("/usuario/mostrar/<int:id>")
def usuario_mostrar(id):
    print(f"El usuario con ID {id} será mostrado")
    usuario=Usuario.show(id)
    return render_template('usuario_id.html', usuario=usuario)

@app.route("/usuario/<int:id>/edit")
def usuario_editar(id):
    usuario=Usuario.show(id)
    return render_template('usuario_editar.html', usuario=usuario)

@app.route("/usuario/<int:id>/editar", methods = ['POST'])
def usuario_editado(id):
    Usuario.save_edit(request.form, id)
    return redirect(f"/usuario/mostrar/{id}")

if __name__ == "__main__":
    app.run(debug=True, port=8000)