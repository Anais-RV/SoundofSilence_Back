from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    last_name: str
    user_name: str
    profile_image: Optional[str]
    email: EmailStr

class UserCreate(User):
    name: str
    last_name: str
    user_name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
