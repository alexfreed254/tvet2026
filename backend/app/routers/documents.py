from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.auth.dependencies import get_current_user, require_trainer
from app.models.user import User
from app.services.pdf_service import PDFAssessmentGenerator

router = APIRouter()


@router.get("/assessment-pdf/{session_id}")
def generate_assessment_pdf(session_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    try:
        result = PDFAssessmentGenerator(db).generate_completed_assessment_pdf(session_id)
        return FileResponse(path=result["filepath"], filename=result["filename"], media_type="application/pdf")
    except ValueError as e:
        raise HTTPException(404, str(e))
