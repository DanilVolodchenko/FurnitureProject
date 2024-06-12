from pydantic import BaseModel


class Username(BaseModel):
    username: str


class User(Username):
    password: str


class UserAdmin(Username):
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class DecodeToken(BaseModel):
    id: int
    is_admin: bool


class BadRequest(BaseModel):
    detail: str
