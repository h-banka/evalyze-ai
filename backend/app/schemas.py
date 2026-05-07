from pydantic import BaseModel

class TranscriptResponse(BaseModel):
    filename: str
    transcript: str
    language: str
    audio_path: str
    video_path: str
    relevance: int
    clarity: int
    confidence: int
    face_detected: bool
    authenticity_score: int
    category: str

class ErrorResponse(BaseModel):
    error: str
    detail: str