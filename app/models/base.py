from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class AbstractBase(Base):
    """Родительский класс для моделей CharityProject и Donation."""
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self) -> str:
        return (
            f'Требуемая сумма на проект {self.full_amount}, '
            f'Внесённая сумма {self.invested_amount}'
        )
