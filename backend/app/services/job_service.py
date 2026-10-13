import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.job_repository import (
    JobRepository,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.schemas.job import (
    JobCreateRequest,
    JobStatusUpdateRequest,
)


class JobProfileNotFoundError(Exception):
    pass


class JobNotFoundError(Exception):
    pass


class JobService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.job_repository = (
            JobRepository()
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
            raise JobProfileNotFoundError()

        return profile


    async def get_jobs(
        self,
        db: AsyncSession
    ):

        profile = await self._get_profile(
            db
        )

        return (
            await self.job_repository
            .list_for_profile(
                db,
                profile.id
            )
        )


    async def get_job(
        self,
        db: AsyncSession,
        job_id: uuid.UUID
    ):

        profile = await self._get_profile(
            db
        )

        job = (
            await self.job_repository
            .get_by_id(
                db,
                profile.id,
                job_id
            )
        )

        if job is None:
            raise JobNotFoundError()

        return job


    async def create_job(
        self,
        db: AsyncSession,
        payload: JobCreateRequest
    ):

        profile = await self._get_profile(
            db
        )

        data = payload.model_dump()

        data["title"] = (
            data["title"].strip()
        )

        data["company"] = (
            data["company"].strip()
        )

        data["description"] = (
            data["description"].strip()
        )

        job = (
            await self.job_repository
            .create(
                db,
                profile.id,
                data
            )
        )

        await db.commit()

        await db.refresh(
            job
        )

        return job


    async def update_status(
        self,
        db: AsyncSession,
        job_id: uuid.UUID,
        payload: JobStatusUpdateRequest
    ):

        profile = await self._get_profile(
            db
        )

        job = (
            await self.job_repository
            .get_by_id(
                db,
                profile.id,
                job_id
            )
        )

        if job is None:
            raise JobNotFoundError()

        job = (
            await self.job_repository
            .update_status(
                db,
                job,
                payload.status
            )
        )

        await db.commit()

        await db.refresh(
            job
        )

        return job