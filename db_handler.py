# db_handler.py
import pymongo
from pymongo import MongoClient
from datetime import datetime
import logging
from config import MONGO_URI, DATABASE_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            try:
                 recipe_id_int = int(recipe_data.get('id'))
            except (ValueError, TypeError):
                 logger.error(f"Invalid recipe ID received for saving: {recipe_data.get('id')}")
                 return {'success': False, 'message': 'Invalid recipe ID format for saving.'}

            query = {'_id': recipe_id_int}

            logger.info(f"Attempting to save/update favorite with _id: {query['_id']} (Type: {type(query['_id'])})")
            update_data = {
                '$set': {
                    'title': recipe_data.get('title'),
                    'image': recipe_data.get('image'),
                    'added_at': datetime.utcnow()
                }
            }

            result = self.favorites_collection.update_one(query, update_data, upsert=True)

            if result.upserted_id:
                logger.info(f"Recipe {recipe_id_int} added to favorites.")
                return {'success': True, 'message': 'Recipe added to favorites.'}
            elif result.matched_count > 0:
                logger.info(f"Recipe {recipe_id_int} is already a favorite.")
                return {'success': True, 'message': 'Recipe is already a favorite.'}
            else:
                return {'success': False, 'message': 'Failed to add recipe (unknown issue).'}

        except Exception as e:
            logger.error(f"Error adding favorite recipe: {e}")
            return {'success': False, 'message': str(e)}

    def get_favorite_recipes(self, limit=50):
        """Retrieve all favorite recipes from the database."""
        try:
            cursor = self.favorites_collection.find().sort('added_at', -1).limit(limit)
            favorites = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                favorites.append(doc)
            return favorites
        except Exception as e:
            logger.error(f"Error retrieving favorite recipes: {e}")
            return []

    def delete_favorite_recipe(self, recipe_id_str):
        """Deletes a recipe from the favorites collection by its ID."""
        try:
            try:
                recipe_id_int = int(recipe_id_str)
            except ValueError:
                logger.error(f"Invalid recipe ID format for delete: {recipe_id_str}")
                return {'success': False, 'message': 'Invalid recipe ID format.'}

            logger.info(f"Attempting to delete favorite with _id: {recipe_id_int} (Type: {type(recipe_id_int)})")
            query = {'_id': recipe_id_int}

            result = self.favorites_collection.delete_one(query)

            if result.deleted_count > 0:
                logger.info(f"Recipe {recipe_id_int} removed from favorites.")
                return {'success': True, 'message': 'Recipe removed from favorites.'}
            else:
                logger.warning(f"Recipe {recipe_id_int} not found in favorites for deletion.")
                return {'success': False, 'message': 'Recipe not found in favorites.'}

        except Exception as e:
            logger.error(f"Error deleting favorite recipe: {e}")
            return {'success': False, 'message': str(e)}

    def close_connection(self):
        """Close database connection."""
        self.client.close()