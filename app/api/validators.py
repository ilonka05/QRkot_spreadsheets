from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности полученного имени Проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка наличия запрошенного Проекта в БД."""
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )

    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект не найден'
        )
    return charity_project


def check_charity_project_closed(
        fully_invested: bool,
) -> None:
    """Проверка, закрыт ли Проект."""
    if fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_charity_project_full_amount_for_update(
        charity_project_amount: int,
        new_full_amount: int,
) -> CharityProject:
    """
    Проверка, меньше ли измененная требуемая сумма
    уже вложенных Пожертвований.
    """
    if new_full_amount < charity_project_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Сумма для проекта не может быть меньше суммы уже внесенных пожертвований'
        )


async def check_charity_project_invest(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Проверка, было ли выполнено Пожертвование в Проект.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project
