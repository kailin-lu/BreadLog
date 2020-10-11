from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateRecipeForm(FlaskForm): 
    recipe_name = StringField('Recipe Name', 
                              validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create')