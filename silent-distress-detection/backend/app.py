import threading
import time
import cv2
import numpy as np
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AI Modules
from ai.face_emotion import detect_microexpression
from ai.posture_detection import detect_posture
from ai.audio_stress import detect_audio_stress
from ai.multimodal_fusion import fuse_signals
from alerts.alert_manager import trigger_alert

app = FastAPI(title="Silent Distress Detection API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
SYSTEM_STATE = {
    "is_running": False,
    "last_alert": None,
    "active_alerts_count": 0,
    "camera_status": "Idle"
}

def monitoring_loop():
    """Background thread for processing video frames."""
    print("[SYSTEM] Monitoring Thread Started...")
    cap = cv2.VideoCapture(0) # Open default camera
    
    if not cap.isOpened():
        print("[ERROR] Could not open camera.")
        SYSTEM_STATE["camera_status"] = "Error"
        SYSTEM_STATE["is_running"] = False
        return

    SYSTEM_STATE["camera_status"] = "Active"

    while SYSTEM_STATE["is_running"]:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read frame.")
            break

        # 1. AI Analysis
        face_res = detect_microexpression(frame)
        posture_res = detect_posture(frame) # Assuming this takes frame as input
        audio_res = detect_audio_stress()   # Mock audio for now

        # 2. Fusion
        fusion_result = fuse_signals(face_res, posture_res, audio_res)

        # 3. Alert Logic
        if fusion_result['is_distress']:
            trigger_alert(fusion_result)
            SYSTEM_STATE["last_alert"] = {
                "time": time.time(),
                "score": fusion_result['fusion_score'],
                "details": fusion_result.get('details', {})
            }
            SYSTEM_STATE["active_alerts_count"] += 1
            print(f"[DISTRESS] Score: {fusion_result['fusion_score']:.2f} | {fusion_result['details']}")
        
        # JPEG Encoding for Stream
        try:
            # Optional: Draw bounding box if face detected
            if face_res.get('details') and isinstance(face_res['details'], dict) and 'face_box' in face_res['details']:
                 (fx, fy, fw, fh) = face_res['details']['face_box']
                 color = (0, 0, 255) if fusion_result['is_distress'] else (0, 255, 0)
                 cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), color, 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                with frame_lock:
                    global latest_frame_jpeg
                    latest_frame_jpeg = buffer.tobytes()
        except Exception as e:
            print(f"[ERROR] Encoding frame: {e}")

        # Free up CPU
        time.sleep(0.05)

    cap.release()
    SYSTEM_STATE["camera_status"] = "Idle"
    print("[SYSTEM] Monitoring Thread Stopped.")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Silent Distress Detection Backend is Ready"}

@app.post("/start")
def start_monitoring(background_tasks: BackgroundTasks):
    if SYSTEM_STATE["is_running"]:
        return {"status": "already_running"}
    
    SYSTEM_STATE["is_running"] = True
    background_tasks.add_task(monitoring_loop)
    return {"status": "started"}

@app.post("/stop")
def stop_monitoring():
    SYSTEM_STATE["is_running"] = False
    return {"status": "stopping_initiated"}

@app.get("/status")
def get_status():
    return SYSTEM_STATE

from config.firebase_config import db

@app.get("/alerts")
def get_alerts():
    """Fetch recent alerts. Useful if Frontend cannot connect to Firestore directly (Mock Mode)."""
    try:
        # Sort by timestamp desc
        docs = db.collection("alerts").stream()
        alerts_list = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            alerts_list.append(data)
        
        # Sort client-side mostly for mock; Firestore stream order depends on query
        alerts_list.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        return alerts_list
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []

# MJPEG Streaming Logic
from fastapi.responses import StreamingResponse
import io

# Global buffer for latest frame (JPEG)
# Initialize with a blank black frame to prevent broken image on client load
blank_image = np.zeros((480, 640, 3), np.uint8)
_, blank_buffer = cv2.imencode('.jpg', blank_image)
latest_frame_jpeg = blank_buffer.tobytes()

frame_lock = threading.Lock()

def gen_frames():
    """Video streaming generator function."""
    while True:
        with frame_lock:
            if latest_frame_jpeg:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame_jpeg + b'\r\n')
        time.sleep(0.05) # Cap at ~20 FPS for stream

@app.get("/video_feed")
def video_feed():
    """Returns MJPEG stream."""
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
