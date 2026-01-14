def fuse_signals(face_result, posture_result, audio_result):
    """
    Combines signals from Face, Posture, and Audio models.
    Returns a unified distress level.
    """
    f_score = face_result.get('distress_score', 0)
    p_score = posture_result.get('distress_score', 0)
    a_score = audio_result.get('distress_score', 0)
    
    # Weighted average
    # Audio given higher priority as screaming/sobbing is critical
    # Face and Posture are supportive
    weighted_score = (f_score * 0.3) + (p_score * 0.3) + (a_score * 0.4)
    
    details = []
    if f_score > 0.5: details.append(face_result['details'])
    if p_score > 0.5: details.append(posture_result['details'])
    if a_score > 0.5: details.append(audio_result['details'])
    
    return {
        "fusion_score": weighted_score,
        "is_distress": weighted_score > 0.7,
        "contributing_factors": details
    }
