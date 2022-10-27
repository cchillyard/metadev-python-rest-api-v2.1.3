from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.db.models.product import Product
from src.pydantic_schemas.product import ProductCreate


def create_product_by_user(product, db: Session):
    print(product)
    exist_check = get_product_by_id(db, product.id)

    if exist_check == None:
        db_product = Product(
            id=product.id,
            title=product.title,
            description=product.description,
            availability=product.availability,
            condition=product.condition,
            price=product.price,
            link=product.link,
            image_link=product.image_link,
            brand=product.brand,
            quantity_to_sell_on_facebook=product.quantity_to_sell_on_facebook,
            additional_image_link=product.additional_image_link,
            google_product_category=product.google_product_category,
            fb_product_category=product.fb_product_category,
            sale_price=product.sale_price,
            sale_price_effective_date=product.sale_price_effective_date,
            item_group_id=product.item_group_id,
            color=product.color,
            gender=product.gender,
            size=product.size,
            age_group=product.age_group,
            material=product.material,
            pattern=product.pattern,
            shipping=product.shipping,
            shipping_weight=product.shipping_weight,
            vendor_url=product.vendor_url,
            vendor_cogs=product.vendor_cogs,
            user_id=product.user_id,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    else:
        return None


def update_product_by_owner(product, db: Session):
    db_product = get_product_by_id(db, product_id=product.id)
    if db_product:
        db_product.id = product.id
        db_product.title = product.title
        db_product.description = product.description
        db_product.availability = product.availability
        db_product.condition = product.condition
        db_product.price = product.price
        db_product.link = product.link
        db_product.image_link = product.image_link
        db_product.brand = product.brand
        db_product.quantity_to_sell_on_facebook = product.quantity_to_sell_on_facebook
        db_product.additional_image_link = product.additional_image_link
        db_product.google_product_category = product.google_product_category
        db_product.fb_product_category = product.fb_product_category
        db_product.sale_price = product.sale_price
        db_product.sale_price_effective_date = product.sale_price_effective_date
        db_product.item_group_id = product.item_group_id
        db_product.color = product.color
        db_product.gender = product.gender
        db_product.size = product.size
        db_product.age_group = product.age_group
        db_product.material = product.material
        db_product.pattern = product.pattern
        db_product.shipping = product.shipping
        db_product.shipping_weight = product.shipping_weight
        db_product.vendor_url = product.vendor_url
        db_product.vendor_cogs = product.vendor_cogs
        db_product.user_id = product.user_id

        db.commit()

    return 1


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_products_by_user(db: Session, user_id,  skip: int = 0, limit: int = 100):
    return db.query(Product).filter(or_(Product.user_id == None, Product.user_id == user_id)).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()


def delete_product(db: Session, product_id: str):
    db_product = get_product_by_id(db, product_id=product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product
    return None


def update_product_by_id(req, db: Session, product_id: str):
    db_product = get_product_by_id(db, product_id=product_id)
    if db_product:
        db_product.vendor_cogs = req['cog']
        db_product.availability = req['availability']
        db.commit()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        id=product.id,
        title=product.title,
        description=product.description,
        availability=product.availability,
        condition=product.condition,
        price=product.price,
        link=product.link,
        image_link=product.image_link,
        brand=product.brand,
        quantity_to_sell_on_facebook=product.quantity_to_sell_on_facebook,
        additional_image_link=product.additional_image_link,
        google_product_category=product.google_product_category,
        fb_product_category=product.fb_product_category,
        sale_price=product.sale_price,
        sale_price_effective_date=product.sale_price_effective_date,
        item_group_id=product.item_group_id,
        color=product.color,
        gender=product.gender,
        size=product.size,
        age_group=product.age_group,
        material=product.material,
        pattern=product.pattern,
        shipping=product.shipping,
        shipping_weight=product.shipping_weight,
        vendor_url=product.vendor_url,
        vendor_cogs=product.vendor_cogs,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
