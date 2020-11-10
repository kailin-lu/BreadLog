from flask import render_template, url_for, request, redirect, jsonify, make_response, Blueprint
from flask_login import current_user
from breadlog.models import Recipe, Step, User, StepIngredient
from breadlog.recipes.forms import RecipeForm
from breadlog.recipes.utils import make_err_response, sum_recipe_ingredients
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from breadlog.extensions import db

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes', methods=['GET', 'POST'])
def get_recipes():
    form = RecipeForm()
    user_id = current_user.id 
    default_user = User.query.filter_by(name='default').first()
    recipe_list = Recipe.query.filter(or_(Recipe.user_id == user_id, Recipe.user_id == default_user.id)).order_by(Recipe.created_at).all()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            recipe_name = form.recipe_name.data
            new_recipe = Recipe(name=recipe_name, user_id=user_id)
            # recipe_id = new_recipe.id
            try:
                db.session.add(new_recipe)
                db.session.commit()
                return redirect(url_for('recipes.edit_recipe', recipe_id=new_recipe.id))
            except SQLAlchemyError as e:
                return make_err_response(e)
              
    if len(recipe_list) == 0:
        return render_template('recipes.html', form=form, recipes=[], 
                               hours=0, minutes=0, ingredients={})
    else: 
        # Time calculation for first recipe displayed if recipes exist
        hours = recipe_list[0].total_minutes // 60
        minutes = recipe_list[0].total_minutes % 60
        ingredients = sum_recipe_ingredients(recipe_list[0])
            
        return render_template('recipes.html', form=form, recipes=recipe_list,
                               hours=hours, minutes=minutes,ingredients=ingredients)


@recipes.route('/recipes/edit/<int:recipe_id>', methods=['GET'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients = sum_recipe_ingredients(recipe)
    return render_template('edit_recipe.html', recipe=recipe, ingredients=ingredients)


@recipes.route('/recipes/<int:recipe_id>/add_step', methods=['POST'])
def add_step(recipe_id): 
    req = request.get_json() 
    recipe = Recipe.query.get_or_404(recipe_id)
    hours = req['hours']
    minutes = req['minutes']
    total_steps = len(recipe.steps) + 1
    new_step = Step(step_number=total_steps, 
                    hours=hours, 
                    minutes=minutes, 
                    notes=req['notes'], 
                    recipe_id=recipe_id)
    recipe.total_minutes += int(hours) * 60 + int(minutes)
    recipe.total_steps = total_steps
    try: 
        db.session.add(new_step) 
        db.session.commit()
        db.session.refresh(new_step)
        return make_response(jsonify({
            'step_number': total_steps, 
            'step_id': new_step.id, 
            'recipe_id': recipe.id, 
            'minutes': new_step.minutes, 
            'hours': new_step.hours, 
            'notes': new_step.notes, 
            'item': 'step',
            'action': 'add' 
            }), 200)
    except SQLAlchemyError as e: 
        return f'Error {e.orig} Parameters {e.params}'


@recipes.route('/delete_step/<int:step_id>', methods=['POST'])
def delete_step(step_id):
    step_to_delete = Step.query.get_or_404(step_id)
    step_id = step_to_delete.id
    # recipe_id = step_to_delete.recipe.id
    # Time calculation
    if step_to_delete.minutes > 0 or step_to_delete.hours > 0:
        step_to_delete.recipe.total_minutes -= step_to_delete.hours * 60 + step_to_delete.minutes
    step_to_delete.recipe.total_steps = len(step_to_delete.recipe.steps) - 1
    step_number = step_to_delete.step_number
    # shift step numbers after step up
    for step in step_to_delete.recipe.steps:
        if step.step_number > step_number:
            step.step_number -= 1
    try:        
        db.session.delete(step_to_delete)
        db.session.commit()
        res = make_response(jsonify({
            'step_id': step_id, 
            'step_number': step_number, 
            'item': 'step', 
            'action': 'delete'}), 200)
        return res 
    except SQLAlchemyError as e: 
        return f'Error {e.orig} Parameters {e.params}'


@recipes.route('/move_step_up/<int:step_id>', methods=['POST'])
def move_step_up(step_id):
    step_to_move = Step.query.get_or_404(step_id)
    new_step_number = step_to_move.step_number - 1
    recipe = step_to_move.recipe
    step_to_increment = [step for step in recipe.steps if step.step_number == new_step_number][0]
    step_to_increment.step_number += 1
    step_to_move.step_number = new_step_number
    try: 
        db.session.commit()
        resdata = {
            'item': 'step', 
            'action': 'moveup',
            'step_id': step_to_move.id,
            'shifted_step_id': step_to_increment.id
        } 
        return make_response(jsonify(resdata), 200)
    except SQLAlchemyError as e:
        return make_err_response(e)  
        

@recipes.route('/move_step_down/<int:step_id>', methods=['POST'])
def move_step_down(step_id):
    step_to_move = Step.query.get_or_404(step_id)
    new_step_number = step_to_move.step_number + 1
    recipe = step_to_move.recipe
    step_to_decrement = [step for step in recipe.steps if step.step_number == new_step_number][0]
    step_to_decrement.step_number -= 1
    step_to_move.step_number = new_step_number
    try: 
        db.session.commit()
        resdata = {
            'item': 'step', 
            'action': 'movedown',
            'shifted_step_id': step_to_decrement.id, 
            'step_id': step_to_move.id
        }
        return make_response(jsonify(resdata), 200)
    except SQLAlchemyError as e: 
        return make_err_response(e)


@recipes.route('/delete_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    recipe_to_delete = Recipe.query.get_or_404(recipe_id)
    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return redirect('/recipes')
    except SQLAlchemyError as e:
        return make_err_response(e)


# Add ingredient to step 
@recipes.route('/step/<int:step_id>/add_step_ingredient', methods=['POST']) 
def add_step_ingredient(step_id):
    req = request.get_json() 
    ingredient = req['ingredient']
    weight = req['weight']
    new_step_ingredient = StepIngredient(step_id=step_id, ingredient=ingredient, weight=weight)
    try: 
        db.session.add(new_step_ingredient) 
        db.session.commit() 
        db.session.refresh(new_step_ingredient)
        resdata = {
            'step_ingredient_id': new_step_ingredient.id,
            'step_id': new_step_ingredient.step_id, 
            'ingredient': ingredient, 
            'weight': weight, 
            'action': 'add', 
            'item': 'ingredient'
        }
        res = make_response(jsonify(resdata), 200) 
        return res
    except SQLAlchemyError as e: 
        return make_err_response(e)


@recipes.route('/step/<int:step_id>/step_ingredient/<int:step_ingredient_id>/delete', methods=['POST'])
def delete_step_ingredient(step_id, step_ingredient_id): 
    step_ingredient = StepIngredient.query.get_or_404(step_ingredient_id)
    try: 
        db.session.delete(step_ingredient)
        db.session.commit() 
        resdata = {
            'step_ingredient_id': step_ingredient.id,
            'action': 'delete',
            'item': 'ingredient'
        }
        return make_response(jsonify(resdata), 200)
    except SQLAlchemyError as e: 
        return make_err_response(e)
    
    
# Gets all recipes 
@recipes.route('/recipe', methods=['GET'])
def recipe():
    recipes = Recipe.query.all()
    return jsonify(recipes)


# Get a recipe by ID
@recipes.route('/recipe/id/<int:recipe_id>', methods=['GET'])
def recipe_id(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id) 
    return jsonify(recipe)
    
    
@recipes.route('/recipe/id/<int:recipe_id>/step/<int:step_id>', methods=['GET'])
def step_id(recipe_id, step_id):
    steps = Recipe.query.get_or_404(recipe_id).steps
    step = [step for step in steps if step.id == step_id][0]
    return jsonify(step)
