from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import mapped_column

from db.base import Base


class Cart(Base):

    __tablename__ = 'cart'

    user_id = mapped_column(
        BigInteger,
        ForeignKey('user.id', ondelete='cascade'),
        primary_key=True,
        index=True,
        comment='Внешний ключ на пользователя'
    )

    food_id = mapped_column(
        BigInteger,
        ForeignKey('food.id', ondelete='cascade'),
        primary_key=True,
        index=True,
        comment='Внешний ключ на блюдо'
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1,
        comment='Количество блюда в корзине'
    )

    # Define a check constraint
    __table_args__ = (
        CheckConstraint(quantity > 0, name='check_positive_quantity'),
    )
