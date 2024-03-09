from sqlalchemy import Column, String, Integer

from db.base import Base


class FoodType(Base):

    __tablename__ = 'food_type'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='Уникальный идентификатор типа блюда'
    )

    name = Column(
        String(64),
        nullable=False,
        unique=True,
        comment='Название типа блюда'
    )
