document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const ingredients = document.getElementById('ingredients').value.split(',').map(ingredient => ingredient.trim());

    fetch('/search_recipes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ingredients: ingredients })
    })
    .then(response => response.json())
    .then(data => {
        const recipeList = document.getElementById('recipe-list');
        recipeList.innerHTML = ''; // Clear previous results

        if (data.matching_recipes.length > 0) {
            data.matching_recipes.forEach(recipe => {
                const li = document.createElement('li');
                li.textContent = recipe;
                recipeList.appendChild(li);
            });
        } else {
            recipeList.innerHTML = '<li>No recipes found</li>';
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('add-recipe-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('recipe-name').value;
    const ingredients = document.getElementById('recipe-ingredients').value;
    const instructions = document.getElementById('recipe-instructions').value;

    const formData = new FormData();
    formData.append('name', name);
    formData.append('ingredients', ingredients);
    formData.append('instructions', instructions);

    fetch('/add_recipe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        alert('Recipe added successfully!');
        document.getElementById('add-recipe-form').reset();
    })
    .catch(error => console.error('Error:', error));
});
