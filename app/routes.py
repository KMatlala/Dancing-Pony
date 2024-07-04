from typing import List, Optional
import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.controllers import DishController
from app.models import User
from app.database import get_db
from app.user_manager import create_user, get_user_by_email
from app.auth import get_current_user
from loguru import logger

router = APIRouter()
controller = DishController()

class DishCreate(BaseModel):
    """
    Dish create model class.

    Args:
        BaseModel (_type_): _description_
    """
    name: str
    description: str
    price: float
    image: str

class DishResponse(BaseModel):
    """
    Dish response model class.

    Args:
        BaseModel (_type_): _description_
    """
    id: uuid.UUID
    name: str
    description: str
    price: float
    image: str
    rating: Optional[float]

    class Config:
        from_attributes = True

class DishRate(BaseModel):
    """
    Dish rate model class.

    Args:
        BaseModel (_type_): _description_
    """
    rating: float

    class Config:
        from_attributes = True
        
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(email: str, password: str, name: str, db: AsyncSession = Depends(get_db)):
    """
    Register user.

    Args:
        email (str): user email
        password (str): user password
        name (str): user name
        db (AsyncSession, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: email already registered

    Returns:
        User: created user
    """
    logger.info("Registering user...")
    user = await get_user_by_email(db, email)
    if user:
        logger.warning("Email already registered")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    logger.success("User registered")
    return await create_user(db, email, password, name)

@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current user.

    Args:
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        User: current user
    """
    logger.info("Getting current user...")  
    return current_user

@router.post('/dishes', response_model=DishResponse, status_code=status.HTTP_201_CREATED)
def create_dish(dish: DishCreate, user: User = Depends(get_current_user)):
    """
    Create dish.

    Args:
        dish (DishCreate): dish create model
        user (User, optional): user. Defaults to Depends(get_current_user).

    Returns:
        DishResponse: created dish
    """
    logger.info(f"Creating dish {dish.name}...")
    created_dish = controller.create_dish(name=dish.name, description=dish.description, price=dish.price, image=dish.image)
    return created_dish.to_dict()

@router.get('/dishes/{dish_id}', response_model=DishResponse)
def get_dish(dish_id: uuid.UUID, user: User = Depends(get_current_user)):
    """
    Get dish.

    Args:
        dish_id (uuid.UUID): _description_
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Dish not found

    Returns:
        Dish: dish matching id
    """
    logger.info(f"Getting dish {dish_id}...")
    dish = controller.get_dish(dish_id)
    if dish:
        logger.success(f"Dish {dish_id} found")
        return dish.to_dict()
    logger.warning(f"Dish {dish_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")

@router.get('/dishes', response_model=List[DishResponse])
def list_dishes(user: User = Depends(get_current_user)):
    """
    List dishes.

    Args:
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        List[Dish]: list of dishes
    """
    logger.info("Listing dishes...")
    dishes = controller.list_dishes()
    if dishes:
        logger.success(f"{len(dishes)} dishes found. ")
        return [dish.to_dict() for dish in dishes]
    logger.error("No dishes found.")
    return []

@router.get('/search', response_model=List[DishResponse])
def search_dishes(query: str, user: User = Depends(get_current_user)):
    """
    Search dishes.

    Args:
        query (str): search query
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        List[Dish]: list of dishes matching query
    """
    logger.info(f"Searching dishes for {query}...")
    dishes = controller.search_dishes(query)
    if dishes:
        logger.success(f"{len(dishes)} dishes found. ")
        return [dish.to_dict() for dish in dishes]
    logger.error("No dishes found.")
    return [dish.to_dict() for dish in dishes]

@router.put('/dishes/{dish_id}', response_model=DishResponse)
def update_dish(dish_id: uuid.UUID, dish: DishCreate, user: User = Depends(get_current_user)):
    """
    Update dish.

    Args:
        dish_id (uuid.UUID): dish id
        dish (DishCreate): dish create model
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Dish not found

    Returns:
        Dish: updated dish
    """
    logger.info(f"Updating dish {dish_id}...")
    updated_dish = controller.update_dish(dish_id=dish_id, name=dish.name, description=dish.description, price=dish.price, image=dish.image)
    if updated_dish:
        logger.success(f"Dish {dish_id} updated")
        return updated_dish.to_dict()
    logger.warning(f"Dish {dish_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")

@router.put('/dishes/{dish_id}/rate', response_model=DishResponse)
def rate_dish(dish_id: uuid.UUID, rating: DishRate, user: User = Depends(get_current_user)):
    """
    Rate dish.

    Args:
        dish_id (uuid.UUID): _description_
        rating (DishRate): _description_
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Dish not found

    Returns:
        dict: rated dish
    """
    logger.info(f"Rating dish {dish_id}...")
    rated_dish = controller.rate_dish(dish_id=dish_id, rating=rating.rating)
    if rated_dish:
        logger.success(f"Dish {dish_id} rated")
        return rated_dish.to_dict()
    logger.warning(f"Dish {dish_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")

@router.delete('/dishes/{dish_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(dish_id: uuid.UUID, user: User = Depends(get_current_user)):
    """
    Delete dish.

    Args:
        dish_id (uuid.UUID): _description_
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    logger.info(f"Deleting dish {dish_id}...")
    deleted_count = controller.delete_dish(dish_id)
    if deleted_count > 0:
        logger.success(f"Dish {dish_id} deleted")
    return {"deleted": deleted_count}
