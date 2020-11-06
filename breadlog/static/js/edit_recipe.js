// Scripts for adding ingredients on recipe edit page 
document.addEventListener('DOMContentLoaded', function() {
    var data, url; 

    // Add new ingredient to step 
    document.querySelectorAll('.form-ingredient').forEach(item => {
        item.addEventListener('submit', (e) => addIngredientHandler.apply(item, [e]));
    }); 

    // Delete ingredient from step 
    document.querySelectorAll('.delete-step-ingredient').forEach(item => {
        item.addEventListener('click', deleteIngredientHandler);
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
        item.addEventListener('click', deleteStepHandler);
    }); 

    // On hover 
    document.querySelectorAll('.ingredient-list-table tr').forEach(item => {
        item.addEventListener('mouseenter', (e) => ingredientEnterEditHandler(e));
        item.addEventListener('mouseleave', (e) => ingredientLeaveEditHandler(e));
    });
});

function postData(url = '', data = {}) {
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
                if (resdata['action'] === 'add' && resdata['item'] === 'step') {
                    addStepToWindow(resdata);
                }
                // Add new ingredient to step ingredient list 
                else if (resdata['action'] === 'add' && resdata['item'] === 'ingredient') {
                    addIngredient(resdata); 
                }
                // Delete step 
                else if (resdata['action'] === 'delete' && resdata['item'] === 'step') {
                   removeStepFromWindow(resdata);
                }
                // Delete ingredient from step 
                else if (resdata['action'] === 'delete' && resdata['item'] === 'ingredient') {
                   removeIngredientFromStep(resdata);
                }

                else if (resdata['action'] === 'moveup') {
                    moveStepUp(resdata);
                }

                else if (resdata['action'] === 'movedown') {
                    moveStepDown(resdata);
                }
            }); 
        }
   });
}
// Event listener callback for adding ingredient to step
function addIngredientHandler(e) {
    e.preventDefault(); 
    url = `${window.origin}/step/${this.dataset.stepid}/add_step_ingredient`;
    data = {
        'ingredient': this.ingredient.value.toUpperCase(), 
        'weight': this.weight.value
    };
    postData(url, data);
    this.reset(); 
}

// Event listener callback for deleting ingredient from step
function deleteIngredientHandler() {
    let stepIngredientId = this.dataset.ingredientid; 
    let stepId = this.dataset.stepid;
    url = `${window.origin}/step/${stepId}/step_ingredient/${stepIngredientId}/delete`; 
    console.log(url);
    postData(url);
}

// Event listener callback for deleting step 
function deleteStepHandler() {
    let stepId = this.dataset.stepid;
    let url = `${window.origin}/delete_step/${stepId}`;
    postData(url);
}

// On hover show edit cell
function ingredientEnterEditHandler(e) {
    let editCols = e.target.getElementsByClassName('placeholder-hide'); 
    if (editCols.length === 1) {
        editCols[0].classList.add('placeholder-show');
        editCols[0].classList.remove('placeholder-hide');
    }
}

// On leave hover hide edit cell
function ingredientLeaveEditHandler(e) {
    let editCols = e.target.getElementsByClassName('placeholder-show'); 
    if (editCols.length === 1) {
        editCols[0].classList.add('placeholder-hide');
        editCols[0].classList.remove('placeholder-show');
    }
}

function moveStepUp() {

}

function moveStepDown() {

}

// Insert new ingredient into step ingredient list 
function addIngredient(data) {
    const table = document.getElementById(`ingredient-list-${data['step_id']}`);
    const row = table.insertRow(); 
    row.setAttribute('id', `row-${data['step_ingredient_id']}`);
    let ingrCell = row.insertCell(0); 
    let weightCell = row.insertCell(1);
    
    let editCell = row.insertCell(2);
    editCell.classList.add('edit-col', 'placeholder-hide');

    // let editIcon = document.createElement('i');
    // editIcon.classList.add('fa', 'fa-edit', 'edit-col-icon', 'edit-step-ingredient');
    
    let deleteIcon = document.createElement('i');
    deleteIcon.classList.add('fa','fa-times', 'edit-col-icon', 'delete-step-ingredient');
    deleteIcon.setAttribute('data-stepid', `${data['step_id']}`); 
    deleteIcon.setAttribute('data-ingredientid', `${data['step_ingredient_id']}`); 

    ingrCell.innerText = data['ingredient']; 
    weightCell.innerText = data['weight']; 
    // editCell.appendChild(editIcon);
    editCell.appendChild(deleteIcon);

    // Add event listeners 
    row.addEventListener('mouseenter', (e) => ingredientEnterEditHandler(e));
    row.addEventListener('mouseleave', (e) => ingredientLeaveEditHandler(e)); 
    deleteIcon.addEventListener('click', deleteIngredientHandler);
}

// Remove deleted ingredient from step ingredient list 
function removeIngredientFromStep(data) {
    document.getElementById(`row-${data['step_ingredient_id']}`).remove(); 
}

function removeStepFromWindow(data) {
    var stepNums = document.querySelectorAll('.step-number'); 
    for (i = 0; i < stepNums.length; i++) {
        if (stepNums[i].dataset.stepnum > data['step_number']) {
            stepNums[i].innerText -= 1;
        }
    }
    document.getElementById(`step-${data['step_id']}`).remove(); 
    document.getElementById(`break-${data['step_id']}`).remove(); 
}

function addStepToWindow(data) {
    const template = `<div class="col-12 recipe-step" id="step-${data['step_id']}" data-stepnum="${data['step_number']}">
                        <div class="row">
                            <div class="edit-button col-12">
                                <button class="step-action move-up" data-stepid="{{ step.id }}"><i class="fa fa-chevron-up"></i></button>
                                <button id="step-delete-${data['step_id']}" class="step-action step-delete" data-stepid="${data['step_id']}"><i class="fa fa-times"></i></button>
                            </div>
                        </div>
                            <div class="col-1">
                                <h3 class="step-number" data-stepnum="${data['step_number']}">${data['step_number']}</h3>
                            </div>
                            <div class="col-6">
                                <h4>${data['hours']} H ${data['minutes']} MIN</h4>
                                <div class="col-12 step-notes">
                                    <p>${data['notes']}</p>
                                </div>
                            </div>
                            <div class="col-4">
                                <br>
                                <table class="ingredient-list-table" id="ingredient-list-${data['step_id']}">
                                    <tr>
                                        <th>INGREDIENT</th>
                                        <th>WEIGHT (g)</th>
                                    </tr>
                                </table>
                                <div class="form-ingredient-div" id="ingredient-form-${data['step_id']}">
                                <br>
                                <form id="form-ingredient-${data['step_id']}" class="form-ingredient" data-stepid="${data['step_id']}" data-recipeid="-${data['recipe_id']}">
                                    <label for="ingredient">Add Ingredient to Step</label><br>
                                    <input class="ingredient-input" type="text" required name="ingredient" placeholder="INGREDIENT NAME">
                                    <input class="ingredient-input" type="number" required step=".01" min="0" name="weight" placeholder="WEIGHT IN GRAMS">
                                    <input class="ingredient-add-btn" type="submit" data-stepid="-${data['step_id']}" value="ADD">
                                </form>
                            </div>
                        </div>
                        <div class="col-12" id="break-${data['step_id']}"><br></div>`
                     
    const fragment = document.createRange().createContextualFragment(template);
    const currentEl = document.getElementById('new-step-form');
    currentEl.parentNode.insertBefore(fragment, currentEl);
    // Event listeners 
    document.querySelector(`#step-delete-${data['step_id']}`).addEventListener('click', deleteStepHandler);
    let addIngr = document.querySelector(`#form-ingredient-${data['step_id']}`);
    addIngr.addEventListener('submit', (e) => addIngredientHandler.apply(addIngr, [e]));
}