"""Central settings. Edit values here instead of hunting through the code."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ATTENDANCE_DIR = BASE_DIR / "Attendance"

FACES_FILE = DATA_DIR / "faces_data.pkl"
NAMES_FILE = DATA_DIR / "names.pkl"

FACE_SIZE = (50, 50)      # every face is resized to this (grayscale)
N_SAMPLES = 100           # samples captured per person
SAMPLE_EVERY = 5          # keep every Nth frame with a face (more variety)
MIN_FACE_PX = 80          # ignore faces smaller than this (too far / false hits)

K_NEIGHBORS = 5
# Max average distance to accept a match. Lower = stricter. The live camera
# window shows the distance next to each name so you can tune this value.
THRESHOLD = 9.0

AUTO_MARK_FRAMES = 15     # frames a face must be recognised in a row (auto mode)
CAMERA_INDEX = 0
