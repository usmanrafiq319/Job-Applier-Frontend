import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.experience import Experience


class ExperienceRepository:

    async def list_for_profile(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID
    ) -> list[Experience]:

        result = await db.execute(
            select(Experience)
            .where(
                Experience.profile_id == profile_id
            )
            .order_by(
                Experience.start_date.desc()
            )
        )

        return list(
            result.scalars().all()
        )


    async def get_by_id(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        experience_id: uuid.UUID
    ) -> Experience | None:

        result = await db.execute(
            select(Experience)
            .where(
                Experience.id == experience_id,
                Experience.profile_id == profile_id
            )
        )

        return result.scalar_one_or_none()


    async def create(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        data: dict
    ) -> Experience:

        experience = Experience(
            profile_id=profile_id,
            **data
        )

        db.add(experience)

        await db.flush()

        return experience


    async def update(
        self,
        db: AsyncSession,
        experience: Experience,
        data: dict
    ) -> Experience:

        for key, value in data.items():

            setattr(
                experience,
                key,
                value
            )

        await db.flush()

        return experience


    async def delete(
        self,
        db: AsyncSession,
        experience: Experience
    ) -> None:

        await db.delete(
            experience
        )