import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.repositories.project_repository import (
    ProjectRepository,
)

from app.schemas.project import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)


class ProjectNotFoundError(Exception):
    pass


class ProfileNotFoundError(Exception):
    pass


class ProjectService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.project_repository = (
            ProjectRepository()
        )


    async def _get_profile(
        self,
        db: AsyncSession
    ):

        profile = (
            await self.profile_repository
            .get_profile(db)
        )

        if profile is None:
            raise ProfileNotFoundError()

        return profile


    async def get_projects(
        self,
        db: AsyncSession
    ):

        profile = await self._get_profile(
            db
        )

        return (
            await self.project_repository
            .list_for_profile(
                db,
                profile.id
            )
        )


    async def add_project(
        self,
        db: AsyncSession,
        payload: ProjectCreateRequest
    ):

        profile = await self._get_profile(
            db
        )

        data = payload.model_dump()

        data["technologies"] = [
            technology.strip()
            for technology in data["technologies"]
            if technology.strip()
        ]

        project = (
            await self.project_repository
            .create(
                db,
                profile.id,
                data
            )
        )

        await db.commit()
        await db.refresh(project)

        return project


    async def update_project(
        self,
        db: AsyncSession,
        project_id: uuid.UUID,
        payload: ProjectUpdateRequest
    ):

        profile = await self._get_profile(
            db
        )

        project = (
            await self.project_repository
            .get_by_id(
                db,
                profile.id,
                project_id
            )
        )

        if project is None:
            raise ProjectNotFoundError()

        data = payload.model_dump(
            exclude_unset=True
        )

        if (
            "technologies" in data
            and data["technologies"] is not None
        ):

            data["technologies"] = [
                technology.strip()
                for technology in data["technologies"]
                if technology.strip()
            ]

        project = (
            await self.project_repository
            .update(
                db,
                project,
                data
            )
        )

        await db.commit()
        await db.refresh(project)

        return project


    async def delete_project(
        self,
        db: AsyncSession,
        project_id: uuid.UUID
    ) -> None:

        profile = await self._get_profile(
            db
        )

        project = (
            await self.project_repository
            .get_by_id(
                db,
                profile.id,
                project_id
            )
        )

        if project is None:
            raise ProjectNotFoundError()

        await self.project_repository.delete(
            db,
            project
        )

        await db.commit()