// Script for display recipe on recipe box page 

// Check that DOM has loaded and add onclick event for recipe names
document.addEventListener('DOMContentLoaded', () => {
    var buttons = document.querySelectorAll('.box-recipe'); 
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function() {
            var url = 'recipe/id/' + this.dataset.recipeid; 
            displayRecipe(url); 
        }; 
    }
}); 

function displayRecipe(url) {
    fetch(url).then(function(response) {
        response.json().then(function(resdata) {
            console.log(resdata);
        }); 
    });
}