"""Step 1 - Register a person.
Usage: python add_faces.py            (asks for the name)
       python add_faces.py --name Ali --camera 0
"""
import argparse

import cv2

import config
from utils import (detect_faces, face_vector, load_cascade, load_db,
                   open_camera, save_db)

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="person's name")
parser.add_argument("--camera", type=int, default=config.CAMERA_INDEX)
args = parser.parse_args()

name = (args.name or input("Enter the person's name: ")).strip()
if not name:
    raise SystemExit("Name cannot be empty.")
if "," in name:
    raise SystemExit("Please do not use commas in the name.")

old_faces, old_names = load_db()
if old_names and name in old_names:
    if input(f"'{name}' already exists. Add more samples? (y/n): ").lower() != "y":
        raise SystemExit("Cancelled.")

cascade = load_cascade()
cap = open_camera(args.camera)
samples, frame_no = [], 0
print("Look at the camera and slowly turn your head a little. Press 'q' to cancel.")

while len(samples) < config.N_SAMPLES:
    ok, frame = cap.read()
    if not ok:
        print("Camera stopped sending frames.")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(cascade, gray)

    if len(faces) == 1:
        x, y, w, h = faces[0]
        frame_no += 1
        if frame_no % config.SAMPLE_EVERY == 0:
            samples.append(face_vector(gray, faces[0]))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)
        msg, color = f"Capturing {len(samples)}/{config.N_SAMPLES}", (0, 200, 0)
    elif len(faces) > 1:
        msg, color = "Only ONE person in the frame, please", (0, 0, 255)
    else:
        msg, color = "No face found - face the camera", (0, 165, 255)

    cv2.putText(frame, f"{name}: {msg}", (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.imshow("Register Face  (q = cancel)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

if len(samples) < config.N_SAMPLES:
    raise SystemExit(f"Only {len(samples)}/{config.N_SAMPLES} samples. Nothing saved.")

if old_names:
    faces_all = list(old_faces) + samples
    names_all = old_names + [name] * len(samples)
else:
    faces_all, names_all = samples, [name] * len(samples)

save_db(faces_all, names_all)
print(f"Saved '{name}'. People registered: {len(set(names_all))}")
