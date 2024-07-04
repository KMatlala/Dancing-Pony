from typing import List, Optional
from app.models import Dish
from app.repositories import DishRepository
import uuid

class DishService:
    """
    Service layer for managing dishes.
    """
    def __init__(self, repository: DishRepository = DishRepository()):
        self.repository = repository

    def create_dish(self, name: str, description: str, price: float, image: str) -> Dish:
        """
        Creates a new dish.
        """
        dish = Dish(name=name, description=description, price=price, image=image)
        self.repository.add(dish)
        return dish

    def get_dish(self, dish_id: uuid.UUID) -> Optional[Dish]:
        """
        Retrieves a dish by its ID.
        """
        return self.repository.get(dish_id)

    def list_dishes(self) -> List[Dish]:
        """
        Lists all dishes.
        """
        return self.repository.list()

    def search_dishes(self, query: str) -> List[Dish]:
        """
        Searches for dishes matching the query.
        """
        return self.repository.search(query)

    def update_dish(self, dish_id: uuid.UUID, name: str, description: str, price: float, image: str) -> Optional[Dish]:
        """
        Updates an existing dish.
        """
        dish = self.repository.get(dish_id)
        if dish:
            dish.name = name
            dish.description = description
            dish.price = price
            dish.image = image
            self.repository.update(dish)
            return dish
        return None

    def rate_dish(self, dish_id: uuid.UUID, rating: float) -> Optional[Dish]:
        """
        Rates a dish.
        """
        dish = self.repository.get(dish_id)
        if dish:
            dish.rating = rating
            self.repository.update(dish)
            return dish
        return None

    def delete_dish(self, dish_id: uuid.UUID) -> int:
        """
        Deletes a dish by its ID and returns the number of deleted items.
        """
        return self.repository.delete(dish_id)
