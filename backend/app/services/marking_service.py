from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import uuid
from app.models.session import AssessmentSession
from app.models.criterion import CriterionResult, ChecklistCriterion
from app.models.assessment import Assessment
from app.models.audit import AuditLog


class MarkingService:

    @staticmethod
    def create_assessment_session(db: Session, assessment_id: uuid.UUID, trainee_id: uuid.UUID, assessor_id: uuid.UUID, assessment_date, venue=None, session_number=1) -> AssessmentSession:
        existing = db.query(AssessmentSession).filter(AssessmentSession.assessment_id == assessment_id, AssessmentSession.trainee_id == trainee_id, AssessmentSession.session_number == session_number).first()
        if existing and existing.status in ['submitted', 'verified', 'approved']:
            raise ValueError(f"Session already {existing.status}")
        if existing:
            return existing
        a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not a:
            raise ValueError("Assessment not found")
        total = db.query(func.coalesce(func.sum(ChecklistCriterion.max_marks), 0)).filter(ChecklistCriterion.assessment_id == assessment_id).scalar()
        s = AssessmentSession(assessment_id=assessment_id, trainee_id=trainee_id, assessor_id=assessor_id, session_number=session_number, assessment_date=assessment_date, assessment_venue=venue, academic_period_id=a.academic_period_id, total_marks_available=total, status='in_progress')
        db.add(s)
        db.commit()
        db.refresh(s)
        return s

    @staticmethod
    def record_criterion_mark(db: Session, session_id: uuid.UUID, criterion_id: uuid.UUID, marks_obtained: float, assessor_comment=None, user_id=None) -> CriterionResult:
        c = db.query(ChecklistCriterion).filter(ChecklistCriterion.id == criterion_id).first()
        if not c:
            raise ValueError("Criterion not found")
        if marks_obtained < 0 or marks_obtained > c.max_marks:
            raise ValueError(f"Marks must be between 0 and {c.max_marks}")
        is_competent = marks_obtained >= c.binary_pass_mark if c.scoring_type == 'binary' else None
        r = db.query(CriterionResult).filter(CriterionResult.session_id == session_id, CriterionResult.criterion_id == criterion_id).first()
        if r:
            r.marks_obtained = marks_obtained
            r.assessor_comment = assessor_comment
            r.is_competent = is_competent
        else:
            r = CriterionResult(session_id=session_id, criterion_id=criterion_id, marks_available=c.max_marks, marks_obtained=marks_obtained, assessor_comment=assessor_comment, is_competent=is_competent)
            db.add(r)
        db.commit()
        db.refresh(r)
        if user_id:
            db.add(AuditLog(user_id=user_id, action="criterion_mark_recorded", entity_type="criterion_result", entity_id=r.id, new_values={"marks_obtained": marks_obtained}))
            db.commit()
        return r

    @staticmethod
    def calculate_session_totals(db: Session, session_id: uuid.UUID) -> dict:
        s = db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
        if not s:
            raise ValueError("Session not found")
        total_obtained = db.query(func.coalesce(func.sum(CriterionResult.marks_obtained), 0)).filter(CriterionResult.session_id == session_id).scalar()
        total_available = s.total_marks_available
        percentage = (total_obtained / total_available * 100) if total_available > 0 else 0
        a = db.query(Assessment).filter(Assessment.id == s.assessment_id).first()
        passing = a.passing_percentage if a else 50.0
        if percentage >= 80:
            competency = 'mastery'
        elif percentage >= 70:
            competency = 'proficient'
        elif percentage >= passing:
            competency = 'competent'
        else:
            competency = 'not_yet_competent'
        s.total_marks_obtained = round(total_obtained, 2)
        s.percentage_score = round(percentage, 2)
        s.competency_outcome = competency
        db.commit()
        db.refresh(s)
        return {"session_id": str(s.id), "total_obtained": total_obtained, "total_available": total_available, "percentage": round(percentage, 2), "competency": competency}

    @staticmethod
    def submit_session(db: Session, session_id: uuid.UUID, user_id: uuid.UUID, assessor_comments=None, feedback_to_candidate=None) -> AssessmentSession:
        s = db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
        if not s:
            raise ValueError("Session not found")
        if s.status != 'in_progress':
            raise ValueError(f"Cannot submit: status is {s.status}")
        MarkingService.calculate_session_totals(db, session_id)
        s.assessor_comments = assessor_comments
        s.feedback_to_candidate = feedback_to_candidate
        s.status = 'submitted'
        s.submitted_at = datetime.utcnow()
        db.commit()
        db.refresh(s)
        db.add(AuditLog(user_id=user_id, action="session_submitted", entity_type="assessment_session", entity_id=session_id, new_values={"total_marks_obtained": s.total_marks_obtained, "percentage": s.percentage_score, "competency": s.competency_outcome}))
        db.commit()
        return s

    @staticmethod
    def get_session_summary(db: Session, session_id: uuid.UUID) -> dict:
        s = db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
        if not s:
            raise ValueError("Session not found")
        results = db.query(CriterionResult).filter(CriterionResult.session_id == session_id).order_by(CriterionResult.created_at).all()
        criteria_details = []
        for cr in results:
            c = db.query(ChecklistCriterion).filter(ChecklistCriterion.id == cr.criterion_id).first()
            criteria_details.append({
                "criterion_id": str(cr.criterion_id),
                "criterion_text": c.criterion_text if c else "",
                "sub_criterion_text": c.sub_criterion_text if c else "",
                "max_marks": cr.marks_available,
                "marks_obtained": cr.marks_obtained,
                "is_competent": cr.is_competent,
                "comment": cr.assessor_comment,
                "scoring_type": c.scoring_type if c else "numerical",
            })
        return {
            "session_id": str(s.id),
            "assessment_id": str(s.assessment_id),
            "trainee_id": str(s.trainee_id),
            "assessor_id": str(s.assessor_id),
            "session_number": s.session_number,
            "assessment_date": s.assessment_date.isoformat() if s.assessment_date else None,
            "venue": s.assessment_venue,
            "total_marks_available": s.total_marks_available,
            "total_marks_obtained": s.total_marks_obtained,
            "percentage_score": s.percentage_score,
            "competency_outcome": s.competency_outcome,
            "assessor_comments": s.assessor_comments,
            "feedback_to_candidate": s.feedback_to_candidate,
            "status": s.status,
            "criteria_results": criteria_details,
        }
