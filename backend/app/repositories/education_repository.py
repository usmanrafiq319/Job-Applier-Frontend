import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.education import Education


class EducationRepository:

    async def list_for_profile(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID
    ) -> list[Education]:

        result = await db.execute(
            select(Education)
            .where(
                Education.profile_id == profile_id
            )
            .order_by(
                Education.start_date.desc()
            )
        )

        return list(
            result.scalars().all()
        )


    async def get_by_id(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        education_id: uuid.UUID
    ) -> Education | None:

        result = await db.execute(
            select(Education)
            .where(
                Education.id == education_id,
                Education.profile_id == profile_id
            )
        )

        return result.scalar_one_or_none()


    async def create(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        data: dict
    ) -> Education:

        education = Education(
            profile_id=profile_id,
            **data
        )

        db.add(education)

        await db.flush()

        return education


    async def update(
        self,
        db: AsyncSession,
        education: Education,
        data: dict
    ) -> Education:

        for key, value in data.items():
            setattr(
                education,
                key,
                value
            )

        await db.flush()

        return education


    async def delete(
        self,
        db: AsyncSession,
        education: Education
    ) -> None:

        await db.delete(
            education
        )