from fastapi import UploadFile
from sqlalchemy.orm import Session

from . import schemas, models
from .services import FurnitureService, CategoryService, ImageService


class Manager:

    def __init__(
            self, category_service: CategoryService, furniture_service: FurnitureService, image_service: ImageService
    ) -> None:
        self.category_service = category_service
        self.furniture_service = furniture_service
        self.image_service = image_service

    def create(self, created_furniture: schemas.CreateFurniture, files: list[UploadFile]) -> models.Furniture:
        category = self.category_service.get_or_create(name=created_furniture.category_name)
        furniture = self.furniture_service.create(furniture=created_furniture, category_id=category.id)
        self.image_service.save_create(files=files, furniture_id=furniture.id)

        return furniture

    def update(self, furniture_id: int, updated_furniture: schemas.UpdateFurniture, files: list[UploadFile]) -> None:
        exist_furniture_product = self.furniture_service.get_by_id(updated_furniture.id)
        new_category = self.category_service.update(
            name=exist_furniture_product.category.name, new_name=updated_furniture.category_name
        )
        new_furniture = self.furniture_service.update(updated_furniture)
