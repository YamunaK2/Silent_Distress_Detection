"""
Lightweight posture detection scaffold. For robust skeleton-based posture use MediaPipe or OpenPose.
Here we use motion and bounding-box heuristics to detect collapsing/freezing behavior.
"""
import cv2
import numpy as np

background_subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=25, detectShadows=False)


def detect_posture(frame):
    """
    Analyzes frame for posture-based distress (e.g. freezing or collapsing).
    Renamed from analyze_posture to match app.py interface.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fg = background_subtractor.apply(gray)
    # compute the largest contour area as person proxy
    contours, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return {"score": 0.0, "details": "no_person_detected"}
    areas = [cv2.contourArea(c) for c in contours]
    largest = max(areas)
    # Heuristic: very small movement or very slumped bounding box aspect ratio -> possible distress
    motion_proxy = min(1.0, largest / (frame.shape[0] * frame.shape[1]))
    # Invert motion: small motion -> higher distress score
    score = float(1.0 - motion_proxy)
    return {"score": round(score, 3), "details": {"largest_area": int(largest), "motion_proxy": float(motion_proxy)}}
