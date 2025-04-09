import streamlit as st
import cv2
import pandas as pd
from database import get_posture_history

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.authenticated = True
        else:
            st.sidebar.error("Invalid credentials")

def show_dashboard(detector):
    st.title("PostureGuard 🧘")

    if 'run' not in st.session_state:
        st.session_state.run = False

    if st.sidebar.button("Start Monitoring"):
        st.session_state.run = True
    if st.sidebar.button("Stop Monitoring"):
        st.session_state.run = False

    col1, col2 = st.columns(2)
    front_placeholder = col1.empty()
    side_placeholder = col2.empty()
    stats_placeholder = st.sidebar.empty()

    cap = cv2.VideoCapture(0)
    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access webcam")
            break
        processed_frame, alert, angle = detector.detect_posture(frame)
        front_placeholder.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), channels="RGB")
        side_frame = detector.get_esp32_frame()
        if side_frame is not None:
            side_placeholder.image(cv2.cvtColor(side_frame, cv2.COLOR_BGR2RGB), channels="RGB")
        else:
            side_placeholder.warning("No side view available")

        stats_placeholder.markdown(f"""
        ### Posture Statistics
        - **Score**: {detector.daily_score()}/100
        - **Alerts Today**: {len([e for e in detector.posture_events if e['posture']=='bad'])}
        - **Torso Angle**: {angle:.1f}°
        - **Status**: {'⚠️ ' + alert if "Slouching" in alert else '✅ Good Posture'}
        """)

    cap.release()
    cv2.destroyAllWindows()

    if st.sidebar.button("Show Daily Trend"):
        df = get_posture_history()
        trend = df.groupby(['date', 'posture']).size().unstack(fill_value=0)
        st.line_chart(trend)