from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    """
    Базовый класс Pydantic-схемы для Пожертвований,
    от которого наследуются все остальные классы.
    """
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Pydantic-схема для Пожертвований."""
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    """
    Pydantic-схема, описывающая Пожертвования, полученные из БД.
    """
    id: int
    create_date: datetime
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
