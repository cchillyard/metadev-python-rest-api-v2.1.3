from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import users, products, userProducts
from src.db.db_setup import engine, Base
from src.db.models import user, product

user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IM Marketplace Automation",
    version="0.0.1",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return "Jusimen was here!"

app.include_router(users.router)
app.include_router(products.router)
app.include_router(userProducts.router)
