// Script for display recipe on recipe box page 

// Check that DOM has loaded and add onclick event for recipe names
document.addEventListener('DOMContentLoaded', () => {
    var buttons = document.querySelectorAll('button.recipe-name'); 
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function() {
            var url = 'recipe/id/' + this.dataset.name; 
            displayRecipe(url); 
        }; 
    }
}); 

function displayRecipe(url) {
    fetch(url).then(function(response) {
        console.log(response.json())
    });
}

    // // Make a HTTP get request for recipe information
    // function makeRequest(url) {
    //     httpRequest = new XMLHttpRequest();

    //     httpRequest.onreadystatechange = function() {
    //         if (httpRequest.readyState === XMLHttpRequest.DONE && httpRequest.status === 200) {
    //             var response = JSON.parse(httpRequest.responseText); 
    //             display(response);
    //         }
    //     }
    //     httpRequest.open('GET', url); 
    //     httpRequest.send(); 
    // }

    // // Hide current display in page and replace with updated recipe data 
    // function display(response) {
    //     // Hide default response 
    //     document.getElementById('placeholder').className = 'placeholder-hide';
    //     // Get the requested response div 
    //     let divElem = document.getElementById('requested-recipe'); 
    //     // Remove any requested steps
    //     let stepDiv = document.getElementById('steps');
    //     stepDiv.innerHTML = '';
    //     //Show the requested response 
    //     divElem.className = 'placeholder-show';
    //     // Populate new recipe title
    //     let title = document.getElementById('recipe-name'); 
    //     title.innerText = response['name'];

    //     let timeElem = document.getElementById('recipe-min'); 
    //     timeElem.innerText = 'Total time: ' + response['total_minutes'] +  ' minutes';
        
    //     for (var i=0; i < response['steps'].length; i++) {
    //         let stepTitle = document.createElement('h4')
    //         stepTitle.innerText = "Step " + response['steps'][i]['step_number'] + ": " + response['steps'][i]['action']; 
    //         stepDiv.appendChild(stepTitle);
            
    //         let stepTime = document.createElement('p'); 
    //         stepTime.innerText = 'Time: ' + response['steps'][i]['minutes'] + ' minutes  START TIMER';
    //         stepDiv.appendChild(stepTime);
    //     }
    // }