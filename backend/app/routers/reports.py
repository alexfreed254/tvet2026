from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user, require_hod
from app.models.user import User

router = APIRouter()


@router.get("/summary")
def get_reports_summary(db: Session = Depends(get_db), user: User = Depends(require_hod)):
    from app.models.assessment import Assessment
    from app.models.session import AssessmentSession
    from app.models.trainee import Trainee

    total_assessments = db.query(Assessment).count()
    published = db.query(Assessment).filter(Assessment.status == 'published').count()
    total_sessions = db.query(AssessmentSession).count()
    completed = db.query(AssessmentSession).filter(AssessmentSession.status.in_(['submitted', 'verified', 'approved'])).count()
    total_trainees = db.query(Trainee).filter(Trainee.status == 'active').count()

    return {
        "total_assessments": total_assessments,
        "published_assessments": published,
        "total_sessions": total_sessions,
        "completed_sessions": completed,
        "active_trainees": total_trainees,
    }
