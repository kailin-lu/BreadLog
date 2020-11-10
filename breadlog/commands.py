import click
from flask.cli import with_appcontext 

from .extensions import db     
from .models import User, Recipe 


@click.command(name='create_tables')
@with_appcontext 
def create_tables(): 
    db.create_all() 
    
    
@click.command(name='seed_db')
@with_appcontext 
def seed_db(): 
    sample_user = User('Sample', 'sample@domain.com', 'pw123')
    db.session.add(sample_user)
    db.session.commit() 
    
    sample_recipe = Recipe('Sample Recipe', sample_user.id)
    db.session.add(sample_recipe)
    db.session.commit() 
    
    
    
