import tempfile
import os
from fastapi import UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from shop.products import models as md


from aws_config import s3_client, AWS_FILTEPATH_GET

#   photo_data = await photo.read()
#                 # временное хранилище файлов
#                 temp_url = f'./static/temp/{photo.filename}'

#                 product_photo = md.ProductPhoto(
#                     product_id=product.id, photo_url=f'temp_none')
#                 session.add(product_photo)
#                 await session.flush()

#                 aws_filename = f'proudct_{product_photo.id}.png'
#                 product_photo.photo_url = f'{AWS_FILTEPATH_GET}/product/{aws_filename}'
#                 with open(temp_url, 'wb') as file:
#                     file.write(photo_data)
#                     s3_client.upload_file(
#                         temp_url, test_bucket_name, f'static/product/{aws_filename}')
#                     os.remove(temp_url)

test_bucket_name = 'bat_test'

async def save_product_photo(product: md.Product, photo: UploadFile, session: AsyncSession):
    aws_filename = f'product_{product.id}.png'
    s3_key = f'static/product/{aws_filename}'

    # Сохраняем файл во временное хранилище
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_url = temp_file.name
        temp_file.write(await photo.read())

    try:
        # Загружаем файл на сервер Amazon S3
        s3_client.upload_file(temp_url, test_bucket_name, s3_key)

        # Обновляем информацию о фотографии продукта
        product_photo = md.ProductPhoto(product_id=product.id, photo_url=f'{AWS_FILTEPATH_GET}/{s3_key}')
        session.add(product_photo)
        await session.flush()

        # return product_photo
        print('Uploaded')
    finally:
        # Удаляем временный файл
        os.remove(temp_url)