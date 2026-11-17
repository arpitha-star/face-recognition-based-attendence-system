"""Shared helpers used by every script."""
import csv
import pickle
import threading
from collections import Counter
from datetime import datetime

import cv2
import numpy as np

import config


# ---------- face detection / preprocessing ----------
def load_cascade():
    if not hasattr(cv2, "CascadeClassifier"):
        raise SystemExit("This OpenCV build has no CascadeClassifier (OpenCV 5.x). "
                         "Run: pip install \"opencv-python>=4.5,<5\"")
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if cascade.empty():
        raise SystemExit("Could not load the Haar cascade file from OpenCV.")
    return cascade


def detect_faces(cascade, gray):
    return cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=6,
        minSize=(config.MIN_FACE_PX, config.MIN_FACE_PX))


def face_vector(gray, box):
    """Crop -> resize -> histogram-equalise -> scale to 0..1 -> flat vector.
    Training and recognition both use this, so they always match."""
    x, y, w, h = box
    face = cv2.resize(gray[y:y + h, x:x + w], config.FACE_SIZE)
    face = cv2.equalizeHist(face)
    return (face.astype(np.float32) / 255.0).flatten()


def open_camera(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise SystemExit(
            f"Could not open camera {index}. Close other apps using it, "
            "or try --camera 1.")
    return cap


# ---------- face database ----------
def load_db():
    """Return (faces ndarray, names list) or (None, None) when empty."""
    if not (config.FACES_FILE.exists() and config.NAMES_FILE.exists()):
        return None, None
    with open(config.FACES_FILE, "rb") as f:
        faces = np.asarray(pickle.load(f), dtype=np.float32)
    with open(config.NAMES_FILE, "rb") as f:
        names = list(pickle.load(f))
    if len(names) == 0 or len(names) != len(faces) or faces.shape[1] != \
            config.FACE_SIZE[0] * config.FACE_SIZE[1]:
        return None, None  # empty or created by an older/incompatible version
    return faces, names


def save_db(faces, names):
    config.DATA_DIR.mkdir(exist_ok=True)
    with open(config.FACES_FILE, "wb") as f:
        pickle.dump(np.asarray(faces, dtype=np.float32), f)
    with open(config.NAMES_FILE, "wb") as f:
        pickle.dump(list(names), f)


def recognise(knn, names, vec):
    """Return (label, avg_distance). Label is 'Unknown' if too far away."""
    k = min(config.K_NEIGHBORS, len(names))
    dist, idx = knn.kneighbors(vec.reshape(1, -1), n_neighbors=k)
    votes = [names[i] for i in idx[0]]
    label, count = Counter(votes).most_common(1)[0]
    avg = float(np.mean([d for d, n in zip(dist[0], votes) if n == label]))
    if avg > config.THRESHOLD or count <= k // 2:
        return "Unknown", avg
    return label, avg


# ---------- attendance CSV ----------
def attendance_file(day=None):
    day = day or datetime.now()
    return config.ATTENDANCE_DIR / f"Attendance_{day:%d-%m-%Y}.csv"


def mark_attendance(name):
    """Return 'marked' or 'duplicate'."""
    config.ATTENDANCE_DIR.mkdir(exist_ok=True)
    now = datetime.now()
    path = attendance_file(now)
    if path.exists():
        with open(path, newline="") as f:
            rows = list(csv.reader(f))[1:]
        if any(r and r[0] == name for r in rows):
            return "duplicate"
    new_file = not path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["NAME", "DATE", "TIME"])
        writer.writerow([name, f"{now:%d-%m-%Y}", f"{now:%H:%M:%S}"])
    return "marked"


# ---------- optional voice ----------
def speak(text):
    """Speak in a background thread. Silently does nothing if pyttsx3 is missing."""
    def _run():
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
    threading.Thread(target=_run, daemon=True).start()
