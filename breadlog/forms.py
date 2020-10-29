from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField,\
     FormField, FieldList, SubmitField, PasswordField 
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from breadlog import db
from breadlog.models import Ingredient, Step


class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(message='Email is required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Name is required")])
    email = StringField('Email', validators=[DataRequired(message='Email not validated')])
    password = PasswordField('Password', validators=[DataRequired(message='password not validated')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='confirm password not validated'), 
                                                                     EqualTo('password', message='confirm passwords not the same')])
    submit = SubmitField('Create Account')


class AddIngredientForm(FlaskForm): 
    ingredient = QuerySelectField('Ingredient', 
                                  validators=[DataRequired()], 
                                  query_factory=lambda: ingredient_choices)
    weight = FloatField('Weight', validators=[NumberRange(min=0, message='Weight must be greater than or equal to 0'),
                                              DataRequired()])
    
    def ingredient_choices(): 
        return db.session.query(Ingredient).order_by(Ingredient.name).all()


class StepForm(FlaskForm):
    minutes = IntegerField('Timer', default=0)
    notes = TextAreaField('Details', default='')
    submit = SubmitField('Add Step')
    
    def validate_minutes(self, minutes): 
        """Checks that minutes is left blank or is >= 0"""
        if minutes.data and minutes.data < 0: 
            raise ValidationError('Minutes must be 0 or greater')   


class RecipeForm(FlaskForm): 
    recipe_name = StringField('New Recipe', 
                              render_kw={"placeholder": "Recipe name"},
                              validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create')
