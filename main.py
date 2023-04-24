from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from enum import Enum
import fastapi_users
from pydantic import BaseModel
from typing import List
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from auth.database import User

app = FastAPI(
    title = "BAT agregator"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

 
@app.get("/")
async def root():
    return {'message': 'Hello World'}


async def products():
    pass 
    # get product list

async def user():
    pass
    # get user info