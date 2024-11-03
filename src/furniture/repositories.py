from typing import Optional

from sqlalchemy.orm import joinedload

from src.interfaces import RepositoryInterface
from . import schemas, models, typing


class FurnitureRepository(RepositoryInterface[models.Furniture]):

    def get_all(self) -> list[models.Furniture]:
        return self.query.options(
            joinedload(self.model.category),
            joinedload(self.model.images)
        ).all()

    def get_by_id(self, ident: int) -> models.Furniture:
        return self.query.options(
            joinedload(self.model.category),
            joinedload(self.model.images)
        ).filter(self.model.id == ident).first()


class CategoryRepository(RepositoryInterface[models.Category]):

    def get_by_name(self, name: str) -> Optional[models.Category]:
        return self.query.filter(self.model.name == name).first()


class ImageRepository(RepositoryInterface[models.Image]):

    def get_furniture_images(self, furniture_id: int) -> list[models.Image]:
        return self.query.filter(self.model.furniture_id == furniture_id).all()

    def get_furniture_image(self, furniture_id: int, image_name: typing.UUID) -> models.Image:
        return self.query.options(
            joinedload(self.model.furniture),
        ).filter(
            self.model.furniture_id == furniture_id, self.model.name == image_name
        ).first()
