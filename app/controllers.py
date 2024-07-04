from typing import List, Optional
import uuid
from prometheus_client import Counter, Histogram
from app.models import Dish
from app.services import DishService
from loguru import logger

# Define Prometheus metrics
REQUEST_COUNT = Counter('dish_controller_request_count', 'Request Count', ['method'])
REQUEST_LATENCY = Histogram('dish_controller_request_latency_seconds', 'Request latency in seconds', ['method'])

class DishController:
    """
    Controller for managing dishes.
    """
    def __init__(self, service: DishService = DishService()):
        self.service = service  # Dependency Injection (DI) - allows for easy testing and separation of concerns

    @REQUEST_LATENCY.labels(method='create_dish').time()
    def create_dish(self, name: str, description: str, price: float, image: str) -> Dish:
        """
        Handles the creation of a new dish.
        """
        REQUEST_COUNT.labels(method='create_dish').inc()
        logger.info(f"Creating a new dish with name {name}...")
        return self.service.create_dish(name=name, description=description, price=price, image=image)  # Facade - simplifies client interaction

    @REQUEST_LATENCY.labels(method='get_dish').time()
    def get_dish(self, dish_id: uuid.UUID) -> Optional[Dish]:
        """
        Handles retrieving a dish by its ID.
        """
        REQUEST_COUNT.labels(method='get_dish').inc()
        logger.info(f"Retrieving dish with id {dish_id}...")
        return self.service.get_dish(dish_id)  # Facade - simplifies client interaction

    @REQUEST_LATENCY.labels(method='list_dishes').time()
    def list_dishes(self) -> List[Dish]:
        """
        Handles listing all dishes.
        """
        REQUEST_COUNT.labels(method='list_dishes').inc()
        logger.info("Listing all dishes...")
        return self.service.list_dishes()  # Facade - simplifies client interaction

    @REQUEST_LATENCY.labels(method='search_dishes').time()
    def search_dishes(self, query: str) -> List[Dish]:
        """
        Handles searching for dishes.
        """
        REQUEST_COUNT.labels(method='search_dishes').inc()
        logger.info(f"Searching for dishes with query {query}...")
        return self.service.search_dishes(query)  # Facade - simplifies client interaction

    @REQUEST_LATENCY.labels(method='update_dish').time()
    def update_dish(self, dish_id: uuid.UUID, name: str, description: str, price: float, image: str) -> Optional[Dish]:
        """
        Handles updating an existing dish.
        """
        REQUEST_COUNT.labels(method='update_dish').inc()
        logger.info(f"Updating dish with id {dish_id}...")
        return self.service.update_dish(dish_id, name=name, description=description, price=price, image=image)  # Facade - simplifies client interaction

    @REQUEST_LATENCY.labels(method='rate_dish').time()
    def rate_dish(self, dish_id: uuid.UUID, rating: float) -> Optional[Dish]:
        """
        Handles rating a dish.
        """
        REQUEST_COUNT.labels(method='rate_dish').inc()
        logger.info(f"Rating dish with id {dish_id}...")
        return self.service.rate_dish(dish_id, rating=rating)  # Facade - simplifies client interaction

    @REQUEST_LATENCY.labels(method='delete_dish').time()
    def delete_dish(self, dish_id: uuid.UUID) -> int:
        """
        Handles deleting a dish by its ID and returns the number of deleted items.
        """
        REQUEST_COUNT.labels(method='delete_dish').inc()
        logger.info(f"Deleting dish with id {dish_id}...")
        return self.service.delete_dish(dish_id)  # Facade - simplifies client interaction
