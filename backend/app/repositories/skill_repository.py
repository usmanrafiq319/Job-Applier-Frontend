import uuid

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import (
    ProfileSkill,
    Skill,
)


class SkillRepository:

    async def list_for_profile(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID
    ):

        result = await db.execute(

            select(
                ProfileSkill,
                Skill
            )
            .join(
                Skill,
                ProfileSkill.skill_id == Skill.id
            )
            .where(
                ProfileSkill.profile_id == profile_id
            )
            .order_by(
                Skill.name
            )
        )

        return result.all()


    async def find_by_name(
        self,
        db: AsyncSession,
        name: str
    ) -> Skill | None:

        result = await db.execute(

            select(Skill)
            .where(
                func.lower(Skill.name)
                == name.lower()
            )
            .limit(1)
        )

        return result.scalar_one_or_none()


    async def get_profile_skill(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        skill_id: uuid.UUID
    ):

        result = await db.execute(

            select(
                ProfileSkill,
                Skill
            )
            .join(
                Skill,
                ProfileSkill.skill_id == Skill.id
            )
            .where(
                ProfileSkill.profile_id == profile_id,
                ProfileSkill.skill_id == skill_id
            )
        )

        return result.first()


    async def create_skill(
        self,
        db: AsyncSession,
        name: str,
        category: str
    ) -> Skill:

        skill = Skill(
            name=name,
            category=category
        )

        db.add(skill)

        await db.flush()

        return skill


    async def attach_skill(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        skill_id: uuid.UUID,
        level: str
    ) -> ProfileSkill:

        link = ProfileSkill(
            profile_id=profile_id,
            skill_id=skill_id,
            level=level
        )

        db.add(link)

        await db.flush()

        return link


    async def delete_profile_skill(
        self,
        db: AsyncSession,
        link: ProfileSkill
    ) -> None:

        await db.delete(link)


    async def save_changes(
        self,
        db: AsyncSession
    ) -> None:

        await db.flush()