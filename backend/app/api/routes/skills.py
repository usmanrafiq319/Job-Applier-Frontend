import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.skill import (
    SkillCreateRequest,
    SkillResponse,
    SkillUpdateRequest,
)

from app.services.skill_service import (
    ProfileNotFoundError,
    SkillAlreadyAddedError,
    SkillNotFoundError,
    SkillService,
)


router = APIRouter(
    prefix="/profile/skills",
    tags=["Skills"]
)


service = SkillService()


@router.get(
    "",
    response_model=list[SkillResponse]
)
async def get_skills(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.get_skills(
            db
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_skill(
    payload: SkillCreateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.add_skill(
            db,
            payload
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except SkillAlreadyAddedError:

        raise HTTPException(
            status_code=409,
            detail="Skill already added to profile"
        )


@router.patch(
    "/{skill_id}",
    response_model=SkillResponse
)
async def update_skill(
    skill_id: uuid.UUID,
    payload: SkillUpdateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.update_skill(
            db,
            skill_id,
            payload
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except SkillNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_skill(
    skill_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    try:

        await service.remove_skill(
            db,
            skill_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except SkillNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )