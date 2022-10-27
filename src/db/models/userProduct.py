from sqlalchemy import Column, String, Integer, ForeignKey
from ..db_setup import Base


class UserProduct(Base):
    __tablename__ = 'user_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(100), ForeignKey('product.id'), nullable=False)
    username = Column(String(100), nullable=False)
