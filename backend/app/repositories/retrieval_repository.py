import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.models.resume_chunk import ResumeChunk


class RetrievalRepository:

    async def search_resume_chunks(
        self,
        db: AsyncSession,
        profile_id: uuid.UUID,
        query_embedding: list[float],
        limit: int
    ):

        distance = (
            ResumeChunk.embedding
            .cosine_distance(
                query_embedding
            )
        )

        statement = (
            select(
                ResumeChunk,
                distance.label(
                    "distance"
                )
            )
            .join(
                Resume,
                ResumeChunk.resume_id
                == Resume.id
            )
            .where(
                Resume.profile_id
                == profile_id,

                Resume.is_active.is_(True),

                Resume.status
                == "READY",

                ResumeChunk.embedding
                .is_not(None)
            )
            .order_by(
                distance
            )
            .limit(
                limit
            )
        )

        result = await db.execute(
            statement
        )

        return result.all()