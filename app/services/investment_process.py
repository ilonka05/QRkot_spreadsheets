
from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, ModelType
from app.models import CharityProject, Donation


async def investment_process(
        db_obj: Union[CharityProject, Donation],
        session: AsyncSession,
) -> ModelType:
    """
    Процесс инвестирования свободных Пожертвований в незакрытые Проекты.
    """
    db_project = await CRUDBase(CharityProject).get_not_fully_invested(session)
    db_donation = await CRUDBase(Donation).get_not_fully_invested(session)
    if not db_project or not db_donation:
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    invest_project = db_project.full_amount - db_project.invested_amount
    invest_donation = db_donation.full_amount - db_donation.invested_amount
    if invest_project > invest_donation:
        db_project.invested_amount += invest_donation
        db_donation.invested_amount += invest_donation
        db_donation.fully_invested = True
        db_donation.close_date = datetime.now()
    elif invest_project == invest_donation:
        db_project.invested_amount += invest_donation
        db_donation.invested_amount += invest_donation
        db_project.fully_invested = True
        db_project.close_date = datetime.now()
        db_donation.fully_invested = True
        db_donation.close_date = datetime.now()
    elif invest_project < invest_donation:
        db_project.invested_amount += invest_project
        db_donation.invested_amount += invest_project
        db_project.fully_invested = True
        db_project.close_date = datetime.now()
    session.add(db_project)
    session.add(db_donation)
    await session.commit()
    return await investment_process(db_obj, session)
