import enum
from typing import Optional
from pydantic import EmailStr, Field
from src.models import Role

from fastapi_users import schemas
from src.models import Role


class UserRead(schemas.BaseUser[int]):
    username: str = Field(max_length=20)
    role: Role



class UserCreate(schemas.BaseUserCreate):
    username: str = Field(max_length=20)




