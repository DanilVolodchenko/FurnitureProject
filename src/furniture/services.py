import os
import inspect
from typing import Type, Optional
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.interfaces import RepositoryInterface, ServiceInterface
from .repositories import FurnitureRepository, CategoryRepository, ImageRepository
from ..config import settings
from . import schemas, models, typing


class CategoryService(ServiceInterface[CategoryRepository]):
    def __init__(self, session: Session, repository: Type[RepositoryInterface] = CategoryRepository):
        super().__init__(session, repository)

    def create(self, name: str) -> models.Category:
        category = models.Category(name=name)

        return self.repository.create(category, flush=True)

    def get_or_create(self, ident: Optional[int] = None, name: Optional[str] = None) -> models.Category:
        match ident, name:
            case (ident, None):
                category = self.repository.get_by_id(ident)
            case (None, name):
                category = self.repository.get_by_name(name)
            case _:
                func_name = inspect.currentframe().f_code.co_name
                raise ValueError(f'Ident и name небыли переданы в функцию {func_name}')

        if not category:
            return self.repository.create(models.Category(name=name), flush=True)
        return category

    def update(self, name: str, new_name: schemas.Category) -> models.Category:
        category = self.repository.get_by_name(name)
        if not category:
            raise ValueError(f'Не удалось найти категорию {name}')

        return self.repository.update(category, new_name)


class FurnitureService(ServiceInterface[FurnitureRepository]):

    def __init__(self, session: Session, repository: Type[RepositoryInterface] = FurnitureRepository):
        super().__init__(session, repository)

    def create(self, furniture: schemas.Furniture, category_id: int) -> models.Furniture:
        furniture = models.Furniture(name=furniture.name, description=furniture.description, category_id=category_id)

        return self.repository.create(furniture, flush=True)

    def get_by_id(self, ident: int) -> models.Furniture:
        return self.repository.get_by_id(ident)

    def get_all(self) -> list[models.Furniture]:
        return self.repository.get_all()

    def update(self, furniture_product: schemas.UpdateFurniture, category_id: int) -> models.Furniture:
        furniture_product = self.repository.get_by_id(furniture_product.id)
        if not furniture_product:
            raise
        return furniture_product


class ImageService(ServiceInterface[ImageRepository]):

    def __init__(self, session: Session, repository: Type[RepositoryInterface] = ImageRepository):
        super().__init__(session, repository)

    def save_create(self, files: list[UploadFile], furniture_id: int) -> None:
        for file in files:
            *_, file_extension = file.filename.split('.')
            path_media_file = self.get_path_media_file()
            name = uuid4()

            self.create(name=f'{name}.{file_extension}', furniture_id=furniture_id)
            self.save(path_file=f'{path_media_file}/{name}.{file_extension}', file=file)

    def create(self, name: str, furniture_id: int) -> models.Image:
        image = models.Image(name=name, furniture_id=furniture_id)

        return self.repository.create(image)

    def save(self, file, path_file: str):
        with open(path_file, 'wb') as created_file:
            created_file.write(file.file.read())

    def get_furniture_images(self, furniture_id: int) -> list[models.Image]:

        images = self.repository.get_furniture_images(furniture_id)
        return [image.name for image in images]

    def get_furniture_image(self, furniture_id: int, image_name: typing.UUID) -> models.Image:

        return self.repository.get_furniture_image(furniture_id, image_name)

    @staticmethod
    def get_path_media_file() -> str:
        if not os.path.exists(settings.PATH_MEDIA_FILE):
            os.mkdir(settings.PATH_MEDIA_FILE)
        return settings.PATH_MEDIA_FILE
