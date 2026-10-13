import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.repositories.skill_repository import (
    SkillRepository,
)

from app.schemas.skill import (
    SkillCreateRequest,
    SkillResponse,
    SkillUpdateRequest,
)


class ProfileNotFoundError(Exception):
    pass


class SkillAlreadyAddedError(Exception):
    pass


class SkillNotFoundError(Exception):
    pass


class SkillService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.skill_repository = (
            SkillRepository()
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


    async def get_skills(
        self,
        db: AsyncSession
    ) -> list[SkillResponse]:

        profile = await self._get_profile(db)

        rows = (
            await self.skill_repository
            .list_for_profile(
                db,
                profile.id
            )
        )

        return [
            SkillResponse(
                id=skill.id,
                name=skill.name,
                category=skill.category,
                level=link.level
            )
            for link, skill in rows
        ]


    async def add_skill(
        self,
        db: AsyncSession,
        payload: SkillCreateRequest
    ) -> SkillResponse:

        profile = await self._get_profile(db)

        name = payload.name.strip()

        skill = (
            await self.skill_repository
            .find_by_name(
                db,
                name
            )
        )

        if skill is None:

            skill = (
                await self.skill_repository
                .create_skill(
                    db,
                    name,
                    payload.category
                )
            )

        existing = (
            await self.skill_repository
            .get_profile_skill(
                db,
                profile.id,
                skill.id
            )
        )

        if existing is not None:
            raise SkillAlreadyAddedError()

        link = (
            await self.skill_repository
            .attach_skill(
                db,
                profile.id,
                skill.id,
                payload.level
            )
        )

        await db.commit()

        return SkillResponse(
            id=skill.id,
            name=skill.name,
            category=skill.category,
            level=link.level
        )


    async def update_skill(
        self,
        db: AsyncSession,
        skill_id: uuid.UUID,
        payload: SkillUpdateRequest
    ) -> SkillResponse:

        profile = await self._get_profile(db)

        row = (
            await self.skill_repository
            .get_profile_skill(
                db,
                profile.id,
                skill_id
            )
        )

        if row is None:
            raise SkillNotFoundError()

        link, skill = row

        data = payload.model_dump(
            exclude_unset=True
        )

        if (
            "category" in data
            and data["category"] is not None
        ):
            skill.category = data["category"]

        if (
            "level" in data
            and data["level"] is not None
        ):
            link.level = data["level"]

        await self.skill_repository.save_changes(
            db
        )

        await db.commit()

        return SkillResponse(
            id=skill.id,
            name=skill.name,
            category=skill.category,
            level=link.level
        )


    async def remove_skill(
        self,
        db: AsyncSession,
        skill_id: uuid.UUID
    ) -> None:

        profile = await self._get_profile(db)

        row = (
            await self.skill_repository
            .get_profile_skill(
                db,
                profile.id,
                skill_id
            )
        )

        if row is None:
            raise SkillNotFoundError()

        link, _ = row

        await self.skill_repository.delete_profile_skill(
            db,
            link
        )

        await db.commit()