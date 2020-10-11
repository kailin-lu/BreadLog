from flask import render_template, url_for, request, redirect, flash
from breadlog import app 
from breadlog.models import Recipe
from breadlog.forms import CreateRecipeForm


@app.route('/', methods=['GET', 'POST'])
def index(): 
    form = CreateRecipeForm()
    if form.validate_on_submit(): 
        flash(f'We started a  new recipe {form.recipe_name.data}', category='success')
    if request.method == "POST":
        recipe_name = request.form['recipe_name']
        new_recipe = Recipe(name=recipe_name)
        try: 
            db.session.add(new_recipe)
            db.session.commit() 
            return redirect(url_for('/'))
        except: 
            return 'Error creating new recipe'
    return render_template('index.html', form=form)

@app.route('/recipes', methods=['GET', 'POST'])
def recipes(): 
    if request.method == "POST":
        recipe_name = request.form['name']
        new_recipe = Schedule(name=recipe_name)
        try: 
            db.session.add(new_recipe) 
            db.session.commit() 
            return redirect('/recipes')
        except: 
            return 'There was an issue creating your recipe'
    return render_template('recipes.html')
