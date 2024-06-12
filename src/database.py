from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


SQLALCHEMY_DATABASE_URL = 'sqlite:///../database.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def session() -> Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise
    finally:
        session.close()


from src.auth import models
from src.furniture import models
