from pydantic import BaseModel, EmailStr, Field

from fastapi_users import schemas
from src.models import Role


class UserDTO(BaseModel):
    id: int
    username: str = Field(max_length=20)
    email: EmailStr
    role: Role


class UserUpdateDTO(schemas.BaseUserUpdate):
    username: str = Field(max_length=20)


class UserReadShortDTO(BaseModel):
    id: int
    username: str = Field(max_length=20)


class UserCreateDTO(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr
    password: str = Field(max_length=20, min_length=4)


class UserLoginDTO(BaseModel):
    username: str = Field(max_length=20)
    password: str = Field(max_length=20, min_length=4)
