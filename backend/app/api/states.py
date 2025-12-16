from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from db.base import get_db
from db.models import CubeState
from schemas import FaceStatePayload, DetectionResponse

router = APIRouter(prefix="/api")

@router.post("/detections", response_model=DetectionResponse)
def post_detection(payload: FaceStatePayload, db: Session = Depends(get_db)):
    session_id = payload.session_id or str(uuid.uuid4())
    timestamp = payload.timestamp or datetime.utcnow()

    state = CubeState(
        session_id=session_id,
        timestamp=timestamp,
        face_state=payload.face_state
    )

    db.add(state)
    db.commit()
    db.refresh(state)

    return DetectionResponse(session_id=session_id, state_id=state.id)

@router.get("/state/{session_id}")
def get_state(session_id: str, db: Session = Depends(get_db)):
    states = (
        db.query(CubeState)
        .filter(CubeState.session_id == session_id)
        .order_by(CubeState.timestamp)
        .all()
    )

    if not states:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "current": states[-1].face_state,
        "history": [
            {"id": s.id, "timestamp": s.timestamp.isoformat()} for s in states
        ]
    }

@router.post("/state/{session_id}/undo")
def undo_last(session_id: str, db: Session = Depends(get_db)):
    last = (
        db.query(CubeState)
        .filter(CubeState.session_id == session_id)
        .order_by(CubeState.timestamp.desc())
        .first()
    )

    if not last:
        raise HTTPException(status_code=404, detail="No state to undo")
    
    db.delete(last)
    db.commit()

    return {"status": "last detection deleted successfully"}

@router.delete("/state/{session_id}")
def clear_session(session_id: str, db: Session = Depends(get_db)):
    rows = (
        db.query(CubeState)
        .filter(CubeState.session_id == session_id)
        .all()
    )

    for r in rows:
        db.delete(r)

    db.commit()
    return {"status":"all detections deleted!"}