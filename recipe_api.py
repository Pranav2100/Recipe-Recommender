# recipe_api.py
import requests
import logging
from config import SPOONACULAR_API_KEY, SPOONACULAR_BASE_URL

CONFIG_PLACEHOLDER = "574c4f7ca2844856b4988a72af131983"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecipeAPI:
    def __init__(self):
        """Initialize the Recipe API handler."""
        self.api_key = SPOONACULAR_API_KEY
        self.base_url = SPOONACULAR_BASE_URL

    def find_by_ingredients(self, ingredients_list, number_to_return=10):
        """
        ... (docstring) ...
        """

        ingredients_str = ",".join(ingredients_list)

        endpoint = f"{self.base_url}/recipes/findByIngredients"

        params = {
            'apiKey': self.api_key,
            'ingredients': ingredients_str,
            'number': number_to_return,
            'ranking': 1 
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status() 
            recipes = response.json()
            logger.info(f"Successfully fetched {len(recipes)} recipes.")
            return self.parse_recipe_data(recipes)

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                logger.error("HTTP 401 Error: Invalid API Key. Check config.py.")
            else:
                logger.error(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while fetching recipe data: {e}")
            return None

    def parse_recipe_data(self, raw_recipes):
        """
        ... (docstring) ...
        """
        parsed_list = []
        for recipe in raw_recipes:
            parsed_list.append({
                'id': recipe.get('id'),
                'title': recipe.get('title'),
                'image': recipe.get('image'),
                'used_ingredients_count': len(recipe.get('usedIngredients', [])),
                'missed_ingredients_count': len(recipe.get('missedIngredients', []))
            })
        return parsed_list

if __name__ == "__main__":
    print("Testing RecipeAPI class...")
    api = RecipeAPI()

    test_ingredients = ["apples", "flour", "sugar"]
    recipes = api.find_by_ingredients(test_ingredients)

    if recipes:
        print(f"\nSuccessfully found {len(recipes)} recipes:")
        for r in recipes:
            print(f"  - {r['title']} (Misses {r['missed_ingredients_count']} ingredients)")
    else:
        print("\nFailed to get recipes. Check your API key in config.py.")