import random

def detect_posture_distress(frame=None):
    """
    Simulates posture distress detection.
    Args:
        frame: Image frame (ignored in stub).
    Returns:
        dict: {'distress_score': float (0.0-1.0), 'details': str}
    """
    # Simulate specific postures
    postures = [
        ("Slumped", 0.7),
        ("Head in hands", 0.9),
        ("Upright", 0.1),
        ("Relaxed", 0.2)
    ]
    
    posture, base_score = random.choice(postures)
    
    # Add some noise
    final_score = min(1.0, base_score + random.uniform(-0.1, 0.1))
    
    return {
        "distress_score": max(0.0, final_score),
        "details": f"Posture: {posture}"
    }
