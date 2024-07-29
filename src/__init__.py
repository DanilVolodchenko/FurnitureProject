from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from loguru import logger

from .auth import auth_router
from .furniture import back_router
from .default_response import DefaultResponse

logger.add('log/file_{time:YYYY-MM-DD}.log', retention=7, level='INFO')

__version__ = (0, 0, 0)

app = FastAPI(
    version='.'.join(map(str, __version__)),
    title='FurnitureProject',
    default_response_class=DefaultResponse,
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
def error_handler(request: Request, exc: Exception):
    return DefaultResponse(
        content=f'{exc}',
        status_code=HTTPStatus.BAD_REQUEST
    )
    # JSONResponse(
    #     status_code=HTTPStatus.BAD_REQUEST,
    #     content={'detail': f'{exc}'},
    # )


@app.exception_handler(RequestValidationError)
def bad_request(request: Request, exc: Exception):
    return DefaultResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=f'Проверьте валидность отправленного JSON: {exc}'
    )
    # return JSONResponse(
    #     status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    #     content={'detail': f'Проверьте валидность отправленного JSON: {exc}'}
    # )


app.include_router(auth_router)
app.include_router(back_router)

app.mount('/media', StaticFiles(directory='media'), 'media')
