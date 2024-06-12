from jose import JWTError, jwt
from passlib.context import CryptContext

from . import schemas
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_decoded_jwt_token(token: str) -> schemas.DecodeToken:
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise JWTError('Не удалось расшифровать токен')
    return schemas.DecodeToken(**decoded_jwt)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
