from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate
]):
    """Класс пожертвований, унаследованный от базового класса."""

    async def get_user_donations(
            self,
            user: User,
            session: AsyncSession,
    ) -> List[Donation]:
        """Вернуть список пожертвований пользователя, выполняющего запрос."""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
