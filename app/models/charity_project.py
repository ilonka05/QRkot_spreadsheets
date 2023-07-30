from sqlalchemy import Column, String, Text

from app.models.base import AbstractBase


class CharityProject(AbstractBase):
    """Модель проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
