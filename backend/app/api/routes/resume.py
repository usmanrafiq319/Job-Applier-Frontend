from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)

from app.schemas.retrieval import (
    ResumeChunkSearchResult,
    ResumeSearchRequest,
)

from app.services.retrieval_service import (
    InvalidSearchQueryError,
    RetrievalProfileNotFoundError,
    RetrievalService,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.resume import (
    ResumeResponse,
)

from app.services.resume_service import (
    InvalidResumeError,
    ResumeNotFoundError,
    ResumeProcessingError,
    ResumeProfileNotFoundError,
    ResumeService,
)


router = APIRouter(
    prefix="/profile/resume",
    tags=["Resume"]
)


service = ResumeService()

retrieval_service = RetrievalService()

@router.post(
    "/search",
    response_model=list[
        ResumeChunkSearchResult
    ]
)
async def search_resume(
    payload: ResumeSearchRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await retrieval_service.search_resume(
            db,
            payload
        )


    except RetrievalProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


    except InvalidSearchQueryError:

        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )
    
@router.get(
    "",
    response_model=ResumeResponse
)
async def get_resume(
    db: AsyncSession = Depends(get_db)
):

    try:

        return await service.get_resume(
            db
        )

    except ResumeProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except ResumeNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    try:

        pdf_bytes = await file.read()


        return await service.upload_resume(
            db=db,
            original_file_name=(
                file.filename
                or "resume.pdf"
            ),
            mime_type=file.content_type,
            pdf_bytes=pdf_bytes
        )


    except ResumeProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


    except InvalidResumeError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


    except ResumeProcessingError:

        raise HTTPException(
            status_code=500,
            detail="Could not process resume"
        )


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_resume(
    db: AsyncSession = Depends(get_db)
):

    try:

        await service.delete_resume(
            db
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )


    except ResumeProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


    except ResumeNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )