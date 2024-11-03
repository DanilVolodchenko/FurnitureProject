from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from loguru import logger

from .auth import auth_router
from .furniture import back_router
from .common.schemas import BaseResponseStructural

logger.add('log/file_{time:DD-MM-YYYY}.log', retention=7, level='INFO')

__version__ = (0, 0, 0)


class BaseResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, *args, **kwargs) -> None:
        content = BaseResponseStructural(content=content, error=False, error_desc='').model_dump()
        super().__init__(content, status_code, *args, **kwargs)


app = FastAPI(
    version='.'.join(map(str, __version__)),
    title='FurnitureProject',
    default_response_class=BaseResponse,
    debug=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.exception_handler(Exception)
def error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        {
            'content': '',
            'error': True,
            'error_desc': f'{exc.__class__.__name__} {exc}'
        },
    )


@app.exception_handler(RequestValidationError)
def bad_request(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        {
            'content': '',
            'error': True,
            'error_desc': f'{exc.__class__.__name__} {exc}'
        },
    )


@app.exception_handler(ValidationError)
def bad_request(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        {
            'content': '',
            'error': True,
            'error_desc': f'{exc.__class__.__name__} {exc}'
        },
    )


app.include_router(auth_router)
app.include_router(back_router)

app.mount('/media', StaticFiles(directory='media'), 'media')
