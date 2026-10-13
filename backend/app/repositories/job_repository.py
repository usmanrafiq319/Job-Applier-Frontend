import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job


class JobRepository:

    async def list_for_profile(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID
    ) -> list[Job]:

        result = await db.execute(
            select(Job)
            .where(
                Job.profile_id == profile_id
            )
            .order_by(
                Job.created_at.desc()
            )
        )

        return list(
            result.scalars().all()
        )


    async def get_by_id(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        job_id: uuid.UUID
    ) -> Job | None:

        result = await db.execute(
            select(Job)
            .where(
                Job.id == job_id,
                Job.profile_id == profile_id
            )
        )

        return result.scalar_one_or_none()


    async def create(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        data: dict
    ) -> Job:

        job = Job(
            profile_id=profile_id,
            **data
        )

        db.add(job)

        await db.flush()

        return job


    async def update_status(
        self,
        db: AsyncSession,
        job: Job,
        status: str
    ) -> Job:

        job.status = status

        await db.flush()

        return job