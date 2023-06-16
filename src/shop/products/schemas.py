from typing import Any, List, Optional, TypeVar, Generic

from pydantic import BaseModel, validator, ValidationError
from pydantic.generics import GenericModel

import json

DataT = TypeVar('DataT')


class Response(GenericModel, Generic[DataT]):
    '''
    Response is a generic model that takes a type parameter DataT. It has three fields:

    status: Represents the status of the response (e.g., "success", "error").
    data: Represents the actual data being returned. It uses the DataT type parameter, allowing you to specify the specific model you want to use.
    detail: Represents additional details or information about the response. It is optional and can be None.
    '''

    status: str
    data: DataT
    details: Optional[str]


# Category schemas


class CategoryBase(BaseModel):
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


class StockBase(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    id: int

    class Config:
        orm_mode = True

# Product schemas


class ProductBase(BaseModel):
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


class Product(ProductBase):
    id: int
    stocks: List[Stock] = []

    class Config:
        orm_mode = True

# Warehouse schemas


class WarehouseBase(BaseModel):
    name: str


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase):
    id: int


# Reviews schemas


class ReviewBase(BaseModel):
    body: str
    product_id: int
    user_id: int
    estimate: str


class ReviwsCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
