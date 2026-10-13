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

from app.schemas.education import (
    EducationCreateRequest,
    EducationResponse,
    EducationUpdateRequest,
)

from app.services.education_service import (
    EducationNotFoundError,
    EducationService,
)


router = APIRouter(
    prefix="/profile/education",
    tags=["Education"]
)


service = EducationService()


@router.get(
    "",
    response_model=list[EducationResponse]
)
async def get_education(
    db: AsyncSession = Depends(get_db)
):

    try:
        return await service.get_education(
            db
        )

    except EducationNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )


@router.post(
    "",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_education(
    payload: EducationCreateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:
        return await service.add_education(
            db,
            payload
        )

    except EducationNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )


@router.patch(
    "/{education_id}",
    response_model=EducationResponse
)
async def update_education(
    education_id: uuid.UUID,
    payload: EducationUpdateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:
        return await service.update_education(
            db,
            education_id,
            payload
        )

    except EducationNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_education(
    education_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    try:

        await service.delete_education(
            db,
            education_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except EducationNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )