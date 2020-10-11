from datetime import datetime 
from sqlalchemy.dialects.postgresql.base import UUID 
from breadlog import db 
import uuid 

db.UUID = UUID 

class Recipe(db.Model): 
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    total_steps = db.Column(db.Integer, nullable=False)
    total_minutes = db.Column(db.Integer, nullable=True)
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    steps = db.relationship('Step', backref='recipe_id', lazy=True)

    def __init__(self, name): 
        self.name = name 
        self.total_steps = 0
        self.total_minutes = 0 
    
    def __repr__(self): 
        return f'Recipe: {self.id}  Name: {self.name}'


class Step(db.Model): 
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    recipe_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('recipe.id'), nullable=False)  

    def __init__(self, minutes, notes): 
        self.minutes = minutes 
        self.notes = notes 

    def __repr__(self):
        return f'Step {self.step_number} Total time: {self.minutes}'


class Ingredient(db.Model): 
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Type as an enum

    def __init__(self, name): 
        self.name = name 

    def __repr__(self): 
        pass 


class StepIngredient(db.Model): 
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    # ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredient.id'), nullable=False)
    step_id = db.Column(UUID(as_uuid=True), db.ForeignKey('step.id'), nullable=False) 
    weight = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, weight):
        self.weight = weight 
    
    def __repr__(self): 
        pass 



