from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.schemas.profile import (
    ProfileUpsertRequest,
)


class ProfileService:

    def __init__(self):

        self.repository = ProfileRepository()


    async def get_profile(
        self,
        db: AsyncSession
    ) -> Profile | None:

        return await self.repository.get_profile(
            db
        )


    async def upsert_profile(
        self,
        db: AsyncSession,
        payload: ProfileUpsertRequest
    ) -> Profile:

        profile = await self.repository.get_profile(
            db
        )

        data = payload.model_dump()

        if profile is None:

            profile = (
                await self.repository.create_profile(
                    db,
                    data
                )
            )

        else:

            profile = (
                await self.repository.update_profile(
                    db,
                    profile,
                    data
                )
            )

        await db.commit()

        await db.refresh(
            profile
        )

        return profile