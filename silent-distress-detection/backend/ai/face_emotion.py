"""
Micro-expression and Physical Impact (Slap) Detector.
Uses Haar Cascades for face detection and tracks head velocity to detect sudden impacts.
"""
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

class FaceEmotionDetector:
    def __init__(self):
        self.prev_center = None
        self.prev_area = None
        self.IMPACT_THRESHOLD = 80.0 # Relaxed from 120 (was 50) to catch real slaps but avoid noise

    def detect(self, frame):
        """
        Detects face, micro-expression proxy, and physical impact (sudden head jerk).
        Returns dict with scores.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            self.prev_center = None # Reset if face lost
            return {"score": 0.0, "impact_detected": False, "details": "no_face"}

        # Track the largest face
        # Sort by area (w*h) descending
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        (x, y, w, h) = faces[0]
        
        current_center = np.array([x + w/2, y + h/2])
        current_area = w * h
        impact_detected = False
        velocity = 0.0

        if self.prev_center is not None and self.prev_area is not None:
            # Stability Check: Allow larger changes during fast motion, but filter massive glitches
            # Changed from 0.5 to 1.5 (150% change allowed)
            area_diff = abs(current_area - self.prev_area) / self.prev_area
            if area_diff < 1.5:
                velocity = np.linalg.norm(current_center - self.prev_center)
                if velocity > self.IMPACT_THRESHOLD:
                    impact_detected = True
                    print(f"[IMPACT DEBUG] Velocity: {velocity:.2f} > Threshold {self.IMPACT_THRESHOLD}")
            else:
                 # Reset if unstable
                 print(f"[DEBUG] Face size unstable (diff {area_diff:.2f}), skipping velocity check.")

        self.prev_center = current_center
        self.prev_area = current_area

        # Micro-expression Logic (Edge Energy Proxy)
        face_roi = gray[y : y + h, x : x + w]
        edges = cv2.Canny(face_roi, 50, 150)
        energy = np.sum(edges) / (w * h * 255)
        expression_score = float(np.tanh(energy * 5))

        return {
            "score": round(expression_score, 3), # Emotion/Stress score
            "impact_detected": impact_detected,
            "details": {
                "face_box": [int(x), int(y), int(w), int(h)], 
                "velocity": round(velocity, 1),
                "edge_energy": float(energy)
            }
        }

# Instantiate for simple usage if needed, though App should manage lifecycle
detector = FaceEmotionDetector()

def detect_microexpression(frame):
    # Backward compatibility wrapper
    return detector.detect(frame)
