from pydantic import BaseModel
from enum import Enum


class UserProductDetails(BaseModel):
    username: str
    product_id: str


class UserProductBase(BaseModel):
    username: str
    product_id: str


class UserProductCreate(UserProductBase):
    ...


class UserProduct(UserProductBase):
    role: Enum

    class Config:
        orm_mode: True
