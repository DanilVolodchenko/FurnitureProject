from typing import Type, Optional, get_args

from sqlalchemy.orm import Session, Query
from pydantic import BaseModel

from src.database import Base


class RepositoryInterface[T: Base]:
    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def model(self) -> Type[T]:
        model_type, *_ = get_args(self.__orig_bases__[0])
        return model_type

    @property
    def query(self) -> Query:
        return self.session.query(self.model)

    def get_by_id(self, ident: int) -> Optional[T]:
        return self.query.filter(self.model.id == ident).first()

    def get_all(self) -> list[T]:
        return self.query.all()

    def create(self, item: T, *, flush: bool = False) -> T:
        self.session.add(item)
        if flush:
            self.session.flush()

        return item

    def update(self, item: T, new_item: BaseModel, flush: bool = False) -> T:
        for key, value in new_item.model_dump().items():
            if hasattr(item, key):
                setattr(item, key, value)

        if flush:
            self.session.flush()
        return item


class ServiceInterface[T: RepositoryInterface]:

    def __init__(self, session: Session, repository: Type[T]) -> None:
        self.__repository = repository
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def repository(self) -> T:
        return self.__repository(self.session)
