from fastapi import UploadFile

from .exceptions import IncorrectFile


def validate_media_type(files: list[UploadFile]) -> list[UploadFile]:
    for file in files:
        if not file.content_type.startswith('image'):
            raise IncorrectFile('Передан некорректный файл. Передавать нужно изображение.')

    return files
