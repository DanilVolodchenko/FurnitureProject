from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Furniture(Base):
    __tablename__ = 'furnitures'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    created_date: Mapped[date] = mapped_column(default=date.today())

    category: Mapped['Category'] = relationship(back_populates='furnitures')
    images: Mapped[list['Image']] = relationship(back_populates='furniture')


class Image(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    furniture_id: Mapped[int] = mapped_column(ForeignKey('furnitures.id'))

    furniture: Mapped['Furniture'] = relationship(back_populates='images')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    furnitures: Mapped[list['Furniture']] = relationship(back_populates='category')
