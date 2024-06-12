from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from auth import auth_router
from furniture import back_router

__version__ = (0, 0, 0)


def build_app() -> FastAPI:
    app = FastAPI(
        version='.'.join(map(str, __version__)),
        title='FurnitureProject'
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
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={'detail': f'{exc}'},
        )

    @app.exception_handler(RequestValidationError)
    def bad_request(request: Request, exc: Exception):
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content={'detail': f'Проверьте валидность отправленного JSON: {exc}'}
        )

    app.include_router(auth_router)
    app.include_router(back_router)

    return app
