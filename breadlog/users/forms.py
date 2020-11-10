from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, PasswordField 
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(message='Email is required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(message="Name is required")])
    email = StringField('Email', validators=[DataRequired(message='Email not validated')])
    password = PasswordField('Password', validators=[DataRequired(message='password not validated')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='confirm password not validated'), 
                                                                     EqualTo('password', message='confirm passwords not the same')])
    submit = SubmitField('Create Account')
