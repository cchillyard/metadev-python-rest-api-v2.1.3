from enum import Enum
from pydantic import BaseModel

class UserBase(BaseModel):
    id: str
    username: str
    hashed_password: str
    email: str
    first_name: str
    last_name: str
    

class UserCreate(UserBase):
    ...
    
class User(UserBase):
    role: Enum
    
    class Config:
        orm_mode: True