from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField,\
     FormField, FieldList, SubmitField, PasswordField 
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo

class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(message='Email is required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    submit = SubmitField('Log In') 

class RegisterForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(message='Email not validated')])
    password = PasswordField('Password', validators=[DataRequired(message='password not validated')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='confirm password not validated'), 
                                                                     EqualTo('password', message='confirm passwords not the same')])
    submit = SubmitField('Create Account')

class IngredientForm(FlaskForm): 
    weight = FloatField('Weight', validators=[NumberRange(min=0, message='Weight must be greater than or equal to 0')])

class StepForm(FlaskForm): 
    action_choices = [
        ('mix', 'Mix'), 
        ('autolyse', 'Autolyse'), 
        ('knead', 'Knead'), 
        ('rest', 'Rest'), 
        ('fold', 'Fold'), 
        ('shape', 'Shape'), 
        ('bake', 'Bake')
    ]
    step_number = IntegerField('Step Number', validators=[NumberRange(min=0)]) 
    action = SelectField('Action', choices=action_choices)
    # Add ingredients form 
    minutes = IntegerField('Timer', validators=[NumberRange(min=0)])
    notes = TextAreaField('Details')
    submit = SubmitField('Add Step')


class RecipeForm(FlaskForm): 
    recipe_name = StringField('Recipe Name', 
                              validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create')