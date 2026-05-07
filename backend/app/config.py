"""
app/config.py
Central place for all configuration values.
Videos are written to the OS temp folder and deleted after transcription —
nothing is stored permanently on your device.
"""

import tempfile
from pathlib import Path


class Settings:
    # -----------------------------------------------------------------
    # General
    # -----------------------------------------------------------------
    APP_NAME: str = "AI Interview System"

    # -----------------------------------------------------------------
    # File storage — temp dir only, cleaned up after each request
    # -----------------------------------------------------------------
    UPLOAD_DIR: Path = Path(tempfile.gettempdir()) / "ai_interview" / "uploads"
    AUDIO_DIR: Path = Path(tempfile.gettempdir()) / "ai_interview" / "audio"

    # Maximum allowed upload size (bytes). 100 MB is generous for demos.
    MAX_FILE_SIZE_BYTES: int = 100 * 1024 * 1024  # 100 MB

    # Video MIME types we're willing to accept
    ALLOWED_VIDEO_TYPES: list[str] = [
        "video/mp4",
        "video/mpeg",
        "video/quicktime",  # .mov
        "video/x-msvideo",  # .avi
        "video/webm",
    ]

    # -----------------------------------------------------------------
    # Whisper
    # -----------------------------------------------------------------
    WHISPER_MODEL: str = "base"
    WHISPER_LANGUAGE: str | None = None  # None = auto-detect


# A single shared instance used everywhere
settings = Settings()

# Create temp directories on import
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
