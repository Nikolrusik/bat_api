from typing import List, Optional
from datetime import datetime

import json

from schemas import BaseOrmModel


# Category schemas


class CategoryBase(BaseOrmModel):
    name: str
    discount: int
    is_active: bool
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Category(CategoryBase):
    id: int
    photo_url: Optional[str] = None

# Stock schemas


class StockBase(BaseOrmModel):
    product_id: int
    warehouse_id: int
    quantity: int


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    id: int


# Product schemas


class ProductBase(BaseOrmModel):
    name: str
    articul: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    price: float
    category_id: int = 1


class ProductCreate(ProductBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ProductUpdate(ProductBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ProductForList(ProductBase):
    id: int
    photos: List


class Product(ProductForList):
    stocks: List[Stock]
    reviews: List

### Reviews ###


class ReviewBase(BaseOrmModel):
    user_id: int
    product_id: int
    estimate: int
    body: str
    created_at: datetime


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int


# Warehouse schemas


class WarehouseBase(BaseOrmModel):
    name: str


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase):
    id: int
    stock: list = []


# Reviews schemas


class ReviewBase(BaseOrmModel):
    body: str
    product_id: int
    user_id: int
    estimate: str


class ReviwsCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
