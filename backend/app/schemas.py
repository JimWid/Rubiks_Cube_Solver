from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class FaceStatePayload(BaseModel):
    session_id: Optional[str] | None
    face_state: Dict[str, List[str]]
    timestamp: Optional[datetime] | None
    meta: Optional[dict] | None

class DetectionResponse(BaseModel):
    session_id: str
    state_id: str

class SolveResponse(BaseModel):
    move: str