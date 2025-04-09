# posture-monitor-app
posture monitor app using dual camera and a dashboard with notification system and data logging  (1>Webcam , 2> ESP 32 camera for posture from two angles) 
# PostureGuard 🧘 – Real-Time Posture Monitoring App

A Streamlit-based posture detection app using OpenCV, Mediapipe, and ESP32-CAM.

## Features

- Dual-camera posture analysis (Webcam + ESP32-CAM)
- Real-time alerts for slouching
- Historical trend visualization
- User authentication (basic)
- Local SQLite logging

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
