import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.environ['SQLALCHEMY_SECRET_KEY']

db = SQLAlchemy(app)

from breadlog import routes 
from breadlog import forms
