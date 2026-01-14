"""
Edge agent that captures camera frames, runs the lightweight AI modules, and triggers alerts to Firebase via the alert_manager.
Run this on-device for privacy. It never stores frames or audio on disk.
"""
import os
import sys
# Ensure project root is on sys.path so imports that reference `backend.*` work whether
# this script is run from backend/ or project root.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
import cv2
from backend.ai.face_emotion import detect_microexpression
from backend.ai.posture_detection import analyze_posture
from backend.ai.multimodal_fusion import fuse, PersistenceBuffer
from backend.alerts.alert_manager import create_alert
from backend.utils.logger import logger

CAMERA_ID = "camera-1"
LOCATION_ID = "lobby-1"
CONFIDENCE_THRESHOLD = 0.75
PERSIST_WINDOW = PersistenceBuffer(window_seconds=6, sample_rate=2)


def run_edge_loop(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        logger.error("Camera not accessible")
        return

    sample_period = 0.5  # seconds
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.warning("Frame read failed")
                time.sleep(0.5)
                continue

            face_result = detect_microexpression(frame)
            posture_result = analyze_posture(frame)

            # Build modalities dict
            modalities = {
                "face": float(face_result.get("score", 0.0)),
                "posture": float(posture_result.get("score", 0.0)),
            }

            fused = fuse(modalities)
            confidence = fused["confidence"]
            timestamp = time.time()
            PERSIST_WINDOW.add(timestamp, confidence)

            logger.debug(f"Confidence={confidence} modalities={modalities}")

            if confidence >= CONFIDENCE_THRESHOLD and PERSIST_WINDOW.sustained_confidence(threshold=CONFIDENCE_THRESHOLD, min_fraction=0.6):
                # Trigger alert
                alert_doc = {
                    "camera_id": CAMERA_ID,
                    "location_id": LOCATION_ID,
                    "confidence": float(confidence),
                    "modalities": modalities,
                    "note": "auto-alert: sustained detection",
                }
                create_alert(alert_doc)
                logger.info("Alert created: " + str(alert_doc))
                # After an alert, pause to avoid duplicates
                time.sleep(5)

            time.sleep(sample_period)
    except KeyboardInterrupt:
        logger.info("Edge agent stopped by user")
    finally:
        cap.release()


if __name__ == '__main__':
    run_edge_loop()
