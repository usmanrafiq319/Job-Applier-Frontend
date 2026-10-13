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

from app.schemas.experience import (
    ExperienceCreateRequest,
    ExperienceResponse,
    ExperienceUpdateRequest,
)

from app.services.experience_service import (
    ExperienceNotFoundError,
    ExperienceService,
    InvalidExperienceDatesError,
    ProfileNotFoundError,
)


router = APIRouter(
    prefix="/profile/experiences",
    tags=["Experience"]
)


service = ExperienceService()


@router.get(
    "",
    response_model=list[ExperienceResponse]
)
async def get_experiences(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.get_experiences(
            db
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_experience(
    payload: ExperienceCreateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.add_experience(
            db,
            payload
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except InvalidExperienceDatesError:

        raise HTTPException(
            status_code=400,
            detail=(
                "End date cannot be before "
                "start date"
            )
        )


@router.patch(
    "/{experience_id}",
    response_model=ExperienceResponse
)
async def update_experience(
    experience_id: uuid.UUID,
    payload: ExperienceUpdateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.update_experience(
            db,
            experience_id,
            payload
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except ExperienceNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Experience not found"
        )

    except InvalidExperienceDatesError:

        raise HTTPException(
            status_code=400,
            detail=(
                "End date cannot be before "
                "start date"
            )
        )


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_experience(
    experience_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    try:

        await service.delete_experience(
            db,
            experience_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except ExperienceNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Experience not found"
        )