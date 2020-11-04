// Scripts for adding ingredients on recipe edit page 

document.addEventListener('DOMContentLoaded', function() {
    // Add new ingredient to step 
    document.querySelectorAll('.form-ingredient').forEach(item => {
        item.addEventListener('submit', function(e) {
            e.preventDefault(); 
            let stepId = this.dataset.stepid;
            let url = `${window.origin}/step/${stepId}/add_step_ingredient`;
            let data = {
                'ingredient': this.ingredient.value.toUpperCase(), 
                'weight': this.weight.value
            }
            postData(url, data, stepId);
        }); 
    }); 

    // Delete ingredient from step 
    document.querySelectorAll('.step-delete').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); 
            let stepId = this.dataset.stepid; 
            let stepNumber = this.dataset.stepnum;
            let url = `${window.origin}/step_ingredient/${stepId}/delete_step_ingredient`; 
            data = {
                'stepNumber': stepNumber
            }
            postData(url, data, stepId=stepId, itemToDelete='ingredient');
        })
    });

    // Add step to recipe 
    document.getElementById('add-new-step').addEventListener('submit', function(e) {
        e.preventDefault(); 
        let recipeId = this.dataset.recipeid;
        let steps = this.dataset.steps;
        let url = `${window.origin}/recipes/${recipeId}/add_step`;

        let data = {
            'step_number': steps + 1,
            'hours': this.hours.value || 0,
            'minutes': this.minutes.value || 0, 
            'notes': this.notes.value,
            'recipe_id': recipeId
        }
        postData(url, data);
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
            postData(url, data={}, stepId, itemToDelete='step')
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
            console.log(response); 
            return
        }
        else {
            // If ingredient in data, add to ingredient list
            if ('ingredient' in data) {
                updateIngredients(data, stepId); 
            }
            // Add step 
            else if ('notes' in data) {
                addStepToWindow(data); 
            }
            // Remove step 
            else if (itemToDelete === 'step') {
                removeStepFromWindow(data, stepId);
            }
        }
   });
}

function updateIngredients(data, stepId) {
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
                            <div class="col-1">
                                 <h3 class="step-number" data-stepnum="{{ step.step_number }}">${data['step_number']}</h3>
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

function removeStepFromWindow(data, stepId) {
    let elementId = `step-${stepId}`;
    // Update step numbers in other steps 
    document.querySelectorAll('.step-number').forEach(item => {
        if (item.dataset.stepnum > data['stepNumber']) {
            item.dataset.stepnum -= 1;
            item.innerText = item.dataset.stepnum;
        }
    }); 
    document.getElementById(`step-${stepId}`).remove(); 
}