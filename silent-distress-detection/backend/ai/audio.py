import random

def detect_audio_distress(audio_chunk=None):
    """
    Simulates audio distress detection.
    Args:
        audio_chunk: Audio data (ignored in stub).
    Returns:
        dict: {'distress_score': float (0.0-1.0), 'details': str}
    """
    # 10% chance of detecting a sob or scream
    if random.random() > 0.9:
        return {
            "distress_score": 0.95,
            "details": "High pitch / Sobbing detected"
        }
    return {
        "distress_score": 0.1,
        "details": "Ambient noise"
    }
