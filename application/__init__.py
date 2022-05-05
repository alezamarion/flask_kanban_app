
#Application folder: this is where all the application logic lives.
#The __init__.py file in this folder is where the app object is created, and where the blueprints are registered.

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Migrate(app, db)

#passing application to login manager
login_manager.init_app(app)
login_manager.login_view = 'login'

# When you call .register_blueprint(), you apply all operations recorded in the Flask Blueprint views_blueprint
#to app. Now, requests to the app for the URL / will be served using .about() or .blog() etc from the Flask Blueprint.
from application.views import views_blueprint
app.register_blueprint(views.views_blueprint)
