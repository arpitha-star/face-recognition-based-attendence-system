🧑‍💼 Smart Face Recognition Attendance System

An automated, real-time attendance management system built with Python, OpenCV, Scikit-Learn (KNN), and Streamlit. It captures face samples via webcam, trains a K-Nearest Neighbors classifier, logs daily attendance in CSV format with voice announcements, and provides an interactive web dashboard for monitoring.

📌 Features
⚡ Fast Face Registration: Captures 100 normalized facial frames with Haar Cascade detection.
🎯 Real-Time Face Recognition: Uses histogram-equalized feature vectors and KNN classification with customizable distance thresholds.
📝 Automated Attendance Logging: Prevents duplicate entries on the same day and logs timestamps to daily CSV files.
🔊 Voice Announcements: Audio feedback via pyttsx3 confirming when attendance has been marked.
📊 Interactive Streamlit Dashboard:
Live counts for Present, Registered, and Absent users.
Daily attendance trends and charts.
Search/filter by name and date.
One-click CSV export.
👥 User Management CLI: Easily list or delete registered profiles.
🚀 One-Click Launcher: Included run.bat provides a quick terminal menu for Windows users.
🏗️ System Architecture & Workflow
📁 Project Structure
text
face_attendance_v2/
│
├── Attendance/             # Generated daily attendance CSV records
├── data/                   # Saved face vectors and label pickles
│   ├── faces_data.pkl
│   └── names.pkl
├── add_faces.py            # Step 1: Script to capture & register a person's face
├── take_attendance.py      # Step 2: Live recognition & attendance logging
├── app.py                  # Step 3: Streamlit web dashboard
├── manage_users.py         # Utility to inspect and remove registered users
├── utils.py                # Core helpers: camera, cascade, vectors, audio, DB
├── config.py               # Tunable parameters (threshold, sample count, camera index)
├── requirements.txt        # Python package dependencies
├── run.bat                 # One-click Windows interactive launcher
└── README.md               # Project documentation
⚙️ Installation & Setup
Prerequisites
Python 3.9 - 3.13
A working webcam
1. Clone the Repository
bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance/face_attendance_v2
2. Create and Activate Virtual Environment
Windows:
powershell
python -m venv venv
venv\Scripts\activate
macOS / Linux:
bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt

Note for Linux users: If using voice feedback, install espeak:

bash
sudo apt install espeak
🚀 How to Use
Option A: Using the Launcher (Windows)

Simply double-click run.bat or run:

cmd
run.bat

Select an option from the menu (1 to Register, 2 to Take Attendance, 3 for Dashboard).

Option B: Running Scripts Manually
Step 1: Register New Faces

Sit in front of your camera and slowly move your head while samples are captured:

bash
python add_faces.py --name "Alice"

(Repeat for each user you wish to register.)

Step 2: Take Attendance
bash
python take_attendance.py
Keyboard Shortcuts:
o : Mark attendance for the recognized face
a : Toggle Auto-mark mode (marks automatically after 15 steady frames)
q : Quit camera window
Command-line flags:
bash
python take_attendance.py --auto       # Start directly with auto-marking enabled
python take_attendance.py --no-voice   # Disable voice announcements
python take_attendance.py --camera 1   # Use external webcam (index 1)
Step 3: Launch the Streamlit Dashboard
bash
streamlit run app.py

Open your browser at http://localhost:8501 to view live statistics, absent lists, and export CSV logs.

Step 4: Manage Registered Users
List registered users and sample counts:
bash
python manage_users.py list
Delete a registered user:
bash
python manage_users.py delete "Alice"
🛠️ Configuration & Tuning (config.py)

You can fine-tune detection and recognition in config.py:

Parameter	Default	Purpose
THRESHOLD	9.0	Max average KNN distance. Lower = stricter match; Higher = more lenient.
N_SAMPLES	100	Number of face crops collected during registration.
MIN_FACE_PX	80	Ignores detected faces smaller than 80×80 px (filters false positives).
AUTO_MARK_FRAMES	15	Consecutive matching frames required to auto-mark attendance.
CAMERA_INDEX	0	Default webcam index (0 for built-in, 1 for external USB camera).
🧰 Tech Stack
Language: Python
Computer Vision: OpenCV (cv2) with Haar Cascade Classifiers
Machine Learning: Scikit-Learn (KNeighborsClassifier)
Web App / Dashboard: Streamlit, Streamlit Autorefresh
Data Handling: NumPy, Pandas
Audio Feedback: pyttsx3
⚠️ Notes & Limitations
Light Sensitivity: Haar Cascades and pixel-distance metrics depend on uniform lighting. Register faces in the environment where attendance will be taken.
Security: Haar + KNN is designed for educational and demonstration purposes. It does not include 3D liveness detection (can be spoofed by a printed photograph).



 Run via Terminal (PowerShell)

Open PowerShell in face_attendance_v2:

Step 1 — Register your face:

powershell
cd "c:\Users\ARPITHA\OneDrive\Desktop\face recognition\face_attendance_v2"
.\venv\Scripts\python.exe add_faces.py --name "YourName"

Look into the camera and slightly turn your head until all 100 samples are captured.

Step 2 — Take attendance:

powershell
.\venv\Scripts\python.exe take_attendance.py
Controls: Press o to mark attendance, a to toggle auto-mark, and q to quit.
Records are saved to Attendance/.

Step 3 — View the Dashboard:

powershell
.\venv\Scripts\streamlit.exe run app.py

Opens the live attendance web dashboard in your browser (http://localhost:8501).
