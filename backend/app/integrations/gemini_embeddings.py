import asyncio

from google import genai
from google.genai import types

from app.core.config import settings
from app.core.constants import EMBEDDING_DIMENSION


class EmbeddingConfigurationError(Exception):
    pass


class EmbeddingGenerationError(Exception):
    pass


class GeminiEmbeddingClient:

    def __init__(self):

        self.client = None


    def _get_client(self):

        if not settings.gemini_api_key:

            raise EmbeddingConfigurationError(
                "GEMINI_API_KEY is not configured"
            )

        if self.client is None:

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

        return self.client


    async def _generate_embedding(
        self,
        content: str
    ) -> list[float]:

        client = self._get_client()

        try:

            result = await asyncio.to_thread(
                client.models.embed_content,
                model=settings.embedding_model,
                contents=content,
                config=types.EmbedContentConfig(
                    output_dimensionality=(
                        EMBEDDING_DIMENSION
                    )
                )
            )

            if not result.embeddings:

                raise EmbeddingGenerationError(
                    "Embedding API returned "
                    "no embeddings"
                )

            values = result.embeddings[0].values

            if len(values) != EMBEDDING_DIMENSION:

                raise EmbeddingGenerationError(
                    "Embedding dimension "
                    "does not match database"
                )

            return list(values)


        except EmbeddingGenerationError:
            raise

        except Exception as exc:

            raise EmbeddingGenerationError(
                "Could not generate embedding"
            ) from exc


    async def embed_document(
        self,
        content: str,
        title: str | None = None
    ) -> list[float]:

        document_title = (
            title or "none"
        )

        prepared_content = (
            f"title: {document_title} | "
            f"text: {content}"
        )

        return await self._generate_embedding(
            prepared_content
        )


    async def embed_query(
        self,
        query: str
    ) -> list[float]:

        prepared_query = (
            f"task: search result | "
            f"query: {query}"
        )

        return await self._generate_embedding(
            prepared_query
        )