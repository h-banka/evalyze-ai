from pathlib import Path
import cv2

def detect_face_in_video(video_path: Path) -> bool:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError("Could not open video for face detection.")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    try:
        frame_index = 0
        step = 15  # check every 15th frame for efficiency
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_index % step == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, None, fx=0.5, fy=0.5)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
                if len(faces) > 0:
                    return True

            frame_index += 1
    finally:
        cap.release()

    return False