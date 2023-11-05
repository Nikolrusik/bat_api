from fastapi.responses import JSONResponse
from typing import Any


class ResponseData(JSONResponse):
    def __init__(self, data: Any = None, status_code: int = 200, details: str = "success"):
        if data is None:
            raise ValueError("Data cannot be None")
        content = {
            "details": details,
            "result": data
        }
        super().__init__(content=content, status_code=status_code)
