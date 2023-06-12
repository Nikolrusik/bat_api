from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete
from fastapi_cache.decorator import cache

from database import get_async_session
from shop.products import models as md
from shop.products import schemas as sc


router = APIRouter(
    prefix='',
    tags=['Products'],
)

### Category ###


@router.get('/category', response_model=sc.Response[List[sc.Category]])
async def get_category_list(session: AsyncSession = Depends(get_async_session)):
    '''
    Getting a list of category
    '''
    try:
        query = select(md.Category).where(md.Category.is_active == True)
        result = await session.execute(query)

        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None
        }
    except:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.post('/category/create')
async def create_category(
        new_category: sc.CategoryCreate = Body(...),
        photo: Optional[UploadFile] = File(...),
        session: AsyncSession = Depends(get_async_session)):
    try:
        async with session.begin():
            category = md.Stock(**new_category.dict())
            session.add(category)
            await session.commit()
        return {
            'status': 'success',
            'data': category,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


### Products ###
@router.get('/products', response_model=sc.Response[List[sc.Product]])
# @cache(expire=300)
async def get_products_list(session: AsyncSession = Depends(get_async_session)):
    '''
    Getting a list of products
    '''
    try:
        query = select(md.Product).options(selectinload(
            md.Product.photos)).where(md.Product.is_active == True)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None
        }
    except:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.get('/products/{product_id}', response_model=sc.Response[sc.Product])
# @cache(expire=300)
async def get_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Get product by id
    '''
    try:
        query = select(md.Product).options(
            selectinload(md.Product.stocks),
            selectinload(md.Product.photos),
            selectinload(md.Product.reviews)).where(md.Product.id == product_id)
        result = await session.execute(query)
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail={
                'status': 'error',
                'data': None,
                'details': 'Object not found'
            })

        return {
            'status': 'success',
            'data': product,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.post('/products/create')
async def create_product(
        new_product: sc.ProductCreate = Body(...),
        photos: List[UploadFile] = File(...),
        session: AsyncSession = Depends(get_async_session)):
    '''
    Create product
    '''
    try:
        async with session.begin():
            product = md.Product(**new_product.dict())
            session.add(product)
            await session.flush()

            for photo in photos:
                photo_data = await photo.read()
                # временное хранилище файлов
                photo_url = f'./path/{photo.filename}'
                product_photo = md.ProductPhoto(
                    product_id=product.id, photo_url=photo_url)
                session.add(product_photo)

                with open(photo_url, 'wb') as file:
                    file.write(photo_data)

            await session.commit()

        return {'status': 'success'}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': error,
            'details': None
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.patch('/products/update/{id}', response_model=sc.Response[sc.Product])
async def update_product(
    id: int,
    updated_data: sc.ProductUpdate = Body(...),
    delete_photo_ids: str = Body([]),
    new_photos: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Update(Patch) for product
    '''
    try:
        stmt = select(md.Product).filter(md.Product.id == id)
        result = await session.execute(stmt)
        stored_item = result.scalar_one_or_none()

        if not stored_item:
            raise HTTPException(status_code=404, detail={
                'status': 'error',
                'data': None,
                'details': 'Object not found'
            })

        # Удаление выбранных фотографий
        for ids in delete_photo_ids:
            await session.execute(delete(md.ProductPhoto).where(
                md.ProductPhoto.id == int(ids)
            ))
            # await session.

        # Добавление новых фотографий
        for photo in new_photos:
            photo_data = await photo.read()
            # временное хранилище файлов
            photo_url = f'./path/{photo.filename}'
            product_photo = md.ProductPhoto(
                product_id=stored_item.id, photo_url=photo_url)
            session.add(product_photo)

            with open(photo_url, 'wb') as file:
                file.write(photo_data)

        # Обновление остальных полей продукта
        update_data = updated_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(stored_item, field, value)

        await session.commit()
        await session.refresh(stored_item)

        return {
            'status': 'success',
            'data': stored_item,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.delete('/products/delete/{id}')
async def delete_product(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Delete product by id
    '''
    try:
        stmt = delete(md.Product).where(md.Product.id == id)
        await session.execute(stmt)
        await session.commit()

        return {
            'status': 'success',
            'data': f'Deleted product.id = {id}',
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })

### Stocks ###


@router.get('/stocks', response_model=sc.Response[List[sc.Stock]])
async def get_stocks_list(
    limit: int = 25,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Getting a list of stock
    '''
    try:
        query = select(md.Stock).limit(limit).offset(offset)
        result = await session.execute(query)
        stocks = result.scalars().all()

        return {
            'status': 'success',
            'data': stocks,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.post('/stocks/create')
async def create_stocks(
    new_stock: sc.StockCreate,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Create stock item
    '''
    try:
        async with session.begin():
            stock = md.Stock(**new_stock.dict())
            session.add(stock)
            await session.commit()
        return {
            'status': 'success',
            'data': stock,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.patch('/stocks/update/{id}', response_model=sc.Response[sc.Stock])
async def update_stock(
    id: int,
    updated_data: sc.Stock,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Update(Patch) for stock
    '''
    try:
        stmt = select(md.Stock).filter(md.Stock.id == id)
        result = await session.execute(stmt)
        stored_item = result.scalar_one_or_none()

        if not stored_item:
            raise HTTPException(status_code=404, detail={
                'status': 'error',
                'data': None,
                'details': 'Object not found'
            })

        update_data = updated_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(stored_item, field, value)

        await session.commit()
        await session.refresh(stored_item)

        return {
            'status': 'success',
            'data': stored_item,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.delete('/stocks/delete/{id}')
async def delete_stock(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Delete stock by id
    '''
    try:
        stmt = delete(md.Stock).where(md.Stock.id == id)
        await session.execute(stmt)
        await session.commit()

        return {
            'status': 'success',
            'data': f'Deleted stock.id = {id}',
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })

### Warehouses ###


@router.get('/warehouses', response_model=sc.Response[List[sc.Warehouse]])
async def get_warehouses_list(session: AsyncSession = Depends(get_async_session)):
    '''
    Getting list of warehouse
    '''
    try:
        query = select(md.Warehouse).options(selectinload(
            md.Warehouse.stocks))
        result = await session.execute(query)

        return {
            'status': 'success',
            'data': result.scalars().all(),
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.post('/warehouses/create')
async def create_warehouses(
    new_warehouse: sc.WarehouseCreate,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Create warehouse item
    '''
    try:
        async with session.begin():
            warehouse = md.Warehouse(**new_warehouse.dict())
            session.add(warehouse)
            await session.commit()
        return {
            'status': 'success',
            'data': warehouse,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.patch('/warehouses/update/{id}', response_model=sc.Response[sc.Warehouse])
async def update_warehouse(
    id: int,
    updated_data: sc.Warehouse,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Update(Patch) for warehouse
    '''
    try:
        stmt = select(md.Warehouse).filter(md.Warehouse.id == id)
        result = await session.execute(stmt)
        stored_item = result.scalar_one_or_none()

        if not stored_item:
            raise HTTPException(status_code=404, detail={
                'status': 'error',
                'data': None,
                'details': 'Object not found'
            })

        update_data = updated_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(stored_item, field, value)

        await session.commit()
        await session.refresh(stored_item)

        return {
            'status': 'success',
            'data': stored_item,
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })


@router.delete('/warehouses/delete/{id}')
async def delete_warehouse(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Delete warehouse by id
    '''
    try:
        stmt = delete(md.Warehouse).where(md.Warehouse.id == id)
        await session.execute(stmt)
        await session.commit()

        return {
            'status': 'success',
            'data': f'Deleted warehouse.id = {id}',
            'details': None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': str(e)
        })
