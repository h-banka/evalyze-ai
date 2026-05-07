from fastapi import APIRouter, File, HTTPException, UploadFile
from .config import settings
from .schemas import ErrorResponse, TranscriptResponse
from .services.audio_service import extract_audio, get_audio_duration
from .services.file_service import delete_file, save_upload
from .services.transcription_service import transcribe_audio, evaluate_transcript, calculate_authenticity
from .services.video_service import detect_face_in_video

router = APIRouter()

def classify_candidate(authenticity_score: int, relevance: int, clarity: int) -> str:
    if authenticity_score < 50:
        return "Fraud"
    elif relevance < 5:
        return "Low Confidence"
    elif clarity < 5:
        return "Needs Training"
    else:
        return "Job Ready"

@router.get("/")
async def root():
    return {"status": "ok", "message": "AI Interview System is running."}

@router.post("/analyze-video", response_model=TranscriptResponse)
async def analyze_video(file: UploadFile = File(...)):
    if file.content_type not in settings.ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail={
            "error": "invalid_file_type",
            "detail": f"'{file.content_type}' is not supported."
        })

    try:
        video_path = await save_upload(file)
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"error": "file_save_failed", "detail": str(exc)})

    audio_path = None
    try:
        try:
            audio_path = extract_audio(video_path)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail={"error": "no_audio_track", "detail": str(exc)})
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail={"error": "audio_extraction_failed", "detail": str(exc)})

        try:
            result = transcribe_audio(audio_path)
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail={"error": "transcription_failed", "detail": str(exc)})

        try:
            duration = get_audio_duration(audio_path)
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail={"error": "audio_duration_failed", "detail": str(exc)})

        try:
            face_detected = detect_face_in_video(video_path)
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail={"error": "face_detection_failed", "detail": str(exc)})

    finally:
        delete_file(video_path)
        if audio_path:
            delete_file(audio_path)

    scores = evaluate_transcript(result["transcript"])
    authenticity_score = calculate_authenticity(
    face_detected,
    duration,
    result["transcript"],
    scores["relevance"],
    scores["clarity"]
    )
    classification = classify_candidate(authenticity_score, scores["relevance"], scores["clarity"])

    return TranscriptResponse(
        filename=file.filename or "unknown",
        transcript=result["transcript"],
        language=result["language"],
        audio_path="deleted after transcription",
        video_path="deleted after transcription",
        relevance=scores["relevance"],
        clarity=scores["clarity"],
        confidence=scores["confidence"],
        face_detected=face_detected,
        authenticity_score=authenticity_score,
        category=classification,
    )