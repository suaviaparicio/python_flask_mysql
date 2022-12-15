from flask_app import app

# registramos los controladores de la app
from flask_app.controllers.auth import auth
from flask_app.controllers.pages import pages
from flask_app.controllers.recipes import recipes

app.register_blueprint(auth)
app.register_blueprint(pages)
app.register_blueprint(recipes)
'''
from app.controllers.azar import azar
from app.controllers.twitter import twitter
from app.controllers.books import books
app.register_blueprint(azar)
app.register_blueprint(twitter, url_prefix='/twitter')
app.register_blueprint(books, url_prefix='/books')
'''
if __name__=="__main__":   
    app.run(debug=True, port=8000)