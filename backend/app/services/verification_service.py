from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.models.session import AssessmentSession
from app.models.verification import VerificationRecord
from app.models.user import User
from app.models.audit import AuditLog


class VerificationService:

    @staticmethod
    def verify_assessment(db: Session, session_id: uuid.UUID, verifier_id: uuid.UUID, verifier_type: str, decision: str, comments=None, rejection_reasons=None) -> VerificationRecord:
        s = db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
        if not s:
            raise ValueError("Session not found")
        if s.assessor_id == verifier_id:
            raise ValueError("Assessors cannot verify their own assessments")
        v = db.query(User).filter(User.id == verifier_id).first()
        if verifier_type == 'internal' and v.role not in ['super_admin', 'internal_verifier', 'hod']:
            raise ValueError("Not authorized as internal verifier")
        if verifier_type == 'external' and v.role != 'external_verifier':
            raise ValueError("Not authorized as external verifier")
        if s.status not in ['submitted', 'returned']:
            raise ValueError(f"Cannot verify: status is {s.status}")

        record = VerificationRecord(session_id=session_id, verifier_id=verifier_id, verifier_type=verifier_type, decision=decision, comments=comments, rejection_reasons=rejection_reasons, verified_at=datetime.utcnow())
        db.add(record)

        if decision == 'approved':
            s.status = 'approved'; s.approved_at = datetime.utcnow()
        elif decision == 'returned_for_correction':
            s.status = 'returned'
        elif decision == 'rejected':
            s.status = 'rejected'

        db.commit()
        db.refresh(record)
        db.add(AuditLog(user_id=verifier_id, action=f"assessment_{decision}", entity_type="verification", entity_id=record.id, new_values={"session_id": str(session_id), "decision": decision}))
        db.commit()
        return record

    @staticmethod
    def get_verification_history(db: Session, session_id: uuid.UUID):
        records = db.query(VerificationRecord).filter(VerificationRecord.session_id == session_id).order_by(VerificationRecord.verified_at.desc()).all()
        result = []
        for r in records:
            v = db.query(User).filter(User.id == r.verifier_id).first()
            result.append({
                "verification_id": str(r.id),
                "verifier_name": f"{v.first_name} {v.last_name}" if v else "Unknown",
                "verifier_type": r.verifier_type,
                "decision": r.decision,
                "comments": r.comments,
                "rejection_reasons": r.rejection_reasons,
                "verified_at": r.verified_at.isoformat() if r.verified_at else None,
            })
        return result
