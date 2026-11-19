from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

from app.database import get_db
from app.auth.dependencies import get_current_user, require_trainer
from app.models.user import User
from app.services.marking_service import MarkingService

router = APIRouter()


class MarkEntry(BaseModel):
    criterion_id: uuid.UUID
    marks_obtained: float = Field(..., ge=0)
    assessor_comment: str = None


class SessionSubmit(BaseModel):
    assessor_comments: str = None
    feedback_to_candidate: str = None


@router.post("/sessions/{session_id}/marks")
def record_marks(session_id: uuid.UUID, marks: List[MarkEntry], db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    results = []
    for m in marks:
        try:
            r = MarkingService.record_criterion_mark(db, session_id, m.criterion_id, m.marks_obtained, m.assessor_comment, user.id)
            results.append({"criterion_id": str(m.criterion_id), "status": "saved"})
        except ValueError as e:
            results.append({"criterion_id": str(m.criterion_id), "error": str(e)})
    totals = MarkingService.calculate_session_totals(db, session_id)
    return {"results": results, "totals": totals}


@router.get("/sessions/{session_id}/summary")
def get_session_summary(session_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    try:
        return MarkingService.get_session_summary(db, session_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/sessions/{session_id}/submit")
def submit_session(session_id: uuid.UUID, data: SessionSubmit, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    try:
        s = MarkingService.submit_session(db, session_id, user.id, data.assessor_comments, data.feedback_to_candidate)
        return {
            "message": "Submitted for verification",
            "session_id": str(s.id),
            "status": s.status,
            "total_marks_obtained": s.total_marks_obtained,
            "percentage": s.percentage_score,
            "competency": s.competency_outcome,
        }
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/trainee/{trainee_id}/sessions")
def get_trainee_sessions(trainee_id: uuid.UUID, assessment_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    from app.models.session import AssessmentSession
    q = db.query(AssessmentSession).filter(AssessmentSession.trainee_id == trainee_id)
    if assessment_id:
        q = q.filter(AssessmentSession.assessment_id == assessment_id)
    sessions = q.order_by(AssessmentSession.created_at.desc()).all()
    return [{
        "session_id": str(s.id),
        "assessment_id": str(s.assessment_id),
        "session_number": s.session_number,
        "status": s.status,
        "total_marks_obtained": s.total_marks_obtained,
        "percentage_score": s.percentage_score,
        "competency_outcome": s.competency_outcome,
        "assessment_date": s.assessment_date.isoformat() if s.assessment_date else None,
    } for s in sessions]
