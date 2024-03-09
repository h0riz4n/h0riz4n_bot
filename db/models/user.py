from datetime import datetime

import pytz as pytz
from sqlalchemy import Column, BigInteger, String, DateTime

from db.base import Base


class User(Base):

    __tablename__ = "user"

    id = Column(
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=False,
        comment="Уникальный идентификатор пользователя"
    )

    username = Column(
        String(32),
        nullable=True,
        unique=True,
        comment='Имя пользователя'
    )

    creation_date_time = Column(
        DateTime(),
        nullable=False,
        comment="Время запуска бота"
    )

