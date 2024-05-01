from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def session() -> Session:
    session = session_maker
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


from .auth import models
