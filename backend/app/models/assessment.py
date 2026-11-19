from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime


class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="CASCADE"))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"))
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id", ondelete="CASCADE"))
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"))
    academic_period_id = Column(UUID(as_uuid=True), ForeignKey("academic_periods.id"))
    title = Column(String(255), nullable=False)
    assessment_number = Column(String(50), nullable=False)
    assessment_type = Column(String(20), nullable=False)
    assessment_level = Column(String(20))
    instructions = Column(Text)
    duration_minutes = Column(Integer)
    total_marks = Column(Integer)
    passing_percentage = Column(Float, default=50.0)
    required_tools = Column(Text)
    required_equipment = Column(Text)
    required_materials = Column(Text)
    safety_precautions = Column(Text)
    ppe_requirements = Column(Text)
    marking_guidelines = Column(Text)
    reference_documents = Column(Text)
    status = Column(String(20), default='draft')
    version = Column(Integer, default=1)
    published_at = Column(DateTime)
    deadline = Column(DateTime)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AssessmentTask(Base):
    __tablename__ = "assessment_tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"))
    task_number = Column(Integer, nullable=False)
    task_title = Column(String(255), nullable=False)
    task_description = Column(Text)
    max_marks = Column(Integer, default=0)
    task_type = Column(String(30), default='practical')
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
