// static/js/app.js

// --- PHASE 2: Pantry Variables ---
const pantry = [];
const ingredientForm = document.getElementById('add-ingredient-form');
const ingredientInput = document.getElementById('ingredient-input');
const pantryTagsContainer = document.getElementById('pantry-tags');

// --- PHASE 3 & 4: Results & Button Variables ---
const findRecipesBtn = document.getElementById('find-recipes-btn');
const viewFavoritesBtn = document.getElementById('view-favorites-btn');
const loadingSpinner = document.getElementById('loading-spinner');
const resultsTitle = document.getElementById('results-title');
const resultsGrid = document.getElementById('recipe-results-grid');


// --- PHASE 2: Add Ingredient Form Listener ---
ingredientForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const ingredient = ingredientInput.value.trim().toLowerCase();
    if (ingredient && !pantry.includes(ingredient)) {
        pantry.push(ingredient);
        renderPantryTags();
        ingredientInput.value = "";
    }
});

// --- PHASE 2: Render Pantry Tags Function ---
function renderPantryTags() {
    pantryTagsContainer.innerHTML = "";
    pantry.forEach(ingredient => {
        const tag = document.createElement('span');
        tag.className = 'pantry-tag';
        tag.textContent = ingredient;
        const removeBtn = document.createElement('button');
        removeBtn.className = 'pantry-tag-remove';
        removeBtn.textContent = '×';
        removeBtn.addEventListener('click', function() {
            const index = pantry.indexOf(ingredient);
            if (index > -1) pantry.splice(index, 1);
            renderPantryTags();
        });
        tag.appendChild(removeBtn);
        pantryTagsContainer.appendChild(tag);
    });
}

// --- PHASE 3: Find Recipes Button Listener ---
findRecipesBtn.addEventListener('click', async function() {
    if (pantry.length === 0) {
        alert("Please add some ingredients to your pantry first!");
        return;
    }
    console.log("Finding recipes for:", pantry);
    loadingSpinner.style.display = 'block';
    resultsTitle.style.display = 'block';
    resultsTitle.textContent = "Your Recipe Ideas";
    resultsGrid.innerHTML = "";

    try {
        const response = await fetch('/api/find_recipes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ingredients: pantry })
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        loadingSpinner.style.display = 'none';
        if (data.success && data.recipes.length > 0) {
            renderRecipes(data.recipes, 'search'); // Pass 'search' type
        } else if (data.success) {
            resultsGrid.innerHTML = "<p>No recipes found. Try adding more ingredients!</p>";
        } else {
            resultsGrid.innerHTML = `<p>Error: ${data.error}</p>`;
        }
    } catch (error) {
        console.error("Error fetching recipes:", error);
        loadingSpinner.style.display = 'none';
        resultsGrid.innerHTML = "<p>An error occurred fetching recipes.</p>";
    }
});

// --- PHASE 4: View Favorites Button Listener ---
viewFavoritesBtn.addEventListener('click', async function() {
    console.log("Loading favorites...");
    loadingSpinner.style.display = 'block';
    resultsTitle.style.display = 'block';
    resultsTitle.textContent = "Your Favorite Recipes";
    resultsGrid.innerHTML = "";

    try {
        const response = await fetch('/api/favorites'); // GET request
        const data = await response.json();
        loadingSpinner.style.display = 'none';
        if (data.success && data.favorites.length > 0) {
            const favoriteRecipes = data.favorites.map(fav => ({
                id: fav._id, // Comes from DB as _id (now a string)
                title: fav.title,
                image: fav.image,
                used_ingredients_count: 'Saved', // Placeholder text
                missed_ingredients_count: 'Favorite' // Placeholder text
            }));
            renderRecipes(favoriteRecipes, 'favorites'); // Pass 'favorites' type
        } else if (data.success) {
            resultsGrid.innerHTML = "<p>You haven't saved any favorites yet!</p>";
        } else {
             resultsGrid.innerHTML = `<p>Error: ${data.error || 'Could not load favorites.'}</p>`;
        }
    } catch (error) {
        console.error("Error fetching favorites:", error);
        loadingSpinner.style.display = 'none';
        resultsGrid.innerHTML = "<p>An error occurred fetching favorites.</p>";
    }
});


// --- PHASE 3 & 4: Render Recipe Cards Function (NOW WITH REMOVE BUTTON) ---
function renderRecipes(recipes, type = 'search') {
    resultsGrid.innerHTML = "";

    recipes.forEach(recipe => {
        const card = document.createElement('article');
        const recipeId = recipe.id; // Correct ID for both search and favorites
        const recipeTitle = recipe.title;
        const recipeImage = recipe.image;

        // --- Create dynamic footer content ---
        let footerContent = '';
        if (type === 'search') {
            // Search result: Show "Save" button
            footerContent = `
                <button class="save-btn"
                        data-id="${recipeId}"
                        data-title="${recipeTitle}"
                        data-image="${recipeImage}">
                    Save to Favorites
                </button>
            `;
        } else { // type === 'favorites'
            // Favorite result: Show "Remove" button
            footerContent = `
                <button class="remove-btn secondary"
                        data-id="${recipeId}">
                    Remove
                </button>
            `;
        }

        // Create the card's inner HTML
        card.innerHTML = `
            <img src="${recipe.image}" alt="${recipe.title}">
            <h5 class="recipe-title">${recipe.title}</h5>
            <p>
                <small>
                    <strong>Uses:</strong> ${recipe.used_ingredients_count}<br>
                    <strong>Missing:</strong> ${recipe.missed_ingredients_count}
                </small>
            </p>
            <footer>
                ${footerContent}
            </footer>
        `;
        resultsGrid.appendChild(card);
    });

    // --- Attach event listeners ---
    // Add listeners ONLY to save buttons (if any exist)
    document.querySelectorAll('.save-btn').forEach(button => {
        button.addEventListener('click', function() {
            const recipeData = {
                id: this.dataset.id,
                title: this.dataset.title,
                image: this.dataset.image
            };
            saveRecipe(recipeData, this);
        });
    });

    // Add listeners ONLY to remove buttons (if any exist)
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function() {
            const recipeId = this.dataset.id; // Get the ID from the button
            removeFavorite(recipeId, this); // Call the new remove function
        });
    });
}


// --- PHASE 4: Save Recipe Function ---
async function saveRecipe(recipeData, buttonElement) {
    console.log("Saving recipe:", recipeData);
    try {
        const response = await fetch('/api/favorites', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(recipeData)
        });
        const result = await response.json();
        if (result.success) {
            buttonElement.textContent = "Saved!";
            buttonElement.disabled = true;
        } else {
             console.error("Failed to save:", result.message);
            buttonElement.textContent = "Error!";
        }
    } catch (error) {
         console.error("Error saving recipe:", error);
        buttonElement.textContent = "Error!";
    }
}


// --- NEW: Remove Favorite Function (WITH LOGGING ADDED) ---
async function removeFavorite(recipeId, buttonElement) {
    // --- THIS LOG IS NOW ADDED ---
    console.log("Remove button clicked for recipe ID:", recipeId, "Type:", typeof recipeId);
    // --- END ADD ---

    const cardElement = buttonElement.closest('article');
    if (cardElement) cardElement.style.opacity = '0.5'; // Dim card

    try {
        const url = `/api/favorites/${recipeId}`; // Construct URL with ID
        const response = await fetch(url, { method: 'DELETE' }); // Use DELETE
        const result = await response.json();

        if (result.success) {
            console.log(result.message);
            if (cardElement) cardElement.remove(); // Remove card from page
        } else {
            console.error("Failed to remove:", result.message);
             if (cardElement) cardElement.style.opacity = '1'; // Revert dim
            alert(`Error removing favorite: ${result.message}`);
        }
    } catch (error) {
        console.error("Error removing recipe:", error);
         if (cardElement) cardElement.style.opacity = '1';
        alert("An error occurred. Please try again.");
    }
}