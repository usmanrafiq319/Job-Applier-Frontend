import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


class ProjectRepository:

    async def list_for_profile(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID
    ) -> list[Project]:

        result = await db.execute(
            select(Project)
            .where(
                Project.profile_id == profile_id
            )
            .order_by(
                Project.created_at.desc()
            )
        )

        return list(
            result.scalars().all()
        )


    async def get_by_id(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        project_id: uuid.UUID
    ) -> Project | None:

        result = await db.execute(
            select(Project)
            .where(
                Project.id == project_id,
                Project.profile_id == profile_id
            )
        )

        return result.scalar_one_or_none()


    async def create(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        data: dict
    ) -> Project:

        project = Project(
            profile_id=profile_id,
            **data
        )

        db.add(project)

        await db.flush()

        return project


    async def update(
        self,
        db: AsyncSession,
        project: Project,
        data: dict
    ) -> Project:

        for key, value in data.items():
            setattr(
                project,
                key,
                value
            )

        await db.flush()

        return project


    async def delete(
        self,
        db: AsyncSession,
        project: Project
    ) -> None:

        await db.delete(
            project
        )