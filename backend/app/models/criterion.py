from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime


class ChecklistCriterion(Base):
    __tablename__ = "checklist_criteria"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"))
    task_id = Column(UUID(as_uuid=True), ForeignKey("assessment_tasks.id", ondelete="CASCADE"))
    criterion_number = Column(String(20))
    criterion_text = Column(Text, nullable=False)
    sub_criterion_text = Column(Text)
    max_marks = Column(Integer, default=0)
    scoring_type = Column(String(20), default='numerical')
    award_max = Column(Integer)
    binary_pass_mark = Column(Integer, default=1)
    display_order = Column(Integer, default=0)
    is_sub_total = Column(Boolean, default=False)
    is_grand_total = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CriterionResult(Base):
    __tablename__ = "criterion_results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("assessment_sessions.id", ondelete="CASCADE"))
    criterion_id = Column(UUID(as_uuid=True), ForeignKey("checklist_criteria.id", ondelete="CASCADE"))
    marks_available = Column(Integer, nullable=False)
    marks_obtained = Column(Float, default=0)
    is_competent = Column(Boolean)
    assessor_comment = Column(Text)
    evidence_attached = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
