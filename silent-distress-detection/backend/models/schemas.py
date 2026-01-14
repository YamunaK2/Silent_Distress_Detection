from pydantic import BaseModel
from typing import Optional

class AlertCreate(BaseModel):
    camera_id: str
    location_id: Optional[str]
    confidence: float
    modalities: dict  # e.g. {"face":0.8, "posture":0.6, "audio":0.2}

class AlertUpdate(BaseModel):
    status: str  # pending | confirmed | dismissed
    reviewer: Optional[str]
    comment: Optional[str]
