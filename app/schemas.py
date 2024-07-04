from pydantic import BaseModel, EmailStr
import uuid

class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    name: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

    class Config:
        from_attributes = True
