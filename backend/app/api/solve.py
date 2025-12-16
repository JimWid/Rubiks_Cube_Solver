from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.base import get_db
from db.models import CubeState
from db.solver import solve_cube
from schemas import SolveResponse
import time, asyncio

router = APIRouter(prefix="/api")
CONFIDENCE_THRESHOLD = 0.7

@router.post("/solve/{session_id}", response_model=SolveResponse)
async def detect(session_id: str, db: Session = Depends(get_db)):
    last = (
        db.query(CubeState)
        .filter(CubeState.session_id == session_id)
        .order_by(CubeState.timestamp.desc())
        .first()
    )

    if not last:
        raise HTTPException(status_code=404, detail="Session not Found")
    
    try:
        solution = solve_cube(last.face_state)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Solver ErrorL {e}")
    
    return SolveResponse(solution=solution)