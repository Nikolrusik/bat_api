from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy import select, delete
from fastapi_cache.decorator import cache
from schemas import Response

from database import get_async_session
from auth.models import User
from auth.base_config import current_user
from shop.cart import utils as ut
from shop.cart import models as md
from shop.cart import schemas as sc


router = APIRouter(
    prefix='',
    tags=['Shop[Cart]']
)

# response_model=Response[sc.Cart]
@router.get('/cart/list')
async def get_cart_by_user(user:  User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    '''
    Retrieving a list of products in the shopping cart for the currently authenticated user.
    '''
    try: 
        query = select(md.Cart).where(md.Cart.user_id == user.id)
        result = await session.execute(query)
        products = result.scalars().all()


        return {
            'status': 'success',
            'data': products,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })




# @router.get('/products/{product_id}', response_model=sc.Response[sc.Product])
# # @cache(expire=300)
# async def get_product_by_id(
#     product_id: int,
#     session: AsyncSession = Depends(get_async_session)
# ):
#     '''
#     Get product by id
#     '''
#     try:
#         query = select(md.Product).options(
#             selectinload(md.Product.stocks),
#             selectinload(md.Product.photos),
#             selectinload(md.Product.reviews)).where(md.Product.id == product_id)
#         result = await session.execute(query)
#         product = result.scalar_one_or_none()

#         if product is None:
#             raise HTTPException(status_code=404, detail={
#                 'status': 'error',
#                 'data': None,
#                 'details': 'Object not found'
#             })

#         return {
#             'status': 'success',
#             'data': product,
#             'details': None
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={
#             'status': 'error',
#             'data': None,
#             'details': str(e)
#         })

# @router.get('/products/list_in_category/{category_id}')
# async def get_product_list_in_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
#     '''
#     This endpoint returns a list of all active products for the selected category and its subcategories.
#     '''
#     try:
#         cte = select(md.Category.id, md.Category.parent_id).cte(recursive=True)
#         cte_alias = aliased(cte, name='cte_alias')
#         recursive_part = select(md.Category.id, md.Category.parent_id).where(md.Category.parent_id == cte_alias.c.id)

#         cte = cte.union_all(recursive_part)

#         subquery = select(cte.c.id).where(cte_alias.c.parent_id == category_id).correlate_except(cte_alias)

#         query = select(md.Product).where(md.Product.category_id.in_(subquery)).order_by(md.Product.category_id)

#         result = await session.execute(query)

#         return {
#             'status': 'success',
#             'data': result.scalars().all(),
#             'details': None
#         }
#     except:
#         raise HTTPException(status_code=500, detail={
#             'status': 'error',
#             'data': None,
#             'details': None
#         })
    

# @router.post('/products/create')
# async def create_product(
#         new_product: sc.ProductCreate = Form(...),
#         photos: List[UploadFile] = File(...),
#         session: AsyncSession = Depends(get_async_session)):
#     '''
#     Create product
#     '''
#     try:
#         async with session.begin():
#             product = md.Product(**new_product.dict())
#             session.add(product)
#             await session.flush()

#             for photo in photos:
#                product_photo = await ut.save_product_photo(product, photo, session)

#             await session.commit()

#         return {'status': 'success'}
#     except SQLAlchemyError as e:
#         error = str(e.__dict__['orig'])
#         raise HTTPException(status_code=500, detail={
#             'status': 'error',
#             'data': error,
#             'details': None
#         })
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={
#             'status': 'error',
#             'data': None,
#             'details': str(e)
#         })

