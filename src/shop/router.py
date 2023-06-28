from fastapi import APIRouter
from .products.router import router as product_router
from .cart.router import router as cart_router


router = APIRouter(
    prefix='/shop',
)

router.include_router(product_router)
router.include_router(cart_router)
