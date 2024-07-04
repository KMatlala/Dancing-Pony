from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.user_manager import get_user_by_email, verify_password
from app.failed_attempts import failed_attempts, MAX_FAILED_ATTEMPTS, BLOCK_TIME
from loguru import logger

security = HTTPBasic()

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    """
    Get the current user based on the provided credentials.

    Args:
        credentials (HTTPBasicCredentials, optional): Defaults to Depends(security).
        db (AsyncSession, optional): Defaults to Depends(get_db).

    Raises:
        HTTPException: incorrect email or password
        HTTPException: account locked due to too many failed login attempts. Please try again later.
        HTTPException: incorrect email or password

    Returns:
        User: current user
    """
    user = await get_user_by_email(db, credentials.username)  # Repository Pattern - abstracting database access

    if user is None:
        logger.error(f"User with email {credentials.username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if credentials.username in failed_attempts:
        failed_attempt_info = failed_attempts[credentials.username]
        if failed_attempt_info['count'] >= MAX_FAILED_ATTEMPTS:
            logger.error(f"Account locked for user {credentials.username}")
            if datetime.utcnow() - failed_attempt_info['last_attempt'] < BLOCK_TIME:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account locked due to too many failed login attempts. Please try again later.",
                    headers={"WWW-Authenticate": "Basic"},
                )
            else:
                logger.info(f"Account unlocked for user {credentials.username}")
                del failed_attempts[credentials.username]  # State Management - handling the state of failed attempts

    if not await verify_password(credentials.password, user.hashed_password):  # Strategy Pattern - different password verification strategies
        if credentials.username not in failed_attempts:
            logger.error(f"Incorrect password for user {credentials.username}")
            failed_attempts[credentials.username] = {'count': 1, 'last_attempt': datetime.utcnow()}  # State Management
        else:
            logger.error(f"Incorrect password for user {credentials.username}")
            failed_attempts[credentials.username]['count'] += 1  # State Management
            failed_attempts[credentials.username]['last_attempt'] = datetime.utcnow()  # State Management
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if credentials.username in failed_attempts:
        logger.info(f"Login successful for user {credentials.username}")
        del failed_attempts[credentials.username]  # State Management
    
    return user
