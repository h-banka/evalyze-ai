"""
app/services/file_service.py
Saves an uploaded file to the OS temp folder.
The file is automatically deleted after transcription — nothing stays on disk.
"""

import uuid
from pathlib import Path

from fastapi import UploadFile

from ..config import settings


async def save_upload(file: UploadFile) -> Path:
    """
    Stream an uploaded file to UPLOAD_DIR (a temp folder).

    A UUID prefix is prepended so two uploads with the same name
    never collide.

    Returns the path where the file was saved.
    """
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    save_path = settings.UPLOAD_DIR / unique_name

    with save_path.open("wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # 1 MB chunks
            buffer.write(chunk)

    return save_path


def delete_file(path: Path) -> None:
    """
    Silently delete a file. Ignores errors if the file is already gone.
    """
    try:
        path.unlink(missing_ok=True)
    except Exception:
        pass  # Never crash the response just because cleanup failed
