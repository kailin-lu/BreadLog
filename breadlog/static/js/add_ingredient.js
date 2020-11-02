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

    // Show delete button on hover 
    document.querySelectorAll('tr').forEach(item => {
        item.addEventListener('hover', function() {
            // flip child nodes with placeholder-hide 
        });
    })

    // Edit existing ingredients 
    document.querySelectorAll('.step-ingredient').forEach(item => {
        item.ondblclick = dblClickToEditIngredient;
    }); 

    // Delete ingredient from step 
    document.querySelectorAll('').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); 

    }); 

    // Add step to recipe 
    document.getElementById().addEventListener('click', function(e) {
        e.preventDefault(); 
    }); 

    // Delete step from recipe 
});

function postData(url = '', data = {}, stepId = '') {
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

function dblClickToEditIngredient() {
    // Replace ingredient row with input 
    const template = `${this.childNodes[0].innerText}`; 
    console.log(template);
}
