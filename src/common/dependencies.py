from typing import Annotated

from fastapi import Depends, Request

from src.fastapi_overrides import CustomAPIKeyCookie
from src.common.exeptions import IncorrectToken

security_cookie = CustomAPIKeyCookie(name='access_token')


def check_token(request: Request, expected_token: Annotated[str, Depends(security_cookie)]) -> None:
    if not expected_token or request.cookies.get('access_token') != expected_token:
        raise IncorrectToken('Некорректный токен')
