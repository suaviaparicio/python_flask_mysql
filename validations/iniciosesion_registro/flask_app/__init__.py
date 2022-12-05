from flask import Flask
from flask_bcrypt import Bcrypt  

app = Flask(__name__)

app.secret_key = "silencio para mantenerla a salvo"


bcrypt = Bcrypt(app)     # estamos creando un objeto llamado bcrypt, que se realiza invocando la función Bcrypt con nuestra aplicación como argumento
