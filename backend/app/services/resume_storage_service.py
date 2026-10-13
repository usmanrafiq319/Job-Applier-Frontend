import uuid

from pathlib import Path

from app.core.config import BASE_DIR


class ResumeStorageService:

    def __init__(self):

        self.storage_directory = (
            BASE_DIR
            / "storage"
            / "resumes"
        )

        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True
        )


    def save(
        self,
        pdf_bytes: bytes
    ) -> str:

        file_name = (
            f"{uuid.uuid4()}.pdf"
        )

        path = (
            self.storage_directory
            / file_name
        )

        path.write_bytes(
            pdf_bytes
        )


        relative_path = (
            path.relative_to(BASE_DIR)
        )

        return (
            str(relative_path)
            .replace("\\", "/")
        )


    def delete(
        self,
        storage_path: str | None
    ) -> None:

        if not storage_path:
            return


        path = (
            BASE_DIR
            / storage_path
        )


        if path.exists():

            path.unlink()