from typing import Optional, Type

from sqlalchemy.orm import Session

from src.abc import Controller, Service
from src.config import settings
from . import schemas, models
from .services import UserService
from .exceptions import UserNotFound, IncorrectToken, UserAlreadyExists
from .security import verify_password, get_password_hash, get_decoded_jwt_token


class UserController(Controller[UserService]):

    def __init__(
            self, session: Session,
            service: Type[Service] = UserService,
    ) -> None:
        super().__init__(session, service)

    def create(self, user: schemas.User) -> models.User:

        user_db = self.service.get_by_username(user.username)
        if user_db:
            raise UserAlreadyExists('Пользователь с таким именем зарегистрирован')

        password_hash = get_password_hash(user.password)
        if settings.SECRET_USERNAME in user.username.lower():
            user = models.User(username=user.username, password=password_hash, is_admin=True)
        else:
            user = models.User(username=user.username, password=password_hash)

        return self.service.create(user, flush=True)

    def get_current_user(self, token: str, access_token: str) -> Optional[schemas.UserAdmin]:
        if token != access_token:
            raise IncorrectToken('Некорректный токен')
        decoded_token = get_decoded_jwt_token(token)
        user = self.service.get_by_id(decoded_token.id)

        return schemas.UserAdmin(username=user.username, is_admin=user.is_admin)

    def auth(self, user: schemas.User) -> Optional[models.User]:
        db_user = self.service.get_by_username(user.username)
        if not db_user:
            raise UserNotFound('Пользователь не найден')
        if not verify_password(user.password, db_user.password):
            raise UserNotFound('Неверный логин или пароль')
        return db_user
