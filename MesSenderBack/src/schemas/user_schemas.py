from pydantic import BaseModel, Field

from fastapi_users import schemas
from src.models import Role


class UserReadDTO(schemas.BaseUser[int]):
    username: str = Field(max_length=20)
    role: Role

class UserUpdateDTO(schemas.BaseUserUpdate):
    username: str = Field(max_length=20)


class UserCreateDTO(schemas.BaseUserCreate):
    username: str = Field(max_length=20)

class UserReadShortDTO(BaseModel):
    id: int
    username: str = Field(max_length=20)


