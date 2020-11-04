import sys
from collections import defaultdict
from flask import render_template, url_for, request, redirect, flash, jsonify, make_response
from breadlog import app, db, bcrypt
from breadlog.models import Recipe, Step, User, StepIngredient
from breadlog.forms import RecipeForm, StepForm, RegisterForm, LoginForm, AddIngredientForm
from flask_login import login_user, current_user, logout_user
from sqlalchemy.exc import SQLAlchemyError


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/recipes') 
    form = RegisterForm()
    if request.method == 'POST' and not form.validate():
        errors = []
        for field, error in form.errors.items():
            for err in error:
                errors.append([field, err])
        return ' '.join([str(i) for i in errors])
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(form.email.data, hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return 'There was an error creating user'
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/recipes')  # TODO: replace with something that makes sense 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and the password matches
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)  # Add a remember=form.remember.data
            return redirect(url_for('recipes'))
        else:
            return 'Login unsuccessful'  # TODO: change to a flash message
    return render_template('login.html', form=form)


@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    form = RecipeForm()
    user_id = current_user.id
    recipes = Recipe.query.filter_by(user_id=user_id).order_by(Recipe.created_at).all()
    if request.method == 'POST':
        if form.validate_on_submit():
            recipe_name = form.recipe_name.data
            new_recipe = Recipe(name=recipe_name, user_id=user_id)
            recipe_id = new_recipe.id
            try:
                db.session.add(new_recipe)
                db.session.commit()
                return redirect(url_for('edit_recipe', recipe_id=new_recipe.id))
            except:
                return 'Something went wrong'
    return render_template('recipes.html', form=form, recipes=recipes)


@app.route('/recipes/edit/<int:recipe_id>', methods=['GET'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients = sum_recipe_ingredients(recipe)
    return render_template('edit_recipe.html', recipe=recipe, ingredients=ingredients)


@app.route('/recipes/<int:recipe_id>/add_step', methods=['POST'])
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
        return make_response(jsonify({'message': 'successful'}, 200))
    except SQLAlchemyError as e: 
        return f'Error {e.orig} Parameters {e.params}'


@app.route('/delete_step/<int:step_id>', methods=['POST'])
def delete_step(step_id):
    step_to_delete = Step.query.get_or_404(step_id)
    recipe_id = step_to_delete.recipe.id
    msg = ''
    if step_to_delete.minutes > 0:
        step_to_delete.recipe.total_minutes -= step_to_delete.minutes
    step_to_delete.recipe.total_steps = len(step_to_delete.recipe.steps) - 1
    step_number = step_to_delete.step_number
    # shift step numbers after step up
    for step in step_to_delete.recipe.steps:
        if step.step_number > step_number:
            step.step_number -= 1
    try:        
        db.session.delete(step_to_delete)
        db.session.commit()
        res = make_response(jsonify({'message': 'delete successful'}), 200)
        return res 
    except SQLAlchemyError as e: 
        return f'Error {e.orig} Parameters {e.params}'


@app.route('/move_step_up/<int:step_id>', methods=['GET', 'POST'])
def move_step_up(step_id):
    step_to_move = Step.query.get_or_404(step_id)
    new_step_number = step_to_move.step_number - 1
    recipe = step_to_move.recipe
    step_to_increment = [step for step in recipe.steps if step.step_number == new_step_number][0]
    step_to_increment.step_number += 1
    step_to_move.step_number = new_step_number
    db.session.commit()
    return redirect(url_for('edit_recipe', recipe_id=recipe.id))


@app.route('/move_step_down/<int:step_id>', methods=['GET', 'POST'])
def move_step_down(step_id):
    step_to_move = Step.query.get_or_404(step_id)
    new_step_number = step_to_move.step_number + 1
    recipe = step_to_move.recipe
    step_to_decrement = [step for step in recipe.steps if step.step_number == new_step_number][0]
    step_to_decrement.step_number -= 1
    step_to_move.step_number = new_step_number
    db.session.commit()
    return redirect(url_for('edit_recipe', recipe_id=recipe.id))


@app.route('/delete_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    recipe_to_delete = Recipe.query.get_or_404(recipe_id)
    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return redirect('/recipes')
    except:
        return 'Error deleting recipe'


# Add ingredient to step 
@app.route('/step/<int:step_id>/add_step_ingredient', methods=['POST']) 
def add_step_ingredient(step_id):
    req = request.get_json() 
    ingredient = req['ingredient']
    weight = req['weight']
    print(req)
    new_step_ingredient = StepIngredient(step_id=step_id, ingredient=ingredient, weight=weight)
    try: 
        db.session.add(new_step_ingredient) 
        db.session.commit() 
        res = make_response(jsonify({'ingredient': 'received'}), 200) 
    except: 
        res = make_response(jsonify({'ingredient': 'not received'}), 404) 
    return res


@app.route('/step_ingredient/<string:step_ingredient_id>/delete_step_ingredient', methods=['POST'])
def delete_step_ingredient(step_ingredient_id): 
    step_ingredient = StepIngredient.query.get_or_404(step_ingredient_id)
    try: 
        db.session.delete(step_ingredient)
        db.session.commit() 
    except: 
        return 'Error deleting step ingredient'


# sum ingredient totals in recipe 
def sum_recipe_ingredients(recipe): 
    ingredient_list = defaultdict(list)
    flour_weight = 0 
    for step in recipe.steps: 
        for ingr in step.ingredients: 
            if ingr.ingredient in ingredient_list.keys():
                ingredient_list[ingr.ingredient][0] += ingr.weight 
            else: 
                ingredient_list[ingr.ingredient].append(ingr.weight)
            # if ingredient name contains flour add to flour weight 
            if 'FLOUR' in ingr.ingredient:
                flour_weight += ingr.weight
    for ingr, val in ingredient_list.items(): 
        if flour_weight != 0: 
            ingredient_list[ingr].append(round(val[0]*100 / flour_weight,1))
        else: 
            ingredient_list[ingr].append(0)
    return ingredient_list


# Add ingredient to database 
@app.route('/add_ingredient')
def add_ingredient():
    pass


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


# ------ API routes ------#

# Gets all recipes 
@app.route('/recipe', methods=['GET'])
def recipe():
    recipes = Recipe.query.all()
    return jsonify(recipes)


# Get a recipe by ID
@app.route('/recipe/id/<int:recipe_id>', methods=['GET'])
def recipe_id(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id) 
    return jsonify(recipe)
    
    
@app.route('/recipe/id/<int:recipe_id>/step/<int:step_id>', methods=['GET'])
def step_id(recipe_id, step_id):
    steps = Recipe.query.get_or_404(recipe_id).steps
    step = [step for step in steps if step.id == step_id][0]
    return jsonify(step)
