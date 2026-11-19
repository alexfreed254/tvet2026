from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime


class EvidenceFile(Base):
    __tablename__ = "evidence_files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("assessment_sessions.id", ondelete="CASCADE"))
    criterion_id = Column(UUID(as_uuid=True), ForeignKey("checklist_criteria.id"))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    original_filename = Column(String(500), nullable=False)
    system_filename = Column(String(500), nullable=False)
    storage_path = Column(String, nullable=False)
    file_type = Column(String(20), nullable=False)
    mime_type = Column(String(100))
    file_size_bytes = Column(BigInteger)
    admission_number = Column(String(50))
    unit_code = Column(String(50))
    document_type = Column(String(50))
    assessment_number = Column(String(50))
    term = Column(Integer)
    year = Column(Integer)
    assessed_by_name = Column(String(200))
    item_reference = Column(String(50))
    version = Column(Integer, default=1)
    is_current = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
