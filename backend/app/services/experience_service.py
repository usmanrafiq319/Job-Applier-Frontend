import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.experience_repository import (
    ExperienceRepository,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.schemas.experience import (
    ExperienceCreateRequest,
    ExperienceUpdateRequest,
)


class ProfileNotFoundError(Exception):
    pass


class ExperienceNotFoundError(Exception):
    pass


class InvalidExperienceDatesError(Exception):
    pass


class ExperienceService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.experience_repository = (
            ExperienceRepository()
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


    def _clean_technologies(
        self,
        technologies: list[str]
    ) -> list[str]:

        cleaned = []

        for technology in technologies:

            value = technology.strip()

            if value and value not in cleaned:
                cleaned.append(value)

        return cleaned


    def _validate_dates(
        self,
        start_date,
        end_date,
        currently_working: bool
    ) -> None:

        if currently_working:
            return

        if (
            start_date is not None
            and end_date is not None
            and end_date < start_date
        ):
            raise InvalidExperienceDatesError()


    async def get_experiences(
        self,
        db: AsyncSession
    ):

        profile = await self._get_profile(
            db
        )

        return (
            await self.experience_repository
            .list_for_profile(
                db,
                profile.id
            )
        )


    async def add_experience(
        self,
        db: AsyncSession,
        payload: ExperienceCreateRequest
    ):

        profile = await self._get_profile(
            db
        )

        data = payload.model_dump()

        data["technologies"] = (
            self._clean_technologies(
                data["technologies"]
            )
        )

        if data["currently_working"]:
            data["end_date"] = None

        self._validate_dates(
            data["start_date"],
            data["end_date"],
            data["currently_working"]
        )

        experience = (
            await self.experience_repository
            .create(
                db,
                profile.id,
                data
            )
        )

        await db.commit()

        await db.refresh(
            experience
        )

        return experience


    async def update_experience(
        self,
        db: AsyncSession,
        experience_id: uuid.UUID,
        payload: ExperienceUpdateRequest
    ):

        profile = await self._get_profile(
            db
        )

        experience = (
            await self.experience_repository
            .get_by_id(
                db,
                profile.id,
                experience_id
            )
        )

        if experience is None:
            raise ExperienceNotFoundError()

        data = payload.model_dump(
            exclude_unset=True
        )

        if (
            "technologies" in data
            and data["technologies"] is not None
        ):

            data["technologies"] = (
                self._clean_technologies(
                    data["technologies"]
                )
            )

        currently_working = data.get(
            "currently_working",
            experience.currently_working
        )

        start_date = data.get(
            "start_date",
            experience.start_date
        )

        end_date = data.get(
            "end_date",
            experience.end_date
        )

        if currently_working:

            data["end_date"] = None
            end_date = None

        self._validate_dates(
            start_date,
            end_date,
            currently_working
        )

        experience = (
            await self.experience_repository
            .update(
                db,
                experience,
                data
            )
        )

        await db.commit()

        await db.refresh(
            experience
        )

        return experience


    async def delete_experience(
        self,
        db: AsyncSession,
        experience_id: uuid.UUID
    ) -> None:

        profile = await self._get_profile(
            db
        )

        experience = (
            await self.experience_repository
            .get_by_id(
                db,
                profile.id,
                experience_id
            )
        )

        if experience is None:
            raise ExperienceNotFoundError()

        await self.experience_repository.delete(
            db,
            experience
        )

        await db.commit()