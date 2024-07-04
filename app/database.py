from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Singleton Pattern - Ensures a single instance of the database engine is created and reused
engine = create_async_engine(
    DATABASE_URL, 
    echo=True, 
    pool_size=20,  
    max_overflow=0
)

# Singleton Pattern - Ensures a single instance of the session factory is created and reused
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Singleton Pattern - Ensures a single instance of the base class for models is created and reused
Base = declarative_base()

async def get_db():
    """
    Dependency Injection (DI) for database session.

    Yields:
        AsyncSession: Database session
    """
    async with SessionLocal() as session:
        yield session
