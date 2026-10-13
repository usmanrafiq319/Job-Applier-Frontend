from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.profile import (
    ProfileResponse,
    ProfileUpsertRequest,
)

from app.services.profile_service import (
    ProfileService,
)


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


service = ProfileService()


@router.get(
    "",
    response_model=ProfileResponse
)
async def get_profile(
    db: AsyncSession = Depends(get_db)
):

    profile = await service.get_profile(
        db
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@router.put(
    "",
    response_model=ProfileResponse
)
async def update_profile(
    payload: ProfileUpsertRequest,
    db: AsyncSession = Depends(get_db)
):

    return await service.upsert_profile(
        db,
        payload
    )