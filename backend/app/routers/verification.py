from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.auth.dependencies import get_current_user, require_verifier
from app.models.user import User
from app.services.verification_service import VerificationService

router = APIRouter()


class VerificationRequest(BaseModel):
    verifier_type: str
    decision: str
    comments: str = None
    rejection_reasons: str = None


@router.post("/sessions/{session_id}")
def verify_session(session_id: uuid.UUID, data: VerificationRequest, db: Session = Depends(get_db), user: User = Depends(require_verifier)):
    try:
        record = VerificationService.verify_assessment(
            db, session_id, user.id, data.verifier_type, data.decision, data.comments, data.rejection_reasons
        )
        return {"verification_id": str(record.id), "decision": record.decision}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/sessions/{session_id}/history")
def get_verification_history(session_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_verifier)):
    return VerificationService.get_verification_history(db, session_id)
