"""Step 2 - Take attendance with the webcam.
Keys:  o = mark attendance   a = toggle auto-mark   q = quit
Usage: python take_attendance.py [--auto] [--no-voice] [--camera 1]
"""
import argparse
import time
from datetime import datetime

import cv2
from sklearn.neighbors import KNeighborsClassifier

import config
from utils import (detect_faces, face_vector, load_cascade, load_db,
                   mark_attendance, open_camera, recognise, speak)

parser = argparse.ArgumentParser()
parser.add_argument("--camera", type=int, default=config.CAMERA_INDEX)
parser.add_argument("--auto", action="store_true",
                    help="mark automatically once a face is recognised steadily")
parser.add_argument("--no-voice", action="store_true")
args = parser.parse_args()

faces, names = load_db()
if faces is None:
    raise SystemExit("No registered faces found. Run add_faces.py first.")

knn = KNeighborsClassifier(n_neighbors=min(config.K_NEIGHBORS, len(names))).fit(faces, names)
cascade = load_cascade()
cap = open_camera(args.camera)

auto = args.auto
streak_name, streak = None, 0
notice, notice_until = "", 0.0


def notify(text, ok=True):
    global notice, notice_until
    notice, notice_until = text, time.time() + 2.5
    print(text)
    if ok and not args.no_voice:
        speak(text)


print("o = mark | a = toggle auto | q = quit")
while True:
    ok, frame = cap.read()
    if not ok:
        print("Camera stopped sending frames.")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected = None

    for box in detect_faces(cascade, gray):
        x, y, w, h = box
        label, dist = recognise(knn, names, face_vector(gray, box))
        known = label != "Unknown"
        color = (0, 200, 0) if known else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{label} ({dist:.1f})", (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        if known and (detected is None or w * h > detected[1]):
            detected = (label, w * h)

    current = detected[0] if detected else None
    streak = streak + 1 if current and current == streak_name else (1 if current else 0)
    streak_name = current

    key = cv2.waitKey(1) & 0xFF
    want_mark = (key == ord("o")) or (auto and current and streak == config.AUTO_MARK_FRAMES)
    if want_mark:
        if not current:
            notify("No known face to mark", ok=False)
        elif mark_attendance(current) == "marked":
            notify(f"Attendance taken for {current}")
        else:
            notify(f"{current} is already marked today", ok=False)
    elif key == ord("a"):
        auto = not auto
    elif key == ord("q"):
        break

    # status banner
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 34), (40, 40, 40), -1)
    cv2.putText(frame, f"{datetime.now():%d-%m-%Y %H:%M:%S}   Auto: {'ON' if auto else 'OFF'}"
                "   [o] mark  [a] auto  [q] quit", (10, 23),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    if time.time() < notice_until:
        cv2.putText(frame, notice, (10, frame.shape[0] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.imshow("Smart Attendance", frame)

cap.release()
cv2.destroyAllWindows()
