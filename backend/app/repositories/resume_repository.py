import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.models.resume_chunk import ResumeChunk


class ResumeRepository:

    async def get_active(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID
    ) -> Resume | None:

        result = await db.execute(
            select(Resume)
            .where(
                Resume.profile_id
                == profile_id,

                Resume.is_active.is_(True)
            )
            .order_by(
                Resume.created_at.desc()
            )
            .limit(1)
        )

        return result.scalar_one_or_none()


    async def deactivate_existing(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID
    ) -> None:

        result = await db.execute(
            select(Resume)
            .where(
                Resume.profile_id
                == profile_id,

                Resume.is_active.is_(True)
            )
        )


        for resume in result.scalars():

            resume.is_active = False


        await db.flush()


    async def create_resume(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        data: dict
    ) -> Resume:

        resume = Resume(
            profile_id=profile_id,
            **data
        )

        db.add(resume)

        await db.flush()

        return resume


    async def create_chunk(
        self,
        db: AsyncSession,
        resume_id: uuid.UUID,
        data: dict
    ) -> ResumeChunk:

        chunk = ResumeChunk(
            resume_id=resume_id,
            **data
        )

        db.add(chunk)

        await db.flush()

        return chunk


    async def delete_resume(
        self,
        db: AsyncSession,
        resume: Resume
    ) -> None:

        await db.delete(
            resume
        )