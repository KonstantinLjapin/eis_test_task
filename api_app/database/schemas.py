from pydantic import BaseModel
from typing import Union


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None

