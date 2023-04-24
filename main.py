from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title = "BAT agregator"
)


class EnumTypes(Enum): # пример вариантов данных которые могут прийти
    left = "left"
    right = "right"

class Degree(BaseModel): # Пример использования перечислений
    id: int 
    type_degree: EnumTypes

class User(BaseModel): 
    id: int
    degree: List[Degree] | None # пример испольщования вложенных моделей


@app.get("/{id}", response_model=User)
async def root(id: int = 0):
    return {'message': 'Hello World'}


async def products():
    pass 
    # get product list

async def user():
    pass
    # get user info