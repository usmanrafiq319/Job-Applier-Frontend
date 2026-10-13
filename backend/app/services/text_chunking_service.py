from dataclasses import dataclass

from app.core.constants import (
    RESUME_CHUNK_OVERLAP_WORDS,
    RESUME_CHUNK_WORDS,
)

from app.services.pdf_extraction_service import (
    ExtractedPage,
)


@dataclass(frozen=True)
class TextChunk:

    chunk_index: int

    page_number: int

    content: str

    word_count: int


class TextChunkingService:

    def chunk_pages(
        self,
        pages: list[ExtractedPage]
    ) -> list[TextChunk]:

        chunks: list[TextChunk] = []

        chunk_index = 0


        for page in pages:

            words = page.text.split()

            if not words:
                continue

            start = 0


            while start < len(words):

                end = min(
                    start + RESUME_CHUNK_WORDS,
                    len(words)
                )

                chunk_words = words[
                    start:end
                ]

                content = " ".join(
                    chunk_words
                ).strip()


                if content:

                    chunks.append(
                        TextChunk(
                            chunk_index=chunk_index,
                            page_number=(
                                page.page_number
                            ),
                            content=content,
                            word_count=len(
                                chunk_words
                            )
                        )
                    )

                    chunk_index += 1


                if end >= len(words):
                    break


                start = (
                    end
                    - RESUME_CHUNK_OVERLAP_WORDS
                )


        return chunks