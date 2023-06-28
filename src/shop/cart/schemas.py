from typing import Optional
from schemas import BaseOrmModel
import json


class CartBase(BaseOrmModel):
    product_id: int
    user_id: int
    amount: int


class CartCreate(CartBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Cart(CartBase):
    id: int
