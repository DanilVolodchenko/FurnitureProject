import uvicorn
from loguru import logger

from server import build_app
from config import settings


def start():
    logger.add('../log/file_{time:YYYY-MM-DD}.log', retention=7, level='INFO')
    app = build_app()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == '__main__':
    start()
