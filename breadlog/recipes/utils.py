from flask import make_response, jsonify
from collections import defaultdict 
from sqlalchemy.exc import SQLAlchemyError


def make_err_response(e): 
    """Helper to return error type and route parameters"""
    err = {
            'orig': str(e.orig), 
            'params': str(e.params)
        }
    return make_response(jsonify(err), 404)


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