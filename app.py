# app.py
from flask import Flask, jsonify, render_template, request
from recipe_api import RecipeAPI
from db_handler import DatabaseHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

try:
    recipe_api = RecipeAPI()
    logger.info("RecipeAPI initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize RecipeAPI: {e}")
    recipe_api = None

try:
    db = DatabaseHandler()
    db.test_connection()
    logger.info("DatabaseHandler initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize DatabaseHandler: {e}")
    db = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/find_recipes', methods=['POST'])
def api_find_recipes():
    if not recipe_api:
        return jsonify({'success': False, 'error': 'RecipeAPI not initialized.'}), 500
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        if not ingredients:
            return jsonify({'success': False, 'error': 'No ingredients provided.'}), 400
        logger.info(f"Fetching recipes for: {', '.join(ingredients)}")
        recipes = recipe_api.find_by_ingredients(ingredients)
        if recipes is not None:
            return jsonify({'success': True, 'recipes': recipes})
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch recipes from API.'}), 500
    except Exception as e:
        logger.exception(f"Error in /api/find_recipes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """Adds a recipe to the favorites in the database."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not connected.'}), 500
    
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({'success': False, 'error': 'Invalid recipe data.'}), 400
        
    result = db.add_favorite_recipe(data)
    return jsonify(result)


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Gets all favorite recipes from the database."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not connected.'}), 500
        
    favorites = db.get_favorite_recipes()
    return jsonify({'success': True, 'favorites': favorites})

@app.route('/api/test-recipes')
def get_test_recipes():
    if not recipe_api:
        return jsonify({'success': False, 'error': 'RecipeAPI not initialized.'}), 500
    try:
        ingredients = ["chicken", "rice", "tomato"]
        recipes = recipe_api.find_by_ingredients(ingredients)
        if recipes is not None:
            return jsonify({'success': True, 'recipes': recipes})
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch recipes.'}), 500
    except Exception as e:
        logger.exception(f"Error in /api/test-recipes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/favorites/<recipe_id_str>', methods=['DELETE'])
def remove_favorite(recipe_id_str):
    """Removes a recipe from the favorites in the database."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not connected.'}), 500
    
    result = db.delete_favorite_recipe(recipe_id_str)
    
    if result['success']:
        return jsonify(result), 200
    else:
        status_code = 404 if "not found" in result.get('message', '').lower() else 500
        return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)