from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip
from ..config import settings

def extract_audio(video_path: Path) -> Path:
    audio_filename = video_path.stem + ".wav"
    audio_path = settings.AUDIO_DIR / audio_filename

    try:
        with VideoFileClip(str(video_path)) as clip:
            if clip.audio is None:
                raise ValueError(f"The video '{video_path.name}' has no audio track.")
            clip.audio.write_audiofile(
                str(audio_path),
                fps=16000,
                nbytes=2,
                ffmpeg_params=["-ac", "1"],
                logger=None,
            )
    except ValueError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Audio extraction failed: {exc}") from exc

    return audio_path

def get_audio_duration(audio_path: Path) -> float:
    try:
        with AudioFileClip(str(audio_path)) as clip:
            return float(clip.duration)
    except Exception as exc:
        raise RuntimeError(f"Audio duration read failed: {exc}") from exc