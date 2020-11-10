from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RecipeForm(FlaskForm): 
    recipe_name = StringField('New Recipe', 
                              render_kw={"placeholder": "Recipe name"},
                              validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create')
