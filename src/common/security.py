from typing import Annotated

from fastapi import Depends, Request, security

from src.common.exeptions import IncorrectToken, UserNotAuthenticated


class CustomAPIKeyCookie(security.APIKeyCookie):
    def __call__(self, request: Request) -> str | None:
        api_key = request.cookies.get(self.model.name)
        if not api_key:
            if self.auto_error:
                raise UserNotAuthenticated('Пользователь не авторизован')
            else:
                return None
        return api_key


security_cookie = CustomAPIKeyCookie(name='access_token')


def check_token(request: Request, expected_token: Annotated[str, Depends(security_cookie)]) -> None:
    if not expected_token or request.cookies.get('access_token') != expected_token:
        raise IncorrectToken('Некорректный токен')
