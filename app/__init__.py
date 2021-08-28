from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__) #flask object instance
app.config.from_object(Config)
db = SQLAlchemy(app) #db instance
migrate = Migrate(app, db)

#flask login
login = LoginManager(app)
login.login_view = 'login' # tells Flask-login of the view fn that handles login

from app import routes, models, errors