from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_date: Mapped[date] = mapped_column(default=date.today())

    def __repr__(self) -> str:
        return f'username={self.username}, is_admin={self.is_admin}'
