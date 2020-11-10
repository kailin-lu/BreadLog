import click
from flask.cli import with_appcontext 

from .extensions import db, bcrypt 
from .models import User, Recipe, Step, StepIngredient


@click.command(name='create_tables')
@with_appcontext 
def create_tables(): 
    db.create_all() 
    
    
@click.command(name='seed_db')
@with_appcontext 
def seed_db(): 
    hashed_pw = bcrypt.generate_password_hash('pw123').decode('utf-8')
    sample_user = User('Sample', 'sample@domain.com', hashed_pw)
    db.session.add(sample_user)
    db.session.commit() 
    
    sample_recipe = Recipe('Sample Recipe', sample_user.id)
    db.session.add(sample_recipe)
    db.session.commit() 
    
    recipe_id = sample_recipe.id

    step1_notes = '''
    Mix the levain. Add 50g of 50% hydration mature starter (50/50 flour water ratio) to a bowl.
    Add an additional 25g bread flour and 25g water. Mix until all ingredients are incorporated and 
    let rest overnight for 12 hours.  
    '''
    step1 = Step(1, 12, 0, step1_notes, recipe_id)
    db.session.add(step1)
    db.session.commit()
    sample_recipe.total_minutes = 12 * 60
    
    step1_flour = StepIngredient(step_id=step1.id, ingredient='BREAD FLOUR', weight=50)
    step1_water = StepIngredient(step_id=step1.id, ingredient='WATER', weight=50)
    db.session.add_all([step1_flour, step1_water])
    db.session.commit() 
    
    step2_notes = '''
    Combine 800g bread flour with 100g whole wheat flour in a large bowl. Add 585g water and mix until a shaggy dough forms.
    Add the levain from step 1. Squeeze and pinch while mixing to combine doughs. Allow to autolyse for 20 minutes. After autolysing, the dough should appear smoother and plumper as the flour has 
    had time absorb the water. 
    '''
    step2 = Step(2,0,20, step2_notes, recipe_id)
    db.session.add(step2) 
    db.session.commit() 
    sample_recipe.total_minutes += 20
    
    step2_flour = StepIngredient(step_id=step2.id, ingredient='BREAD FLOUR', weight=800)
    step2_wwflour = StepIngredient(step_id=step2.id, ingredient='WHOLE WHEAT FLOUR', weight=100)
    step2_water = StepIngredient(step_id=step2.id, ingredient='WATER', weight=585)
    
    db.session.add_all([step2_flour, step2_wwflour, step2_water])
    db.session.commit() 
    
    step3_notes = ''' 
    Measure 20g salt and mix with 30g water to dissolve. 
    Add mixture to bowl and combine completely with the dough. 
    ''' 
    step3 = Step(3, 0,10, step3_notes, recipe_id) 
    db.session.add(step3)
    db.session.commit() 
    sample_recipe.total_minutes += 10
    
    step3_salt = StepIngredient(step_id=step3.id, ingredient='SALT', weight=20)
    step3_water = StepIngredient(step_id=step3.id, ingredient='WATER', weight=30)
    db.session.add_all([step3_salt, step3_water])
    db.session.commit() 
    
    step4_notes = '''
    Knead the dough using a slap and fold technique. Using the table as an anchoring point for the dough, 
    pull the dough towards yourself and fold back over. 
    Flip the dough 90 degrees, anchor on the table, and stretch again. 
    Take care to not split the dough. 
    Knead for 30 minutes or until the dough is smooth and highly elastic. 
    ''' 
    step4 = Step(4, 0, 30, step4_notes, recipe_id)
    db.session.add(step4)
    db.session.commit() 
    sample_recipe.total_minutes += 30
    
    step5_notes = '''
    Begin bulk fermentation. Cover dough and allow it to rise in a warm place. 
    After 30 minutes, perform first stretch and fold. Using a hand to scoop under the dough, 
    stretch the dough gently up, shaking carefully to allow further stretching. Do not break the dough. 
    Fold the stretched portion of the dough over the top of the remaining dough. 
    Turn the bowl 90 degrees and repeat the stretch and fold process four times. 
    '''
    step5 = Step(5, 0, 30, step5_notes, recipe_id) 
    db.session.add(step5) 
    db.session.commit() 
    sample_recipe.total_minutes += 30
    
    step6_notes = 'Rest for another 30 minutes and repeat the stretch and fold.'
    step6 = Step(6, 0, 30, step6_notes, recipe_id) 
    db.session.add(step6)
    db.session.commit() 
    sample_recipe.total_minutes += 30
    
    step7_notes = 'Rest for another hour and do one last stretch and fold'
    step7 = Step(7, 1, 0, step7_notes, recipe_id)
    db.session.add(step7) 
    db.session.commit() 
    sample_recipe.total_minutes += 60
    
    step8_notes = 'Allow the dough to rest for 2 hours'
    step8 = Step(8, 2, 0, step8_notes, recipe_id)
    db.session.add(step7) 
    db.session.commit() 
    sample_recipe.total_minutes += 120
    
    step9_notes = '''
    Divide the dough into two parts. Lightly shape each part into a round ball. 
    Let the dough rest for 20 minutes to relax the gluten for final shaping. 
    '''
    step9 = Step(9, 0, 20, step9_notes, recipe_id)
    db.session.add(step9) 
    db.session.commit() 
    sample_recipe.total_minutes += 20
    
    step10_notes = '''Pull the dough balls tightly into boules or batards. 
    Use a table or a bench scraper to help create tension in the rounds. 
    Place seam side up in a proofing basket dusted with rice flour to prevent sticking. 
    ''' 
    step10 = Step(10, 0, 10, step10_notes, recipe_id)
    db.session.add(step10) 
    db.session.commit() 
    sample_recipe.total_minutes += 10
    
    step11_notes = '''Place proofing baskets covered in the fridge for 12 hours overnight. 
    The next morning, take the baskets out and allow them to come to room temperature as the oven is heated. 
    Score the top of the loaves to allow the bread the release steam in the oven
    ''' 
    step11 = Step(11, 12, 30, step11_notes, recipe_id)
    db.session.add(step11) 
    db.session.commit() 
    sample_recipe.total_minutes += 12 * 60 + 30
    
    step12_notes = '''Preheat a cast iron combo cooker at 485F and bake for rounds covered for 20 minutes. 
    Remove the cover and lower the heat to 425F. Bake for another 20-30 minutes or until golden brown. Let loaves cool 
    for at least 1 hour prior to slicing. 
    ''' 
    step12 = Step(12, 0, 45, step12_notes, recipe_id)
    db.session.add(step12) 
    db.session.commit()
    
    sample_recipe.total_minutes += 45
    sample_recipe.total_steps = 12
    db.session.commit() 