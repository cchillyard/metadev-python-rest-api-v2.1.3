from typing import List
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.scraper.httpsRequest import check_vendor_by_url

from src.db.db_setup import get_db
from src.pydantic_schemas.product import ProductCreate
from src.api.utils.products import get_products, get_products_by_user,  create_product, get_product_by_id, delete_product, update_product_by_id
from src.api.utils.auth import AuthHandler

router = fastapi.APIRouter()
auth_handler = AuthHandler()


@router.get("/products", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_get_products(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products


@router.get("/products_by_user/{id}", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_get_products(id: str, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    products = get_products_by_user(db, user_id=id, skip=skip, limit=limit)
    return products


@router.post("/products", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_post_products(products: List[ProductCreate], db: Session = Depends(get_db)):
    try:
        for product in products:
            if(get_product_by_id(db, product.id) != None):
                delete_product(db, product.id)

            create_product(db, product)

        raise HTTPException(
            status_code=201, detail="Products added successfully")
    except Exception as e:
        error = {
            "message": "Error adding products",
            "error": str(e)
        }
        raise HTTPException(status_code=400, detail=error)


@router.get("/product/{id}", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_get_user(id: str, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id=id)
    return product


@router.post("/product-update/{id}", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_update_product(id: str, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id=id)
    vendor_url = product.vendor_url
    res = check_vendor_by_url(vendor_url)
    update_product_by_id(res, db, product_id=id)
    return get_product_by_id(db, product_id=id)


@router.post("/product-check/{id}", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_check_update(id: str, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id=id)
    vendor_url = product.vendor_url
    res = check_vendor_by_url(vendor_url)
    return res
