from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import mapped_column

from db.base import Base


class Food(Base):

    __tablename__ = 'food'

    id = Column(
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=True,
        index=True,
        comment='Уникальный идентификатор блюда'
    )

    name = Column(
        String(64),
        nullable=False,
        unique=True,
        comment='Название блюда'
    )

    food_type = mapped_column(
        Integer,
        ForeignKey('food_type.id', ondelete='cascade'),
        comment='Внешний ключ на тип блюда'
    )

    ingredients = Column(
        String(198),
        nullable=False,
        comment='Ингридиенты блюда'
    )

    price = Column(
        Integer,
        nullable=False,
        comment='Цена блюда'
    )

    preview = Column(
        String(255),
        nullable=False,
        comment='Превью блюда'
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=False,
        comment='Статус активности блюда'
    )

    # Define a check constraint
    __table_args__ = (
        CheckConstraint(price > 0, name='check_positive_price'),
    )
