from pathlib import Path
from typing import TypedDict
import re
import whisper
from ..config import settings

print(f"[Whisper] Loading '{settings.WHISPER_MODEL}' model...")
_model = whisper.load_model(settings.WHISPER_MODEL)
print("[Whisper] Model ready.")

class TranscriptionResult(TypedDict):
    transcript: str
    language: str

def transcribe_audio(audio_path: Path) -> TranscriptionResult:
    try:
        result = _model.transcribe(
            str(audio_path),
            language=settings.WHISPER_LANGUAGE,
            fp16=False,
        )
    except Exception as exc:
        raise RuntimeError(f"Whisper transcription failed: {exc}") from exc

    return TranscriptionResult(
        transcript=result["text"].strip(),
        language=result.get("language", "unknown"),
    )

def evaluate_transcript(text: str) -> dict:
    word_count = len(text.split())
    if word_count < 20:
        confidence = 2
    elif word_count < 50:
        confidence = 5
    elif word_count < 100:
        confidence = 7
    else:
        confidence = 9

    keywords = [
        "experience", "project", "team", "problem", "solution",
        "result", "impact", "challenge", "goal", "responsibility",
        "achievement", "learning"
    ]
    hits = sum(1 for k in keywords if k in text.lower())
    if hits == 0:
        relevance = 2
    elif hits <= 2:
        relevance = 5
    elif hits <= 4:
        relevance = 7
    else:
        relevance = 9

    sentences = re.split(r"[.!?]+", text.strip())
    full_sentences = [s for s in sentences if len(s.strip().split()) >= 4]
    if len(full_sentences) == 0:
        clarity = 2
    elif len(full_sentences) <= 2:
        clarity = 5
    elif len(full_sentences) <= 5:
        clarity = 7
    else:
        clarity = 9

    return {
        "relevance": relevance,
        "clarity": clarity,
        "confidence": confidence,
    }

def calculate_authenticity(
    face_detected: bool,
    duration: float,
    transcript: str,
    relevance: int,
    clarity: int
) -> int:
    score = 0

    # Face check
    if face_detected:
        score += 40

    # Duration scoring
    if duration < 3:
        score += 5
    elif duration <= 5:
        score += 15
    else:
        score += 30

    # Word-based scoring
    word_list = transcript.split()
    total_words = len(word_list)

    if total_words > 20:
        score += 30
    else:
        score += 10

    # Repetition penalty
    if total_words > 0:
        unique_ratio = len(set(w.lower() for w in word_list)) / total_words
        if unique_ratio < 0.5:
            score -= 15

    # Short response penalty
    if total_words < 10:
        score -= 20

    # Filler word penalty
    fillers = ["um", "uh", "like"]
    filler_count = sum(1 for w in word_list if w.lower() in fillers)
    if filler_count > 3:
        score -= 10

    # Optional boost
    if total_words > 40:
        score += 5

    # NEW: Adjust based on quality (this is the key change)
    score -= (10 - relevance) * 2
    score -= (10 - clarity) * 2

    # Final cap
    return max(0, min(score, 95))

def get_audio_duration(video_path: str) -> float:
    """
    Returns duration of audio/video in seconds
    """
    from moviepy.editor import VideoFileClip

    clip = VideoFileClip(video_path)
    try:
        return float(clip.duration or 0.0)
    finally:
        clip.close()