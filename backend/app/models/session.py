from sqlalchemy import Column, String, Integer, Float, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"))
    trainee_id = Column(UUID(as_uuid=True), ForeignKey("trainees.id", ondelete="CASCADE"))
    assessor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    session_number = Column(Integer, default=1)
    assessment_date = Column(Date)
    assessment_venue = Column(String(255))
    academic_period_id = Column(UUID(as_uuid=True), ForeignKey("academic_periods.id"))
    total_marks_available = Column(Integer, default=0)
    total_marks_obtained = Column(Float, default=0)
    percentage_score = Column(Float, default=0)
    competency_outcome = Column(String(30), default='pending')
    assessor_comments = Column(Text)
    feedback_to_candidate = Column(Text)
    status = Column(String(20), default='in_progress')
    submitted_at = Column(DateTime)
    verified_at = Column(DateTime)
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
