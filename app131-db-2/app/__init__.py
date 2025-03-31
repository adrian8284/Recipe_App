from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

myapp_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
)

db = SQLAlchemy(myapp_obj)

# For user authentication using Flask-Login
login_manager = LoginManager()
login_manager.init_app(myapp_obj) # Initialize Flask-Login with App
login_manager.login_view = 'main.login' # Set login view for unauthorized access, redirecting to main.login route

from app import routes, models
