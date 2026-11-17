# Face Recognition Smart Attendance System
Python · OpenCV (Haar cascade) · KNN (scikit-learn) · Streamlit

## Setup (Python 3.9 - 3.12)
```
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # Mac / Linux
pip install -r requirements.txt
```
OpenCV must be 4.x (the pinned range handles this).
Linux voice support also needs: `sudo apt install espeak`. Voice is optional.

## Use
1. **Register**  `python add_faces.py`  - type a name, look at the camera and slowly turn your head until 100 samples are taken. Repeat for each person.
2. **Attendance**  `python take_attendance.py`
   - `o` mark attendance, `a` toggle auto-mark, `q` quit.
   - Options: `--auto`, `--no-voice`, `--camera 1`.
   - Saved to `Attendance/Attendance_DD-MM-YYYY.csv` (NAME, DATE, TIME); each person once per day.
3. **Dashboard**  `streamlit run app.py` - live table, present/absent counts, per-day chart, CSV download.
4. **Manage**  `python manage_users.py list` / `python manage_users.py delete "Name"`.

## Tuning (config.py)
The camera window shows a distance next to each name (lower = better match).
- Known person shows **Unknown** → raise `THRESHOLD` (e.g. 11).
- Strangers get recognised → lower `THRESHOLD` (e.g. 7).
- Good lighting and facing the camera matter most. Register in the same lighting you will use.

## Notes
- Data from the earlier version of this project is not compatible - re-register people.
- Haar + KNN is a simple learning project, not secure authentication (a photo can fool it).
