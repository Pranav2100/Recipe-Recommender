# db_handler.py
import pymongo
from pymongo import MongoClient
from datetime import datetime
import logging
from config import MONGO_URI, DATABASE_NAME # We defined these in config.py

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define collection names
FAVORITES_COLLECTION = "favorite_recipes"

class DatabaseHandler:
    def __init__(self):
        """Initialize MongoDB connection."""
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DATABASE_NAME]
            self.favorites_collection = self.db[FAVORITES_COLLECTION]
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def test_connection(self):
        """Test database connection."""
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    def add_favorite_recipe(self, recipe_data):
        """
        Adds a new recipe to the favorites collection.
        We use 'update_one' with 'upsert=True' to prevent duplicates.
        """
        try:
            # Use the recipe ID as the unique _id
            # Spoonacular IDs are integers, ensure we get an integer
            try:
                 recipe_id_int = int(recipe_data.get('id'))
            except (ValueError, TypeError):
                 logger.error(f"Invalid recipe ID received for saving: {recipe_data.get('id')}")
                 return {'success': False, 'message': 'Invalid recipe ID format for saving.'}

            query = {'_id': recipe_id_int} # Use the integer ID

            # --- ADDED THIS LOG ---
            logger.info(f"Attempting to save/update favorite with _id: {query['_id']} (Type: {type(query['_id'])})")
            # --- END ADD ---

            # Data to be inserted or updated
            update_data = {
                '$set': {
                    'title': recipe_data.get('title'),
                    'image': recipe_data.get('image'),
                    'added_at': datetime.utcnow()
                }
            }

            # 'upsert=True' means: if it doesn't exist, insert it.
            result = self.favorites_collection.update_one(query, update_data, upsert=True)

            if result.upserted_id:
                logger.info(f"Recipe {recipe_id_int} added to favorites.")
                return {'success': True, 'message': 'Recipe added to favorites.'}
            elif result.matched_count > 0:
                logger.info(f"Recipe {recipe_id_int} is already a favorite.")
                return {'success': True, 'message': 'Recipe is already a favorite.'}
            else:
                 # This case should ideally not happen with upsert=True unless there's an error
                return {'success': False, 'message': 'Failed to add recipe (unknown issue).'}

        except Exception as e:
            logger.error(f"Error adding favorite recipe: {e}")
            return {'success': False, 'message': str(e)}

    def get_favorite_recipes(self, limit=50):
        """Retrieve all favorite recipes from the database."""
        try:
            cursor = self.favorites_collection.find().sort('added_at', -1).limit(limit)
            # Convert ObjectId _id to string for JSON serialization
            favorites = []
            for doc in cursor:
                doc['_id'] = str(doc['_id']) # Convert ObjectId to string
                favorites.append(doc)
            return favorites # Return the list with string IDs
        except Exception as e:
            logger.error(f"Error retrieving favorite recipes: {e}")
            return []

    def delete_favorite_recipe(self, recipe_id_str):
        """Deletes a recipe from the favorites collection by its ID."""
        try:
            # Spoonacular IDs are integers, but come from the URL as strings.
            # We need to convert it to an integer to match how we saved it (_id).
            try:
                recipe_id_int = int(recipe_id_str)
            except ValueError:
                logger.error(f"Invalid recipe ID format for delete: {recipe_id_str}")
                return {'success': False, 'message': 'Invalid recipe ID format.'}

            # --- ADDED THIS LOG ---
            logger.info(f"Attempting to delete favorite with _id: {recipe_id_int} (Type: {type(recipe_id_int)})")
            # --- END ADD ---

            # The query to find the document with the matching _id
            query = {'_id': recipe_id_int}

            result = self.favorites_collection.delete_one(query)

            if result.deleted_count > 0:
                logger.info(f"Recipe {recipe_id_int} removed from favorites.")
                return {'success': True, 'message': 'Recipe removed from favorites.'}
            else:
                # This means the recipe wasn't found (maybe already deleted)
                logger.warning(f"Recipe {recipe_id_int} not found in favorites for deletion.")
                return {'success': False, 'message': 'Recipe not found in favorites.'}

        except Exception as e:
            logger.error(f"Error deleting favorite recipe: {e}")
            return {'success': False, 'message': str(e)}

    def close_connection(self):
        """Close database connection."""
        self.client.close()