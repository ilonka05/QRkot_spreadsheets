from typing import List, Dict, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate
]):
    """Класс проектов, унаследованный от базового класса."""

    async def update(
            self,
            db_obj: CharityProject,
            obj_in: CharityProjectUpdate,
            session: AsyncSession,
    ) -> CharityProject:
        """Обновить Проект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db_obj: CharityProject,
            session: AsyncSession,
    ) -> CharityProject:
        """Удалить Проект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Проверка уникальности имени Проекта."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[Dict[str, str]]:
        """Сортировка списка со всеми закрытыми Проектами."""
        projects_closed = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )
        projects_closed = projects_closed.scalars().all()
        projects = []
        for project in projects_closed:
            projects.append({
                'name': project.name,
                'collection_time': project.close_date - project.create_date,
                'description': project.description
            })
        projects = sorted(projects, key=lambda date: date['collection_time'])
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
