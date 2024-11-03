from typing import Any

from pydantic import BaseModel


class BaseResponseStructural(BaseModel):
    content: Any
    error: bool
    error_desc: str
