from typing import Type, Optional, get_args

from sqlalchemy.orm import Session, Query


class Controller[T]:

    def __init__(self, session: Session, service: T) -> None:
        self.__service = service
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def service(self) -> T:
        return self.__service(self.session)


class Service[T]:
    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def model(self) -> Type[T]:
        model_type, *_ = get_args(self.__orig_bases__[0])
        return model_type

    def commit(self) -> None:
        self.session.commit()

    @property
    def query(self) -> Query:
        return self.session.query(self.model)

    def create(self, item: T, *, flush: bool = False) -> T:
        self.session.add(item)
        if flush:
            self.session.flush()

        return item

    def get_by_id(self, id_: int) -> Optional[T]:
        return self.query.filter(self.model.id == id_).first()

    def get_all(self) -> list[T]:
        return self.query.all()
