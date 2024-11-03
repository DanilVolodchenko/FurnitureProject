from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Path, Request
from sqlalchemy.orm import Session

from src.database import session
from . import schemas, typing
from .managers import Manager
from .services import FurnitureService, ImageService
from .validators import validate_media_type
from src.common.utils import check_token

router = APIRouter(prefix='/api/v1', tags=['Furniture'])


@router.get('/furniture/{furniture_id}')
async def get_furniture(furniture_id: Annotated[int, Path()], session: Annotated[Session, Depends(session)]):
    return FurnitureService(session).get_by_id(furniture_id)


@router.get('/furniture')
async def get_furnitures(session: Annotated[Session, Depends(session)]):
    return FurnitureService(session).get_all()


@router.get('/furniture/{furniture_id}/images')
async def get_images(furniture_id: int, session: Annotated[Session, Depends(session)]):
    """Получение media путей."""

    return ImageService(session).get_furniture_images(furniture_id)


@router.get('/furniture/{furniture_id}/image/{image_uuid}')
async def get_image(furniture_id: int, image_name: typing.UUID, session: Annotated[Session, Depends(session)]):
    """Получение изображения мебели по имени."""

    return ImageService(session).get_furniture_image(furniture_id, image_name)


@router.post('/furniture', dependencies=[Depends(check_token)])
async def create_furniture(
        request: Request,
        furniture_data: Annotated[schemas.CreateFurniture, Depends()],
        files: Annotated[list[UploadFile], Depends(validate_media_type)],
        session: Annotated[Session, Depends(session)]
):
    """Создание мебельного продукта."""

    return Manager(session).create(furniture=furniture_data, files=files)


@router.put('/furniture/{furniture_id}')
async def update_furniture(
        furniture_id: Annotated[int, Path()],
        furniture_data: Annotated[schemas.UpdateFurniture, Depends()],
        files: Annotated[list[UploadFile], Depends(validate_media_type)],
        session: Annotated[Session, Depends(session)]
):
    """Обновление мебельного продукта."""

    return Manager(session).update(furniture=furniture_data, files=files)


@router.put('/category/{category_id}')
async def update_category(
        category_id: int, category_s: schemas.Furniture,
        session: Annotated[Session, Depends(session)]
):
    from .repositories import CategoryRepository
    from .models import Category

    rep = CategoryRepository(session)
    category: Category = rep.query.filter(Category.id == category_id).first()
    if category:
        res = rep.update(category, category_s)
    else:
        return 'Error'
    return category
