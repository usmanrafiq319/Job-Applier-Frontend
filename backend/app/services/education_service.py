import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.education_repository import (
    EducationRepository,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.schemas.education import (
    EducationCreateRequest,
    EducationUpdateRequest,
)


class EducationNotFoundError(Exception):
    pass


class EducationService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.education_repository = (
            EducationRepository()
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
            raise EducationNotFoundError(
                "Profile not found"
            )

        return profile


    async def get_education(
        self,
        db: AsyncSession
    ):

        profile = await self._get_profile(
            db
        )

        return (
            await self.education_repository
            .list_for_profile(
                db,
                profile.id
            )
        )


    async def add_education(
        self,
        db: AsyncSession,
        payload: EducationCreateRequest
    ):

        profile = await self._get_profile(
            db
        )

        education = (
            await self.education_repository
            .create(
                db,
                profile.id,
                payload.model_dump()
            )
        )

        await db.commit()
        await db.refresh(education)

        return education


    async def update_education(
        self,
        db: AsyncSession,
        education_id: uuid.UUID,
        payload: EducationUpdateRequest
    ):

        profile = await self._get_profile(
            db
        )

        education = (
            await self.education_repository
            .get_by_id(
                db,
                profile.id,
                education_id
            )
        )

        if education is None:
            raise EducationNotFoundError(
                "Education not found"
            )

        data = payload.model_dump(
            exclude_unset=True
        )

        education = (
            await self.education_repository
            .update(
                db,
                education,
                data
            )
        )

        await db.commit()
        await db.refresh(education)

        return education


    async def delete_education(
        self,
        db: AsyncSession,
        education_id: uuid.UUID
    ) -> None:

        profile = await self._get_profile(
            db
        )

        education = (
            await self.education_repository
            .get_by_id(
                db,
                profile.id,
                education_id
            )
        )

        if education is None:
            raise EducationNotFoundError(
                "Education not found"
            )

        await self.education_repository.delete(
            db,
            education
        )

        await db.commit()