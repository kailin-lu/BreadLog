// Scripts for adding ingredients on recipe edit page 

document.addEventListener('DOMContentLoaded', function() {
    var data; 
    var stepId; 
    var url; 

    // Add new ingredient to step 
    document.querySelectorAll('.form-ingredient').forEach(item => {
        item.addEventListener('submit', function(e) {
            e.preventDefault(); 
            stepId = this.dataset.stepid;
            url = `${window.origin}/step/${stepId}/add_step_ingredient`;
            data = {
                'ingredient': this.ingredient.value.toUpperCase(), 
                'weight': this.weight.value
            }
            postData(url, data, stepId);
        }); 
    }); 

    // Delete ingredient from step 
    document.querySelectorAll('.delete-step-ingredient').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); 
            let stepIngredientId = this.dataset.step-ingredient-id; 
            let stepNumber = this.dataset.stepnum;
            url = `${window.origin}/step_ingredient/${stepIngredientId}/delete_step_ingredient`; 
            data = {'stepNumber': stepNumber}
            postData(url, data, stepId='', itemToDelete='ingredient');
        })
    });

    // Add step to recipe 
    document.getElementById('add-new-step').addEventListener('submit', function(e) {
        e.preventDefault(); 
        let recipeId = this.dataset.recipeid;
        let steps = this.dataset.steps;
        let url = `${window.origin}/recipes/${recipeId}/add_step`;

        let data = {
            'step_number': parseInt(steps) + 1,
            'hours': this.hours.value || 0,
            'minutes': this.minutes.value || 0, 
            'notes': this.notes.value,
            'recipe_id': recipeId
        }
        postData(url, data);
        this.reset(); 
    }); 

    // Delete step from recipe 
    document.querySelectorAll('.step-delete').forEach(item => {
        item.addEventListener('click', function(e) {
            let stepId = this.dataset.stepid;
            let url = `${window.origin}/delete_step/${stepId}`;
            let stepNumber = this.dataset.stepnum;
            data = {
                'stepNumber': stepNumber
            }
            postData(url, data=data, stepId, itemToDelete='step')
        })
    }); 

    // On hover 
    document.querySelectorAll('.ingredient-list-table tr').forEach(item => {
        item.addEventListener('mouseenter', function(event) {
            let editCols = event.target.getElementsByClassName('placeholder-hide'); 
            if (editCols.length === 1) {
                editCols[0].classList.add('placeholder-show');
                editCols[0].classList.remove('placeholder-hide');
            }
        });

        item.addEventListener('mouseleave', function(event) {
            let editCols = event.target.getElementsByClassName('placeholder-show'); 
            if (editCols.length === 1) {
                editCols[0].classList.add('placeholder-hide');
                editCols[0].classList.remove('placeholder-show');
            }
        });
    });
});

function postData(url = '', data = {}, stepId = '', itemToDelete = '') {
    fetch(url, {
       method: 'POST', 
       cors: 'same-origin',
       headers: {
           'Content-Type': 'application/json'
       }, 
       body: JSON.stringify(data), 
       cache: 'no-cache'
   }).then(function (response) {
        if (response.status !== 200) {
            return
        }
        else {
            response.json().then(function(resdata) {
                // Add step card to window 
                if ('notes' in resdata) {
                    addStepToWindow(resdata); 
                }
                // Add new ingredient to step ingredient list 
                else if ('ingredient' in resdata) {
                    //addIngredient(data, stepId); 
                }
                // Delete step 
                else if (itemToDelete === 'step') {
                   removeStepFromWindow(resdata)
                }
                // Delete ingredient from step 
                else if (itemToDelete === 'ingredient') {
                    //remoteIngredientFromWindow
                }
            }); 
        }
   });
}

function addIngredient(data, stepId) {
    // Insert new ingredient into step ingredient list 
    const tableRow = document.createElement('tr');

    const ingredientNode = document.createElement('td');
    ingredientNode.innerText = data['ingredient']; 

    const weightNode = document.createElement('td'); 
    weightNode.innerText = data['weight']; 

    tableRow.append(ingredientNode); 
    tableRow.append(weightNode); 

    document.getElementById(`ingredient-form-${stepId}`).append(tableRow);
    // Recalculate ingredient totals at top 
}

function addStepToWindow(data) {
    const template = `<div class="col-12 recipe-step">
                        <div class="row">
                            <div class="edit-button col-12">
                                <button class="step-action step-delete" data-stepid="${data['step_id']}"><i class="fa fa-times"></i></button>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-1">
                                 <h3 class="step-number" data-stepnum="${data['step_number']}">${data['step_number']}</h3>
                            </div>
                            <div class="col-6">
                                <h4>${data['hours']} H ${data['minutes']} MIN</h4>
                                <div class="col-12 step-notes">
                                    <p>${data['notes']}</p>
                                </div>
                            </div>
                        </div>
                        <div class="row"></div>
                      </div>
                      <div class="col-12"><br></div>`
    const fragment = document.createRange().createContextualFragment(template);
    const currentEl = document.getElementById('new-step-form');
    currentEl.parentNode.insertBefore(fragment, currentEl);
}

function removeStepFromWindow(data) {
    let elementId = `step-${data['step_id']}`;
    var stepNums = document.querySelectorAll('.step-number'); 
    for (i = 0; i < stepNums.length; i++) {
        if (stepNums[i].dataset.stepnum > data['step_number']) {
            stepNums[i].innerText -= 1;
        }
    }
    document.getElementById(`step-${data['step_id']}`).remove(); 
}