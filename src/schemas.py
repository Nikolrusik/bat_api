
from pydantic import BaseModel, validator, ValidationError
from pydantic.generics import GenericModel
from typing import Any, List, Optional, TypeVar, Generic


DataT = TypeVar('DataT')


class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True


class Response(GenericModel, Generic[DataT]):
    '''
    Response is a generic model that takes a type parameter DataT. It has three fields:

    status: Represents the status of the response (e.g., "success", "error").
    result: Represents the actual data being returned. It uses the DataT type parameter, allowing you to specify the specific model you want to use.
    details: Represents additional details or information about the response. It is optional and can be None.
    '''
    result: DataT
    details: Optional[str] = None
