import asyncio
import logging

from datetime import (
    datetime,
    timezone,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    MAX_RESUME_SIZE_MB,
)

from app.integrations.gemini_embeddings import (
    GeminiEmbeddingClient,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.repositories.resume_repository import (
    ResumeRepository,
)

from app.services.pdf_extraction_service import (
    PdfExtractionError,
    PdfExtractionService,
)

from app.services.resume_storage_service import (
    ResumeStorageService,
)

from app.services.text_chunking_service import (
    TextChunkingService,
)


logger = logging.getLogger(__name__)


class ResumeProfileNotFoundError(Exception):
    pass


class ResumeNotFoundError(Exception):
    pass


class InvalidResumeError(Exception):
    pass


class ResumeProcessingError(Exception):
    pass


class ResumeService:

    def __init__(self):

        self.profile_repository = (
            ProfileRepository()
        )

        self.resume_repository = (
            ResumeRepository()
        )

        self.pdf_service = (
            PdfExtractionService()
        )

        self.chunking_service = (
            TextChunkingService()
        )

        self.storage_service = (
            ResumeStorageService()
        )

        self.embedding_client = (
            GeminiEmbeddingClient()
        )


    async def _get_profile(
        self,
        db: AsyncSession
    ):

        profile = (
            await self.profile_repository
            .get_profile(db)
        )

        if profile is None:

            raise ResumeProfileNotFoundError()

        return profile


    async def get_resume(
        self,
        db: AsyncSession
    ):

        profile = await self._get_profile(
            db
        )

        resume = (
            await self.resume_repository
            .get_active(
                db,
                profile.id
            )
        )

        if resume is None:

            raise ResumeNotFoundError()

        return resume


    async def upload_resume(
        self,
        db: AsyncSession,
        original_file_name: str,
        mime_type: str | None,
        pdf_bytes: bytes
    ):

        profile = await self._get_profile(
            db
        )


        if not original_file_name.lower().endswith(
            ".pdf"
        ):

            raise InvalidResumeError(
                "Only PDF resumes are supported"
            )


        if not pdf_bytes:

            raise InvalidResumeError(
                "Uploaded PDF is empty"
            )


        max_bytes = (
            MAX_RESUME_SIZE_MB
            * 1024
            * 1024
        )


        if len(pdf_bytes) > max_bytes:

            raise InvalidResumeError(
                f"Resume must be smaller than "
                f"{MAX_RESUME_SIZE_MB} MB"
            )


        try:

            pages = await asyncio.to_thread(
                self.pdf_service.extract_pages,
                pdf_bytes
            )

        except PdfExtractionError as exc:

            raise InvalidResumeError(
                str(exc)
            ) from exc


        chunks = (
            self.chunking_service
            .chunk_pages(pages)
        )


        if not chunks:

            raise InvalidResumeError(
                "No usable resume text found"
            )


        storage_path = (
            await asyncio.to_thread(
                self.storage_service.save,
                pdf_bytes
            )
        )


        try:

            await (
                self.resume_repository
                .deactivate_existing(
                    db,
                    profile.id
                )
            )


            resume = (
                await self.resume_repository
                .create_resume(
                    db,
                    profile.id,
                    {
                        "original_file_name":
                            original_file_name,

                        "storage_path":
                            storage_path,

                        "mime_type":
                            mime_type,

                        "file_size":
                            len(pdf_bytes),

                        "status":
                            "PROCESSING",

                        "is_active":
                            True,

                        "chunk_count":
                            0,
                    }
                )
            )


            for chunk in chunks:

                embedding = (
                    await self.embedding_client
                    .embed_document(
                        content=chunk.content,
                        title=original_file_name
                    )
                )


                await (
                    self.resume_repository
                    .create_chunk(
                        db,
                        resume.id,
                        {
                            "content":
                                chunk.content,

                            "chunk_index":
                                chunk.chunk_index,

                            "page_number":
                                chunk.page_number,

                            "chunk_type":
                                "TEXT",

                            "token_count":
                                None,

                            "extra_metadata": {
                                "word_count":
                                    chunk.word_count
                            },

                            "embedding":
                                embedding,
                        }
                    )
                )


            resume.chunk_count = len(
                chunks
            )

            resume.status = "READY"

            resume.processed_at = (
                datetime.now(
                    timezone.utc
                )
            )


            await db.commit()

            await db.refresh(
                resume
            )

            return resume


        except Exception as exc:

            await db.rollback()

            await asyncio.to_thread(
                self.storage_service.delete,
                storage_path
            )

            logger.exception(
                "Resume processing failed"
            )

            raise ResumeProcessingError(
                "Resume processing failed"
            ) from exc


    async def delete_resume(
        self,
        db: AsyncSession
    ) -> None:

        profile = await self._get_profile(
            db
        )

        resume = (
            await self.resume_repository
            .get_active(
                db,
                profile.id
            )
        )


        if resume is None:

            raise ResumeNotFoundError()


        storage_path = (
            resume.storage_path
        )


        await (
            self.resume_repository
            .delete_resume(
                db,
                resume
            )
        )


        await db.commit()


        await asyncio.to_thread(
            self.storage_service.delete,
            storage_path
        )