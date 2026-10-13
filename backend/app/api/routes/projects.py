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

from app.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)

from app.services.project_service import (
    ProfileNotFoundError,
    ProjectNotFoundError,
    ProjectService,
)


router = APIRouter(
    prefix="/profile/projects",
    tags=["Projects"]
)


service = ProjectService()


@router.get(
    "",
    response_model=list[ProjectResponse]
)
async def get_projects(
    db: AsyncSession = Depends(get_db)
):

    try:
        return await service.get_projects(
            db
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_project(
    payload: ProjectCreateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:
        return await service.add_project(
            db,
            payload
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse
)
async def update_project(
    project_id: uuid.UUID,
    payload: ProjectUpdateRequest,
    db: AsyncSession = Depends(get_db)
):

    try:
        return await service.update_project(
            db,
            project_id,
            payload
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except ProjectNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    try:

        await service.delete_project(
            db,
            project_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ProfileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    except ProjectNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )