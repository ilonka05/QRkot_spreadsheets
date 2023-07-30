from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """
    Базовый класс Pydantic-схемы для Проекта,
    от которого наследуются все остальные классы.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Pydantic-схема создания Проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    @validator('name', 'description')
    def name_and_description_cant_be_none(cls, value: str):
        """Проверка наполнения полей 'name' и 'description'."""
        if not value or value is None:
            raise ValueError('Поля "name" и "description" не должны быть пустыми')
        return value


class CharityProjectUpdate(CharityProjectBase):
    """Pydantic-схема для обновления Проекта."""

    @validator('name', 'description', 'full_amount')
    def field_cannot_be_null(cls, value: str):
        """Проверка полей на то, что они не равны None."""
        if value is None:
            raise ValueError('Поля не могут быть пустыми')
        return value


class CharityProjectDB(CharityProjectCreate):
    """Pydantic-схема, описывающая Проект, полученный из БД."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
