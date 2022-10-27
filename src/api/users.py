import requests
import fastapi
import os

from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.api.utils.userProducts import get_products_by_owner

from src.db.db_setup import get_db
from src.pydantic_schemas.user import UserCreate
from src.pydantic_schemas.auth import AuthDetails
from src.api.utils.users import get_users, create_user, get_user_by_username
from src.api.utils.auth import AuthHandler
from definitions import ROOT_DIR

router = fastapi.APIRouter()
auth_handler = AuthHandler()


@router.get("/users", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/user/{username}", dependencies=[Depends(auth_handler.auth_wrapper)])
async def api_get_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=username)
    return user


@router.post("/login")
async def api_login(auth_details: AuthDetails,  db: Session = Depends(get_db)):
    url = f"https://imlwebanalyzer.com/userauth.php?USERNAME={auth_details.username}&PASSWORD={auth_details.password}"
    response = requests.post(url)
    if response.status_code == 200:
        try:
            data = response.json()['data'][0]
            id = data['id']
        except:
            raise HTTPException(
                status_code=401, detail=f"Invalid username or password")

        plain_password = id + auth_details.username

        # Check if user exists in db
        user = get_user_by_username(db, username=auth_details.username)
        # If user does not exist, create it
        if(user is None):
            hashed_password = auth_handler.get_password_hash(plain_password)
            newUser = user = UserCreate(id=id, username=auth_details.username,
                                        email=data['email'], hashed_password=hashed_password, first_name=data['firstName'], last_name=data['lastName'])
            user = create_user(db, user=newUser)

        #Log in user
        if(not auth_handler.verify_password(plain_password, user.hashed_password)):
            raise HTTPException(
                status_code=401, detail=f"Authentication failed")

        token = auth_handler.encode_token(user.username)
        return {"token": token}

    else:
        raise HTTPException(
            status_code=504, detail="Authentication System Error")
