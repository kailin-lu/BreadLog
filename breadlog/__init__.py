import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.environ['SQLALCHEMY_SECRET_KEY']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
login_manager = LoginManager(app) 

from breadlog import routes 
from breadlog import forms


