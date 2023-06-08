from fastapi import APIRouter
from .products.router import router as product_router

router = APIRouter(
    prefix='/shop',
    tags=['Products'],
)

router.include_router(product_router)
