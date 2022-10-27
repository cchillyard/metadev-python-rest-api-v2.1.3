from enum import auto
from sqlalchemy import Column, Integer, String, Enum, Float, DateTime
from ..db_setup import Base

class Product(Base):
    __tablename__ = 'product'

    id = Column(String, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(9999), nullable=False)
    availability = Column(String(), nullable=False)
    condition = Column(String(), nullable=False)
    price = Column(Float(), nullable=False)
    link = Column(String, nullable=False)
    image_link = Column(String, nullable=False)
    brand = Column(String(100), nullable=False)
    quantity_to_sell_on_facebook = Column(Integer, nullable=False, default=1)
    #Optinal Fields
    additional_image_link = Column(String, nullable=True)
    google_product_category = Column(String, nullable=True)
    fb_product_category = Column(String, nullable=True)
    sale_price = Column(Float, nullable=True)
    sale_price_effective_date = Column(DateTime, nullable=True)
    item_group_id = Column(String, nullable=True)
    color = Column(String(200), nullable=True)
    gender = Column(String(), nullable=True, default="unisex")
    size = Column(String(200), nullable=True, default="all")
    age_group = Column(String(), nullable=True, default="all_ages")
    material = Column(String(200), nullable=True)
    pattern = Column(String(100), nullable=True)
    shipping = Column(String(200), nullable=True) 
    shipping_weight = Column(String(200), nullable=True)
    #Custom SSCG Fields
    vendor_url = Column(String, nullable=True)
    vendor_cogs = Column(Float, nullable=True)
    user_id = Column(String(255), nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.title