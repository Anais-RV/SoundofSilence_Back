from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel): #lo que quiero recibir al crear un user
    name: str
    last_name: str
    user_name: str
    email: EmailStr
    password: str
    profile_image: Optional[bytes]

class User(BaseModel): # lo que podría devolver de un user registrado
    id: int
    name: str
    last_name: str
    user_name: str
    profile_image: Optional[str]
    email: EmailStr

class UserLogin(BaseModel):
    user_name: str
    password: str

class UserResponse(BaseModel):
    token: str
    user: User

    class Config:
        orm_mode = True
