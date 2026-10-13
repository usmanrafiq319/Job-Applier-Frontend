from dataclasses import dataclass

import pymupdf


class PdfExtractionError(Exception):
    pass


@dataclass(frozen=True)
class ExtractedPage:

    page_number: int

    text: str


class PdfExtractionService:

    def extract_pages(
        self,
        pdf_bytes: bytes
    ) -> list[ExtractedPage]:

        try:

            with pymupdf.open(
                stream=pdf_bytes,
                filetype="pdf"
            ) as document:

                if document.needs_pass:

                    raise PdfExtractionError(
                        "Password-protected PDFs "
                        "are not supported"
                    )

                pages: list[ExtractedPage] = []

                for index, page in enumerate(
                    document
                ):

                    text = page.get_text(
                        "text",
                        sort=True
                    ).strip()

                    if not text:
                        continue

                    pages.append(
                        ExtractedPage(
                            page_number=index + 1,
                            text=text
                        )
                    )

        except PdfExtractionError:
            raise

        except Exception as exc:

            raise PdfExtractionError(
                "Invalid or unreadable PDF"
            ) from exc


        if not pages:

            raise PdfExtractionError(
                "No extractable text found in PDF"
            )

        return pages