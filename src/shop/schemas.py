from typing import Any, List, Optional
from pydantic import BaseModel
import json

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


# Cart Schemas

class CartBase(BaseModel):
    product_id: int
    user_id: int
    amount: int


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int
