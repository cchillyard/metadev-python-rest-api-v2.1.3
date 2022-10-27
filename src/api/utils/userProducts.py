from sqlalchemy.orm import Session
from sqlalchemy import delete
from src.api.utils.products import get_product_by_id
from src.db.models.userProduct import UserProduct
from src.db.models.product import Product
from src.pydantic_schemas.userProduct import UserProductCreate
from sqlalchemy import or_


def create_user_product(db: Session, userProduct: UserProductCreate):
    user_product = get_user_product_by_username_and_product_id(
        db, username=userProduct.username, product_id=userProduct.product_id)
    if (user_product):
        return {'success': False}
    else:
        db_user_product = UserProduct(
            username=userProduct.username, product_id=userProduct.product_id)
        db.add(db_user_product)
        db.commit()
        db.refresh(db_user_product)
        return db_user_product


def get_user_product(db: Session, user_product_id: int):
    return db.query(UserProduct, Product).join(Product, UserProduct.product_id == Product.id).filter(UserProduct.id == user_product_id).first()


def get_user_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserProduct, Product).join(Product, UserProduct.product_id == Product.id).offset(skip).limit(limit).all()


def get_products_by_owner(db: Session, username: str, skip: int = 0, limit: int = 100):
    return db.query(UserProduct, Product).join(Product, UserProduct.product_id == Product.id).filter(UserProduct.username == username).offset(skip).limit(limit).all()


def get_user_product_by_username_and_product_id(db: Session, username: str, product_id: str):
    return db.query(UserProduct).filter(UserProduct.product_id == product_id).filter(UserProduct.username == username).first()


def remove_product_from_list(db: Session, user_product_id: int):
    db_user_product = get_user_product(db, user_product_id=user_product_id)

    if db_user_product:
        db.query(UserProduct).filter(
            UserProduct.id == user_product_id).delete()
        db.commit()
        return db_user_product
    return None


def delete_product_by_owner(db: Session, product_id: str):
    db_product = get_product_by_id(db, product_id=product_id)

    if db_product:
        db.query(Product).filter(Product.id == product_id).delete()
        db.commit()

        user_product = get_user_product_by_username_and_product_id(
            db, username=db_product.user_id, product_id=product_id)

        if user_product:
            db.query(UserProduct).filter(UserProduct.username == db_product.user_id).filter(UserProduct.product_id == product_id).delete()
            db.commit()

    return db_product
