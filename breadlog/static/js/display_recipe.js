// Script for display recipe on recipe box page 

// Check that DOM has loaded and add onclick event for recipe names
document.addEventListener('DOMContentLoaded', () => {
    // Calculate finish time from now 
    finishTime();

    var buttons = document.querySelectorAll('.box-recipe'); 
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function() {
            var url = 'recipe/id/' + this.dataset.recipeid; 
            displayRecipe(url); 
        }; 
    }

    // Calculate start time from user input
    let inputTimeEl = document.querySelector('#input-time');
    startTime.call(inputTimeEl);
    inputTimeEl.addEventListener('change', startTime); 
}); 

function displayRecipe(url) {
    fetch(url).then(function(response) {
        response.json().then(function(resdata) {
            // Replace Title 
            document.querySelector('#recipe-name').innerHTML = resdata['name'];

            // Replace total time 
            let total_minutes = parseInt(resdata['total_minutes']); 
            let hours = parseInt(total_minutes / 60); 
            let minutes = total_minutes % 60; 
            document.querySelector('#hours').innerText = `${hours}`;
            document.querySelector('#minutes').innerText = `${minutes}`;

            // Recalculate start and finish times 
            let inputTimeEl = document.querySelector('#input-time');
            startTime.call(inputTimeEl);
            finishTime(); 

            // Replace ingredients table 
            let ingredientTable = document.getElementById('ingredients-total-edit');  
            let rows = ingredientTable.rows.length;
            for (i = 1; i < rows; i++) {
                ingredientTable.deleteRow(-1);
            }
            let ingredientData = collectIngredients(resdata['steps']);
            let ingredients = Object.keys(ingredientData[0]); 
            let ingredientCount = ingredients.length; 
            var row, ingr, weight, pct; 
            for (i = 0; i < ingredientCount; i++) {
                row = ingredientTable.insertRow();
                
                ingr = row.insertCell(0); 
                weight = row.insertCell(1); 
                pct = row.insertCell(2); 

                ingr.innerHTML = ingredients[i];
                weight.innerHTML = ingredientData[0][ingredients[i]] + ' g';
                pct.innerHTML = ingredientData[1][ingredients[i]] + '%';
            }

            // Replace steps 
            let stepsDiv = document.getElementById('steps'); 
            while (stepsDiv.firstChild) {
                stepsDiv.removeChild(stepsDiv.firstChild);
            }

            let stepCount = resdata['steps'].length; 
            if (stepCount === 0) {
                stepsDiv.append('No steps have been added. Please edit recipe to add steps.');
            }

            for (i = 0; i < stepCount; i++) {
                buildStep(resdata['steps'][i], stepsDiv); 
                addIngredients(resdata['steps'][i]);

            }
        }); 
    });
}

function finishTime() {
    let hours = parseInt(document.querySelector('#hours').innerText);
    let minutes = parseInt(document.querySelector('#minutes').innerText);
    let now = dayjs(); 
    let finish = now.add(hours, 'hours')
    finish = finish.add(minutes, 'minutes'); 
    document.querySelector('#calculated-finish').innerText = `If starting now, this recipe will finish on approximately ${finish.format('MMM-DD h:mm A')}`
}


function startTime() {
    let val = this.value.split(':');
    let hours = parseInt(val[0]); 
    let minutes = parseInt(val[1]);
    let start = dayjs(); 
    start = start.set('hour', hours); 
    start = start.set('minute', minutes); 

    let recipeHours = parseInt(document.querySelector('#hours').innerText); 
    let recipeMinutes = parseInt(document.querySelector('#minutes').innerText); 
    start = start.subtract(recipeHours, 'hours'); 
    start = start.subtract(recipeMinutes, 'minutes'); 
    document.querySelector('#calculated-start').innerText = `today start at ${start.format('MMM-DD h:mm A')}`;
}

function buildStep(step, stepsDiv) { 
    const template = `<div class="display-step" id="display-step-${step['id']}">
                    <h1 class="display-stepnum">${step['step_number']}</h1>
                    <h5 class="display-time">TIME: ${step['hours']} HOURS ${step['minutes']} MINUTES</h5>
                    <ul class="ingr-list" id="ingr-list-${step['id']}">
                    </ul>
                    <p class="display-notes">${step['notes']}</p>
                </div>`;

    const fragment = document.createRange().createContextualFragment(template); 
    stepsDiv.append(fragment); 
}

function addIngredients(step) {
    let ingredientCount = step['ingredients'].length; 
    const listEl = document.querySelector(`#ingr-list-${step['id']}`); 
    step['ingredients'].forEach(item => {
        if (item) {
            let listItem = document.createElement('li');
            listItem.innerText = item['ingredient'] + ' ' + item['weight'] + 'g'; 
            listEl.append(listItem);
        }
    })
}

// Aggregates ingredients 
// Calculates baker's percentage off of total ingredients with 'FLOUR' in name 
function collectIngredients(steps) {
    let flourWeight = 0; 
    let ingredients = {};
    let percents = {}; 
    let ingr, weight; 
    for (i = 0; i < steps.length; i++) {
        for (j = 0; j < steps[i]['ingredients'].length; j++) {
            ingr = steps[i]['ingredients'][j]['ingredient'];
            weight = parseFloat(steps[i]['ingredients'][j]['weight']);
            if (ingr in ingredients) {
                ingredients[ingr] += weight; 
            }
            else {
                ingredients[ingr] = weight; 
            }
            if (ingr.includes('FLOUR')) {
                flourWeight += weight; 
            }
        }
    }
    for (key in ingredients) {
        ingredients[key] = Number(ingredients[key]).toFixed(1);
        percents[key] = Number(ingredients[key]*100 / flourWeight).toFixed(1); 
    }
    return [ingredients, percents];
}
