import json
import fastapi
import csv
import os
import codecs

from fastapi import Depends
from pydantic import Json
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse
from src.api.utils.products import create_product_by_user, update_product_by_owner
from src.db.db_setup import get_db
from src.api.utils.auth import AuthHandler
from src.pydantic_schemas.userProduct import UserProductDetails, UserProductCreate
from src.pydantic_schemas.product import ProductCreate, Product
from src.api.utils.userProducts import create_user_product, delete_product_by_owner, remove_product_from_list, get_user_product, get_user_products, get_products_by_owner
from src.api.utils.users import get_user_by_username

router = fastapi.APIRouter()
auth_handler = AuthHandler()


@router.post("/add-product-to-list")
async def api_add_product_to_list(user_product_details: UserProductDetails, db: Session = Depends(get_db)):
    newUserProduct = UserProductCreate(
        username=user_product_details.username, product_id=user_product_details.product_id)
    userProduct = create_user_product(db, userProduct=newUserProduct)
    return userProduct


@router.get("/get-products-by-owner/{username}")
async def api_get_products_by_owner(username: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products_by_owner(db, username, skip=skip, limit=limit)


@router.delete("/remove-product-from-list/{id}")
async def api_remove_product_from_list(id: int, db: Session = Depends(get_db)):
    return remove_product_from_list(db, user_product_id=id)


@router.post("/create-product-by-user")
async def api_create_product_by_user(new_product_details: Product, db: Session = Depends(get_db)):
    print(new_product_details)
    product = create_product_by_user(new_product_details, db)
    if product == None:
        return 'Duplicate Product ID'
    else:
        newUserProduct = UserProductCreate(
            username=product.user_id, product_id=product.id)
        userProduct = create_user_product(db, userProduct=newUserProduct)
        return userProduct


@router.post("/update-product-by-owner")
async def api_update_product_by_owner(product_details: Product, db: Session = Depends(get_db)):
    product = update_product_by_owner(product_details, db)
    return product


@router.delete('/delete-product-by-owner/{product_id}')
async def api_delete_product_by_owner(product_id: str, db: Session = Depends(get_db)):
    product = delete_product_by_owner(db, product_id=product_id)
    return product


@router.get("/user/{username}/datafeed.csv")
async def api_user_csv(username: str, db: Session = Depends(get_db)):
    userProducts = jsonable_encoder(
        get_products_by_owner(db, username))

    with open('datafeed.csv', mode='w', newline='', encoding='utf-8-sig') as csv_file:
        fieldnames = ['id', 'title', 'description', 'availability', 'condition', 'price', 'link', 'image_link', 'brand', 'quantity_to_sell_on_facebook', 'additional_image_link', 'google_product_category',
                      'fb_product_category', 'sale_price', 'sale_price_effective_date', 'item_group_id', 'color', 'gender', 'size', 'age_group', 'material', 'pattern', 'shipping', 'shipping_weight', 'vendor_url', 'vendor_cogs']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for index in range(len(userProducts)):
            product = userProducts[index]['Product']

            writer.writerow({
                'id': product['id'],
                'title': product['title'],
                'description': product['description'],
                'availability': product['availability'],
                'condition': product['condition'],
                'price': product['price'],
                'link': product['link'],
                'image_link': product['image_link'],
                'brand': product['brand'],
                'quantity_to_sell_on_facebook': product['quantity_to_sell_on_facebook'],
                'additional_image_link': product['additional_image_link'],
                'google_product_category': product['google_product_category'],
                'fb_product_category': product['fb_product_category'],
                'sale_price': product['sale_price'],
                'sale_price_effective_date': product['sale_price_effective_date'],
                'item_group_id': product['item_group_id'],
                'color': product['color'],
                'gender': product['gender'],
                'size': product['size'],
                'age_group': product['age_group'],
                'material': product['material'],
                'pattern': product['pattern'],
                'shipping': product['shipping'],
                'shipping_weight': product['shipping_weight'],
                'vendor_url': product['vendor_url'],
                'vendor_cogs': product['vendor_cogs']
            })

    if(get_user_by_username(db, username) is None):
        return HTTPException(status_code=404, detail="User does not exist")

    file_path = "datafeed.csv"
    return FileResponse(file_path, media_type="text/csv")
