from typing import Optional
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Singleton Pattern: Ensures a single instance of the base class for models is created and reused
Base = declarative_base()

class Dish(BaseModel):
    """
    Dish model class using Pydantic for data validation and serialization.
    
    This class acts as a Data Transfer Object (DTO), which is used to transfer data between layers.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)  # Automatically generate unique ID for each Dish
    name: str
    description: str
    price: float
    image: str
    rating: Optional[float] = None

    class Config:
        # Allows Pydantic model to be created from ORM objects
        from_attributes = True

    def to_dict(self) -> dict:
        """
        Converts the dish object to a dictionary.
        
        This method implements the Serializer pattern, enabling the object to be converted into a format suitable for storage or transmission.
        """
        logger.info("Converting dish object to dictionary...")
        return {
            "id": str(self.id),  # Convert UUID to string for JSON serialization
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "rating": self.rating
        }

    @staticmethod
    def from_dict(data: dict) -> 'Dish':
        """
        Creates a dish object from a dictionary.
        
        This method acts as a Factory Method, allowing the creation of Dish objects from a dictionary representation.
        """
        logger.info("Creating dish object from dictionary...")
        return Dish(
            id=uuid.UUID(data["id"]) if "id" in data else uuid.uuid4(),
            name=data["name"],
            description=data["description"],
            price=data["price"],
            image=data["image"],
            rating=data.get("rating")
        )

class User(Base):
    """
    User model class using SQLAlchemy for ORM.
    
    This class uses the Active Record pattern, encapsulating both the data and the behavior that operates on the data.
    """
    __tablename__ = os.getenv("USER_TABLE_NAME")  # Table name is dynamically set from environment variable
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Primary key with auto-generated UUID
    email = Column(String, unique=True, index=True, nullable=False)  # Unique and indexed email column
    hashed_password = Column(String, nullable=False)  # Column for storing hashed passwords
    is_active = Column(Boolean, default=True)  # Boolean flag for active users
    is_superuser = Column(Boolean, default=False)  # Boolean flag for superuser status
    name = Column(String, nullable=False)  # Non-nullable name column

class UserUpdate(BaseModel):
    """
    User update model class using Pydantic for data validation and serialization.
    
    This class also acts as a Data Transfer Object (DTO), which is used to transfer data between layers.
    """
    email: Optional[str]
    password: Optional[str]
    name: Optional[str]

    class Config:
        # Allows Pydantic model to be created from ORM objects
        from_attributes = True
