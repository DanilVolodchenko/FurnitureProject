from typing import Optional, Type

from sqlalchemy.orm import Session

from ..interfaces import RepositoryInterface, ServiceInterface
from ..config import settings
from src.common.exeptions import IncorrectToken
from . import schemas, models
from .repositories import UserRepository
from .exceptions import UserNotFound, UserAlreadyExists
from .security import verify_password, get_password_hash, get_decoded_jwt_token


class UserService(ServiceInterface[UserRepository]):

    def __init__(
            self, session: Session,
            repository: Type[RepositoryInterface] = UserRepository,
    ) -> None:
        super().__init__(session, repository)

    def create(self, user: schemas.User) -> models.User:

        user_db = self.repository.get_by_username(user.username)
        if user_db:
            raise UserAlreadyExists('Пользователь с таким именем уже существует')

        password_hash = get_password_hash(user.password)
        if settings.SECRET_USERNAME in user.username.lower():
            user = models.User(username=user.username, password=password_hash, is_admin=True)
        else:
            user = models.User(username=user.username, password=password_hash)

        return self.repository.create(user, flush=True)

    def get_current_user(self, token: str, access_token: str) -> Optional[schemas.UserAdmin]:
        if token != access_token:
            raise IncorrectToken('Некорректный токен')
        decoded_token = get_decoded_jwt_token(token)
        user = self.repository.get_by_id(decoded_token.id)

        return schemas.UserAdmin(username=user.username, is_admin=user.is_admin, created_date=user.created_date)

    def auth(self, user: schemas.User) -> Optional[models.User]:
        from loguru import logger

        logger.info('Получение пользователя')
        db_user = self.repository.get_by_username(user.username)
        if not db_user:
            raise UserNotFound('Пользователь не найден')
        if not verify_password(user.password, db_user.password):
            raise UserNotFound('Неверный логин или пароль')
        logger.info(f'Пользователь получен: {db_user}')
        return db_user
