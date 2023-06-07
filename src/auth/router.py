from fastapi import APIRouter

from .base_config import fastapi_users
from auth.schemas import UserCreate, UserRead
from auth.base_config import auth_backend, fastapi_users


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/jwt',
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
