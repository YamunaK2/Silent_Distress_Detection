import time
from config.firebase_config import db

def trigger_alert(fusion_data):
    """
    Triggers an alert to Firebase/Firestore.
    
    Args:
        fusion_data (dict): Result from fusion engine, e.g.:
                            {
                                'fusion_score': 0.95,
                                'is_distress': True,
                                'details': {...},
                                'timestamp': 1234567890
                            }
    """
    if not fusion_data.get("is_distress"):
        return

    alert_payload = {
        "timestamp": fusion_data.get("timestamp", time.time()),
        "location": "Camera_01_Main_Lobby", # Mock location
        "confidence_score": fusion_data.get("fusion_score", 0.0),
        "status": "pending", # pending, confirmed, dismissed
        "details": fusion_data.get("details", {}),
        "viewed": False
    }

    try:
        # Save to 'alerts' collection
        # db is either real firestore client or MockFirestore
        update_time, ref = db.collection("alerts").add(alert_payload)
        print(f"[ALERT SENT] ID: {ref.id} | Score: {alert_payload['confidence_score']}")
    except Exception as e:
        print(f"[ERROR] Failed to send alert: {e}")
