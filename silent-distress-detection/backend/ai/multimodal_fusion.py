"""
Simple fusion logic: combine modality scores with weighted average and compute final confidence.
Also includes persistence logic helper to decide if sustained distress occurred.
"""
from collections import deque
import time
import numpy as np

class FusionEngine:
    def __init__(self, history_len=5, distress_threshold=0.85):
        self.history = deque(maxlen=history_len)
        self.distress_threshold = distress_threshold
        # Weights for each modality (tunable)
        self.weights = {
            "face": 0.5,
            "posture": 0.3,
            "audio": 0.2
        }

    def fuse(self, face_res, posture_res, audio_res):
        """
        Combines signals from different AI modules into a single distress score.
        Uses temporal smoothing over the last `history_len` frames.
        
        Args:
            face_res (dict): {'score': float, 'details': ...}
            posture_res (dict): {'score': float, 'details': ...}
            audio_res (dict): {'score': float, 'details': ...}
            
        Returns:
            dict: {
                'is_distress': bool,
                'fusion_score': float,
                'details': dict
            }
        """
        score_face = face_res.get('score', 0.0)
        score_posture = posture_res.get('score', 0.0)
        score_audio = audio_res.get('score', 0.0)
        
        # Check for High-Priority Impact (Slap)
        if face_res.get('impact_detected'):
            # Override history and force alert
            self.history.clear()
            self.history.append(1.0)
            return {
                "is_distress": True,
                "fusion_score": 1.0, 
                "instant_score": 1.0,
                "details": {
                    "face": face_res,
                    "posture": posture_res,
                    "audio": audio_res,
                    "trigger": "IMPACT_DETECTED"
                }
            }

        # Immediate frame score
        current_score = (score_face * self.weights["face"]) + \
                        (score_posture * self.weights["posture"]) + \
                        (score_audio * self.weights["audio"])
        
        self.history.append(current_score)
        
        # Temporal smoothing: Average score over the window
        smoothed_score = np.mean(self.history)
        
        is_distress = smoothed_score > self.distress_threshold
        
        return {
            "is_distress": bool(is_distress),
            "fusion_score": round(float(smoothed_score), 3),
            "instant_score": round(float(current_score), 3),
            "details": {
                "face": face_res,
                "posture": posture_res,
                "audio": audio_res
            }
        }

# Singleton instance for simple import usage
engine = FusionEngine()

def fuse_signals(face_res, posture_res, audio_res):
    return engine.fuse(face_res, posture_res, audio_res)
