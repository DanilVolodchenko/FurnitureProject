from typing import Optional
from enum import StrEnum

from pydantic import BaseModel


class CategoryName(StrEnum):
    LIVING_ROOM = 'Гостиные'
    BED_ROOM = 'Спальни'
    HALLWAY = 'Прихожие'
    CHILDREN = 'Детские'
    KITCHEN = 'Кухни'
    OTHER = 'Другое'


class Category(BaseModel):
    name: CategoryName


class Furniture(BaseModel):
    name: str
    category_name: Category
    description: Optional[str] = None


class CreateFurniture(Furniture):
    category_name: CategoryName  # Делается это для того, чтобы все поля передавались в как query параметр


class UpdateFurniture(Furniture):
    id: int


class Image(BaseModel):
    name: str