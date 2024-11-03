from typing import Annotated, Optional

from loguru import logger
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response

from . import schemas
from ..database import session
from .services import UserService
from .security import create_access_token
from ..common.security import security_cookie
from ..config import settings

router = APIRouter(prefix='/api/v1/user', tags=['Auth'])


@router.post('/jwt/token', response_model=schemas.Token)
async def create_token(
        response: Response, user: schemas.User, session: Annotated[Session, Depends(session)]
) -> schemas.Token:
    """Создание jwt токена."""

    logger.info('Запрос на создание jwt токена')
    auth_controller = UserService(session=session)
    logger.info('Авторизация пользователя')
    user = auth_controller.auth(user)
    logger.success('Пользователь успешно авторизован')
    logger.info('Генерация токена')
    access_token = create_access_token(data={'id': user.id, 'is_admin': user.is_admin})
    logger.success('Токен успешно сгенерирован')

    response.set_cookie(key='access_token', value=access_token, expires=settings.EXPIRE_TOKEN)

    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post('/login', response_model=schemas.UserAdmin)
async def login(
        token: str,
        access_token: Annotated[Optional[str], Depends(security_cookie)],
        session: Annotated[Session, Depends(session)]
) -> schemas.UserAdmin:
    """Авторизация пользователя."""

    logger.info('Запрос на получение текущего пользователя')
    current_user = UserService(session).get_current_user(token, access_token)
    logger.success('Пользователь успешно получен')
    return current_user


@router.post('/signup', response_model=schemas.Username)
async def signup(user: schemas.User, session: Annotated[Session, Depends(session)]) -> schemas.Username:
    """Регистрация пользователя."""

    logger.info('Запрос на создание пользователя')
    user = UserService(session).create(user)
    logger.success('Пользователь успешно создан')

    return schemas.Username(username=user.username)


@router.post('/logout')
async def logout(response: Response):
    logger.info('Попытка разлогиниться')
    response.delete_cookie('access_token')
    logger.success('Пользователь успешно разлогинился')
    return 'Пользователь успешно разлогинился'
