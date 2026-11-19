from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
import uuid

from app.database import get_db
from app.auth.dependencies import get_current_user, require_trainer
from app.models.user import User
from app.models.session import AssessmentSession

router = APIRouter()


class SessionCreate(BaseModel):
    trainee_id: uuid.UUID
    assessment_date: date
    venue: str = None
    session_number: int = 1


@router.post("/{assessment_id}")
def start_session(assessment_id: uuid.UUID, data: SessionCreate, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    from app.services.marking_service import MarkingService
    try:
        s = MarkingService.create_assessment_session(db, assessment_id, data.trainee_id, user.id, data.assessment_date, data.venue, data.session_number)
        return {"session_id": str(s.id), "status": s.status}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/")
def list_sessions(assessment_id: uuid.UUID = None, trainee_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    q = db.query(AssessmentSession)
    if assessment_id:
        q = q.filter(AssessmentSession.assessment_id == assessment_id)
    if trainee_id:
        q = q.filter(AssessmentSession.trainee_id == trainee_id)
    if user.role not in ['super_admin', 'management', 'hod']:
        q = q.filter(AssessmentSession.assessor_id == user.id)
    return [{
        "id": str(s.id),
        "assessment_id": str(s.assessment_id),
        "trainee_id": str(s.trainee_id),
        "status": s.status,
        "total_marks_obtained": s.total_marks_obtained,
        "percentage_score": s.percentage_score,
        "competency_outcome": s.competency_outcome,
        "assessment_date": s.assessment_date.isoformat() if s.assessment_date else None,
    } for s in q.order_by(AssessmentSession.created_at.desc()).all()]
