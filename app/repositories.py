from typing import List, Optional
import psycopg2
import psycopg2.extras
from app.models import Dish
import uuid
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

class DishRepository:
    """
    Repository for interacting with the dishes in the database.
    
    This class implements the Repository pattern, providing an abstraction over the data layer.

    """
    def __init__(self, db_connection = conn):
        self.db_connection = db_connection

    def add(self, dish: Dish) -> None:
        """
        Adds a new dish to the database.
        """
        logger.info(f"Adding dish {dish.name} to database...")
        with self.db_connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dish (id, name, description, price, image, rating)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (str(dish.id), dish.name, dish.description, dish.price, dish.image, dish.rating))
            self.db_connection.commit()

    def get(self, dish_id: uuid.UUID) -> Optional[Dish]:
        """
        Retrieves a dish by its ID.
        """
        logger.info(f"Retrieving dish with id {dish_id} from database...")
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM dish WHERE id = %s", (str(dish_id),))
            row = cursor.fetchone()
            if row:
                return Dish.from_dict(dict(row))
            return None

    def list(self) -> List[Dish]:
        """
        Lists all dishes.
        """
        logger.info("Listing all dishes...")
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM dish")
            rows = cursor.fetchall()
            return [Dish.from_dict(dict(row)) for row in rows]

    def search(self, query: str) -> List[Dish]:
        """
        Searches for dishes matching the query.
        """
        logger.info(f"Searching for dishes matching query {query}...")
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM dish WHERE name ILIKE %s OR description ILIKE %s", (f'%{query}%', f'%{query}%'))
            rows = cursor.fetchall()
            return [Dish.from_dict(dict(row)) for row in rows]

    def update(self, dish: Dish) -> None:
        """
        Updates an existing dish in the database.
        """
        logger.info(f"Updating dish with id {dish.id} in database...")
        with self.db_connection.cursor() as cursor:
            cursor.execute("""
                UPDATE dish
                SET name = %s, description = %s, price = %s, image = %s, rating = %s
                WHERE id = %s
            """, (dish.name, dish.description, dish.price, dish.image, dish.rating, str(dish.id)))
            self.db_connection.commit()

    def delete(self, dish_id: uuid.UUID) -> int:
        """
        Deletes a dish from the database and returns the number of deleted items.
        """
        logger.info(f"Deleting dish with id {dish_id} from database...")
        with self.db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM dish WHERE id = %s", (str(dish_id),))
            deleted_count = cursor.rowcount
            self.db_connection.commit()
            return deleted_count
