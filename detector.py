import cv2
import mediapipe as mp
import numpy as np
import time
from database import log_posture_event

mp_pose = mp.solutions.pose

class PostureDetector:
    def __init__(self):
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.esp32_url = "http://192.168.1.100/640x480.jpg"
        self.posture_events = []

    def get_esp32_frame(self):
        try:
            import requests
            response = requests.get(self.esp32_url, timeout=2)
            if response.status_code == 200:
                img_array = np.frombuffer(response.content, dtype=np.uint8)
                return cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        except:
            return None

    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba, bc = a - b, c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(cosine_angle))

    def detect_posture(self, frame):
        alert = "Good Posture"
        angle = 180
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                h, w = frame.shape[:2]
                ls = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w, lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h]
                rs = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h]
                lh = [lm[mp_pose.PoseLandmark.LEFT_HIP].x * w, lm[mp_pose.PoseLandmark.LEFT_HIP].y * h]
                angle = self.calculate_angle(ls, lh, rs)
                status = "good" if angle >= 160 else "bad"
                if status == "bad":
                    alert = "Slouching Detected! Sit Straight!"
                self.posture_events.append({"time": time.time(), "posture": status})
                log_posture_event(status)
        except Exception as e:
            print(f"Error: {e}")
        return frame, alert, angle

    def daily_score(self):
        if not self.posture_events:
            return 100
        good_count = sum(1 for e in self.posture_events if e["posture"] == "good")
        return int((good_count / len(self.posture_events)) * 100)