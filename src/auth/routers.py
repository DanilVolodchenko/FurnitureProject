from typing import Annotated

from loguru import logger
from sqlalchemy.orm import Session
from fastapi.security import APIKeyCookie
from fastapi import APIRouter, Depends, Response, Request

from src.database import session
from . import schemas
from .controllers import UserController
from .security import create_access_token

router = APIRouter(prefix='/api/v1', tags=['Auth'])

security_cookie = APIKeyCookie(name='access_token')


@router.post('/jwt/token', response_model=schemas.Token)
async def create_token(
        request: Response, user: schemas.User, session: Annotated[Session, Depends(session)]
) -> schemas.Token:
    """Создание jwt токена."""

    logger.info('Запрос на создание jwt токена')
    auth_controller = UserController(session=session)
    logger.info('Авторизация пользователя')
    user = auth_controller.auth(user)
    logger.success('Пользователь успешно авторизован')
    logger.info('Генерация токена')
    access_token = create_access_token(data={'id': user.id, 'is_admin': user.is_admin})
    logger.success('Токен успешно сгенерирован')

    request.set_cookie(key='access_token', value=access_token)

    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post('/user/me', response_model=schemas.UserAdmin)
async def me(
        request: Request, token: str, access_token: Annotated[str | None, Depends(security_cookie)],
        session: Annotated[Session, Depends(session)]
) -> schemas.UserAdmin:
    """Авторизация пользователя."""

    logger.info('Запрос на получение текущего пользователя')
    current_user = UserController(session).get_current_user(token, access_token)
    logger.success('Пользователь успешно получен')
    return current_user


@router.post('/register', response_model=schemas.Username)
async def register(user: schemas.User, session: Annotated[Session, Depends(session)]) -> schemas.Username:
    """Регистрация пользователя."""

    logger.info('Запрос на создание пользователя')
    user = UserController(session).create(user)
    logger.success('Пользователь успешно создан')

    return schemas.Username(username=user.username)
