from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlalchemy import Integer, String, Boolean, Text, DECIMAL, ForeignKey, \
    Enum as EnumType, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from auth.models import User
from shop.products.models import Product

from database import Base, metadata


class Cart(Base):
    __tablename__ = 'cart'

    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE')
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE')
    )
    amount: Mapped[int] = mapped_column(Integer, default=1)


    user: Mapped['User'] = relationship(
        'User', back_populates='cart'
    )
    product: Mapped['Product'] = relationship(
        'Product', back_populates='cart'
    )

    # Доработать при добавлении нескольких складов
    # warehouse_id: Mapped[int] = mapped_column(
    #     ForeignKey('')
    # )