from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.gemini_embeddings import (
    GeminiEmbeddingClient,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.repositories.retrieval_repository import (
    RetrievalRepository,
)

from app.schemas.retrieval import (
    ResumeChunkSearchResult,
    ResumeSearchRequest,
)


class RetrievalProfileNotFoundError(
    Exception
):
    pass


class InvalidSearchQueryError(
    Exception
):
    pass


class RetrievalService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.retrieval_repository = (
            RetrievalRepository()
        )

        self.embedding_client = (
            GeminiEmbeddingClient()
        )


    async def search_resume(
        self,
        db: AsyncSession,
        payload: ResumeSearchRequest
    ) -> list[ResumeChunkSearchResult]:

        profile = (
            await self.profile_repository
            .get_profile(db)
        )

        if profile is None:

            raise RetrievalProfileNotFoundError()


        query = payload.query.strip()

        if not query:

            raise InvalidSearchQueryError()


        query_embedding = (
            await self.embedding_client
            .embed_query(
                query
            )
        )


        rows = (
            await self.retrieval_repository
            .search_resume_chunks(
                db=db,
                profile_id=profile.id,
                query_embedding=query_embedding,
                limit=payload.limit
            )
        )


        results = []

        for chunk, distance in rows:

            similarity = (
                1.0 - float(distance)
            )

            similarity = max(
                -1.0,
                min(
                    1.0,
                    similarity
                )
            )

            results.append(
                ResumeChunkSearchResult(
                    chunk_id=chunk.id,
                    resume_id=chunk.resume_id,
                    page_number=(
                        chunk.page_number
                    ),
                    content=chunk.content,
                    similarity=round(
                        similarity,
                        4
                    )
                )
            )


        return results