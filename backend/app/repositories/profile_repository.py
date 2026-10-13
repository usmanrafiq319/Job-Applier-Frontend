from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile


class ProfileRepository:

    async def get_profile(
        self,
        db: AsyncSession
    ) -> Profile | None:

        result = await db.execute(
            select(Profile)
            .limit(1)
        )

        return result.scalar_one_or_none()


    async def create_profile(
        self,
        db: AsyncSession,
        data: dict
    ) -> Profile:

        profile = Profile(
            **data
        )

        db.add(profile)

        await db.flush()

        return profile


    async def update_profile(
        self,
        db: AsyncSession,
        profile: Profile,
        data: dict
    ) -> Profile:

        for key, value in data.items():

            setattr(
                profile,
                key,
                value
            )

        await db.flush()

        return profile