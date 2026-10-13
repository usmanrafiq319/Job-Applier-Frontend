import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
async def health_check():

    return {
        "status": "ok",
        "service": "AI Career Agent API"
    }


@router.get("/db")
async def database_health(
    db: AsyncSession = Depends(get_db)
):

    try:

        result = await db.execute(
            text("SELECT 1")
        )

        value = result.scalar_one()

        return {
            "status": "ok",
            "database": "connected",
            "test": value
        }

    except Exception as exc:

        logger.exception(
            "Database health check failed"
        )

        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        ) from exc