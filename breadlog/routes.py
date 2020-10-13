import sys 
from flask import render_template, url_for, request, redirect, flash, jsonify
from breadlog import app, db, bcrypt
from breadlog.models import Recipe, Step, User
from breadlog.forms import RecipeForm, StepForm, RegisterForm, LoginForm, AddIngredientForm
from flask_login import login_user, current_user, logout_user


@app.route('/', methods=['GET', 'POST'])
def index(): 
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register(): 
    if current_user.is_authenticated: 
        return redirect('/recipes')  # TODO: replace with something that makes sense 
    form = RegisterForm() 
    if request.method == 'POST' and not form.validate(): 
        errors= []
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
              login_user(user) # Add a remember=form.remember.data 
              return redirect(url_for('recipes'))
         else: 
             return 'Login unsuccessful' # TODO: change to a flash message
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


@app.route('/recipes/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id): 
    recipe = Recipe.query.get_or_404(recipe_id) 
    form = StepForm()
    if form.validate_on_submit(): 
        total_minutes = form.minutes.data
        new_step = Step(step_number=form.step_number.data,
                        action=form.action.data, 
                        minutes=total_minutes,
                        notes=form.notes.data, 
                        recipe_id=recipe_id)
        try: 
            if form.minutes.data > 0: 
                recipe.total_minutes += total_minutes
            recipe.total_steps += 1 
            db.session.add(new_step)
            db.session.commit()  
            return redirect(url_for('edit_recipe', recipe_id=recipe.id))
        except:
            return 'There was an error adding the step'
    return render_template('edit_recipe.html', recipe=recipe, form=form) 


@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    recipe_to_delete = Recipe.query.get_or_404(recipe_id)
    try: 
        db.session.delete(recipe_to_delete)
        db.session.commit() 
        return redirect('/recipes') 
    except: 
        return 'Error deleting recipe'


@app.route('/delete_step/<int:step_id>', methods=['GET', 'POST'])
def delete_step(step_id):
    step_to_delete = Step.query.get_or_404(step_id)
    recipe_id = step_to_delete.recipe.id
    try: 
        if step_to_delete.minutes > 0: 
            step_to_delete.recipe.total_minutes -= step_to_delete.minutes
        step_to_delete.recipe.total_steps -= 1 
        db.session.delete(step_to_delete)
        db.session.commit() 
    except: 
        return 'Error deleting step'
    return redirect(url_for('edit_recipe', recipe_id=recipe_id)) 

# Add ingredient to step 
@app.route('/step/<int:step_id>/add_step_ingredient')
def add_step_ingredient(step_id):
    form = AddIngredientForm() 
    
    
# Add ingredient to database 
@app.route('/add_ingredient')
def add_ingredient(): 
    pass 

@app.route('/logout')
def logout(): 
    logout_user() 
    return redirect('/') 

#------ API routes ------# 

# Gets all recipes 
@app.route('/recipe', methods=['GET'])
def recipe(): 
    recipes = Recipe.query.all()
    return jsonify(recipes)

# Get a recipe by ID 
@app.route('/recipe/id/<int:recipe_id>', methods=['GET'])
def recipe_id(recipe_id): 
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    return jsonify(recipe)