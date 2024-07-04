from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User

# Singleton Pattern: Ensures a single instance of the password context is created and reused
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_user(db: AsyncSession, email: str, password: str, name: str):
    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password, name=name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)