from datetime import datetime
from sqlalchemy.dialects.postgresql.base import UUID
from breadlog import db, login_manager
from flask_login import UserMixin
from dataclasses import dataclass
import uuid

db.UUID = UUID


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@dataclass  # Decorator to allow model data to be JSON serializable
class Recipe(db.Model):
    id: int
    name: str
    total_steps: int
    total_minutes: int
    is_public: bool
    created_at: datetime
    user_id: str
    steps: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    total_steps = db.Column(db.Integer, nullable=False)
    total_minutes = db.Column(db.Integer, nullable=True)
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'),
                        nullable=False)  # User does not have to be logged in
    steps = db.relationship('Step', backref='recipe', lazy=False, order_by='Step.step_number', cascade="all, delete-orphan")

    def __init__(self, name, user_id):
        self.name = name
        self.total_steps = 0
        self.total_minutes = 0
        self.user_id = user_id
        
        
class RecipeQuery():
    @staticmethod
    def get_user_recipes_with_default(user_id, default_user_id='276007fc-a00c-415f-b990-581541d92434'):
        user_recipes = Recipe.query.filter_by(user_id=user_id).order_by(Recipe.created_at).all()
        # if user_id != default_user_id: 
        #     default_recipe = Recipe.query.filter_by(user_id=default_user_id).first() 
        #     if default_recipe: 
        #         user_recipes.append(default_recipe)
        return user_recipes


@dataclass
class Step(db.Model):
    id: int
    recipe_id: int
    step_number: int
    created_at: datetime
    hours: int 
    minutes: int
    notes: str
    ingredients: list

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hours = db.Column(db.Integer, nullable=True, default=0)
    minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    ingredients = db.relationship('StepIngredient', backref='step', 
                                  lazy=False, order_by='StepIngredient.weight', cascade="all, delete-orphan")

    def __init__(self, step_number, hours, minutes, notes, recipe_id):
        self.step_number = step_number
        self.hours = hours 
        self.minutes = minutes
        self.notes = notes
        self.recipe_id = recipe_id


class Ingredient(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Type as an enum

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Ingredient({self.name})'


@dataclass
class StepIngredient(db.Model):
    id: int
    ingredient: str
    step_id: int
    weight: float
    created_at: datetime
    
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(256), nullable=True)
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, step_id, ingredient, weight):
        self.step_id = step_id 
        self.ingredient = ingredient
        self.weight = weight


class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True, order_by='desc(Recipe.created_at)')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'User {self.email} '
