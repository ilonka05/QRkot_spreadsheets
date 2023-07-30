from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.base import AbstractBase


class Donation(AbstractBase):
    """Модель пожертвований."""
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
