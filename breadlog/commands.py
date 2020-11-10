import click
from flask.cli import with_appcontext 

from .extensions import db, bcrypt 
from .models import User, Recipe, Step, StepIngredient


@click.command(name='create_tables')
@with_appcontext 
def create_tables(): 
    db.create_all() 
    
    
@click.command(name='seed_db')
@with_appcontext 
def seed_db(): 
    hashed_pw = bcrypt.generate_password_hash('pw123').decode('utf-8')
    sample_user = User('Sample', 'sample@domain.com', hashed_pw)
    db.session.add(sample_user)
    db.session.commit() 
    
    sample_recipe = Recipe('Sample Recipe', sample_user.id)
    db.session.add(sample_recipe)
    db.session.commit() 
    
    step1 = Step()
    step2 = Step() 
