from pydantic import BaseModel, EmailStr, Field
from models import Role


class UserDTO(BaseModel):
    id: int
    username: str = Field(max_length=20)
    email: EmailStr
    role: Role
    is_banned: bool


class UserUpdateDTO(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr
    password: str
    new_password: str  = Field(validate_default=False, default="",max_length=20, min_length=4)

class UserReadShortDTO(BaseModel):
    id: int
    username: str = Field(max_length=20)


class UserCreateDTO(BaseModel):
    username: str = Field(max_length=20,min_length=4)
    email: EmailStr
    password: str = Field(max_length=20, min_length=4)


class UserLoginDTO(BaseModel):
    username: str = Field(max_length=20)
    password: str = Field(max_length=20, min_length=4)
