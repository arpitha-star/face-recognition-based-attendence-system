"""Step 3 - Live attendance dashboard.   Run: streamlit run app.py"""
import glob
import os
from collections import Counter
from datetime import datetime

import pandas as pd
import streamlit as st

import config
from utils import load_db

st.set_page_config(page_title="Smart Attendance", page_icon="🧑‍💼", layout="wide")
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=3000, key="auto_refresh")
except ImportError:
    st.sidebar.warning("Install streamlit-autorefresh for live updates; "
                       "press R to refresh manually.")

st.title("🧑‍💼 Face Recognition Attendance")


def date_of(path):
    return datetime.strptime(os.path.basename(path)[11:21], "%d-%m-%Y")


files = sorted(glob.glob(str(config.ATTENDANCE_DIR / "Attendance_*.csv")),
               key=date_of, reverse=True)
_, reg_names = load_db()
registered = sorted(set(reg_names)) if reg_names else []

if not files:
    st.info("No attendance recorded yet. Run `python take_attendance.py`.")
    st.stop()

with st.sidebar:
    st.header("Filters")
    days = [os.path.basename(p)[11:21] for p in files]
    day = st.selectbox("Date", days)
    search = st.text_input("Search name")

df = pd.read_csv(config.ATTENDANCE_DIR / f"Attendance_{day}.csv")
shown = df[df["NAME"].str.contains(search, case=False, na=False)] if search else df

present = set(df["NAME"])
absent = [n for n in registered if n not in present]

c1, c2, c3 = st.columns(3)
c1.metric("Present", len(present))
c2.metric("Registered", len(registered))
c3.metric("Absent", len(absent))

left, right = st.columns([2, 1])
with left:
    st.subheader(f"Attendance - {day}")
    st.dataframe(shown, use_container_width=True, hide_index=True)
    st.download_button("⬇ Download CSV", df.to_csv(index=False),
                       file_name=f"Attendance_{day}.csv", mime="text/csv")
with right:
    st.subheader("Absent")
    if absent:
        st.write("\n".join(f"- {n}" for n in absent))
    else:
        st.success("Everyone registered is present." if registered else "No one registered yet.")

st.subheader("Attendance per day")
counts = {os.path.basename(p)[11:21]: len(pd.read_csv(p)) for p in reversed(files)}
st.bar_chart(pd.Series(counts, name="Present"))
