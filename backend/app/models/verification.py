from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime


class VerificationRecord(Base):
    __tablename__ = "verification_records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("assessment_sessions.id", ondelete="CASCADE"))
    verifier_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verifier_type = Column(String(20), nullable=False)
    decision = Column(String(20), nullable=False)
    comments = Column(Text)
    rejection_reasons = Column(Text)
    verified_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
