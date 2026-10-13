import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.job import (
    JobCreateRequest,
    JobResponse,
    JobStatusUpdateRequest,
)
from app.schemas.job_analysis import (
    JobAnalysisResponse,
    JobAnalyzeRequest,
)

from app.services.job_analysis_service import (
    AnalyzeJobNotFoundError,
    AnalyzeProfileNotFoundError,
    JobAnalysisService,
)

from app.services.job_service import (
    JobNotFoundError,
    JobProfileNotFoundError,
    JobService,
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


service = JobService()

analysis_service = JobAnalysisService()

@router.get(
    "",
    response_model=list[JobResponse]
)
async def get_jobs(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.get_jobs(
            db
        )

    except JobProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_job(
    payload: JobCreateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.create_job(
            db,
            payload
        )

    except JobProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

@router.post(
    "/analyze",
    response_model=JobAnalysisResponse
)

async def analyze_job(
    payload: JobAnalyzeRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await analysis_service.analyze_job(
            db,
            payload
        )

    except AnalyzeProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except AnalyzeJobNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )    


@router.get(
    "/{job_id}",
    response_model=JobResponse
)
async def get_job(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.get_job(
            db,
            job_id
        )

    except JobProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except JobNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )


@router.patch(
    "/{job_id}/status",
    response_model=JobResponse
)
async def update_job_status(
    job_id: uuid.UUID,
    payload: JobStatusUpdateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.update_status(
            db,
            job_id,
            payload
        )

    except JobProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except JobNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )