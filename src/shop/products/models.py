from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlalchemy import Integer, String, Boolean, Text, DECIMAL, ForeignKey, \
    Enum as EnumType, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, metadata
# from auth.models import User

class Category(Base):
    __tablename__ = 'category'

    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255))
    discount: Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'category.id', ondelete='CASCADE'), nullable=True)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    children: Mapped['Category'] = relationship(
        'Category', backref='parent', remote_side=[id])

    def __repr__(self):
        return f'Category(id={self.id}, name={self.name})'


class Product(Base):
    __tablename__ = 'product'

    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    articul: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    price: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=8, scale=2), default=0.0)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('category.id'))

    stocks: Mapped[Optional[List['Stock']]] = relationship(
        'Stock', back_populates='product')
    photos: Mapped[Optional[List['ProductPhoto']]] = relationship(
        'ProductPhoto', back_populates='product')
    reviews: Mapped[Optional[List['Review']]] = relationship(
        'Review', back_populates='product'
    )

    def __repr__(self) -> str:
        return f'Product(id={self.id!r}, name={self.name!r}, articul={self.articul!r}, is_active={self.is_active!r}, price={self.price!r})'


class ProductPhoto(Base):
    __tablename__ = 'product_photo'

    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('product.id', ondelete='CASCADE'))
    photo_url: Mapped[str] = mapped_column(String(255), default='')

    product: Mapped['Product'] = relationship(
        'Product', back_populates='photos')

    def __repr__(self) -> str:
        return f'ProductPhoto(id={self.id!r}, product_id={self.product_id!r}, photo_url={self.photo_url!r})'


class Warehouse(Base):
    __tablename__ = 'warehouse'

    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))

    stocks: Mapped[List['Stock']] = relationship(
        'Stock', back_populates='warehouse')


class Stock(Base):
    __tablename__ = 'stock'

    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(Integer,
                                              ForeignKey('warehouse.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('product.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    warehouse: Mapped['Warehouse'] = relationship(
        'Warehouse', back_populates='stocks')
    product: Mapped['Product'] = relationship(
        'Product', back_populates='stocks')


class Review(Base):
    class ReviewRating(Enum):
        ONE = '1'
        TWO = '2'
        THREE = '3'
        FOUR = '4'
        FIVE = '5'

    __tablename__ = 'review'

    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey(
                                             'user.id', ondelete='CASCADE')
                                         )
    product_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey(
                                                'product.id', ondelete='CASCADE')
                                            )
    estimate: Mapped[str] = mapped_column(
        EnumType(ReviewRating, name='estimate')
    )
    body: Mapped[str] = mapped_column(
        String, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)

    product: Mapped['Product'] = relationship(
        'Product', back_populates='reviews')


# class Cart(Base):
#     __tablename__ = 'cart'

#     metadata = metadata

#     id: Mapped[int] = mapped_column(
#         Integer, primary_key=True
#     )
#     product_id: Mapped[int] = mapped_column(
#         ForeignKey('product.id', ondelete='CASCADE')
#     )
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey('user.id', ondelete='CASCADE')
#     )
#     amount: Mapped[int] = mapped_column(Integer, default=1)

#     user: Mapped['User'] = relationship(
#         'User', back_populates='cart'
#     )

#     # Доработать при добавлении нескольких складов
#     # warehouse_id: Mapped[int] = mapped_column(
#     #     ForeignKey('')
#     # )
