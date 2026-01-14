"""Helper to send a test alert directly using firebase_admin credentials for demo or testing."""
from backend.config.firebase_config import db

def send_test():
    alert = {
        "camera_id": "demo-camera",
        "location_id": "demo-location",
        "confidence": 0.84,
        "modalities": {"face": 0.9, "posture": 0.7},
        "note": "test alert"
    }
    ref = db.collection('alerts').add(alert)
    print('Sent test alert, doc id:', ref[1].id)

if __name__ == '__main__':
    send_test()
