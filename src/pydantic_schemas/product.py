from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    id: str
    title: str
    description: str
    availability: str
    condition: str
    price: float
    link: str
    image_link: str
    brand: str
    quantity_to_sell_on_facebook: int
    # Optional
    additional_image_link: Optional[str] = None
    google_product_category: Optional[str] = None
    fb_product_category: Optional[str] = None
    sale_price: Optional[float] = None
    sale_price_effective_date: Optional[datetime] = None
    item_group_id: Optional[str] = None
    color: Optional[str] = None
    gender: Optional[str] = None
    size: Optional[str] = None
    age_group: Optional[str] = None
    material: Optional[str] = None
    pattern: Optional[str] = None
    shipping: Optional[str] = None
    shipping_weight: Optional[str] = None
    # Custom SSCG Fields = None
    vendor_url: Optional[str] = None
    vendor_cogs: Optional[float] = None
    user_id: Optional[str] = None


class ProductCreate(ProductBase):
    ...


class Product(ProductBase):

    class Config:
        orm_mode = True
