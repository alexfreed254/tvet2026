from sqlalchemy.orm import Session
import uuid
import mimetypes
import os
from supabase import create_client
from app.config import settings
from app.models.evidence import EvidenceFile
from app.models.session import AssessmentSession
from app.models.trainee import Trainee
from app.models.assessment import Assessment
from app.models.user import User
from app.models.criterion import CriterionResult
from app.services.filename_service import FilenameService

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


class EvidenceService:
    ALLOWED_TYPES = {
        'photo': settings.ALLOWED_IMAGE_TYPES,
        'video': settings.ALLOWED_VIDEO_TYPES,
        'audio': settings.ALLOWED_AUDIO_TYPES,
        'document': settings.ALLOWED_DOC_TYPES,
        'scanned': settings.ALLOWED_IMAGE_TYPES + ['application/pdf'],
    }
    MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    @staticmethod
    def _detect_file_type(mime_type: str) -> str:
        for category, types in EvidenceService.ALLOWED_TYPES.items():
            if mime_type in types:
                return category
        return 'document'

    @classmethod
    def upload_evidence(cls, db: Session, session_id: uuid.UUID, criterion_id, file_content: bytes, original_filename: str, uploaded_by: uuid.UUID, item_reference=None) -> EvidenceFile:
        s = db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
        if not s:
            raise ValueError("Session not found")
        t = db.query(Trainee).filter(Trainee.id == s.trainee_id).first()
        a = db.query(Assessment).filter(Assessment.id == s.assessment_id).first()
        assessor = db.query(User).filter(User.id == uploaded_by).first()

        mime_type, _ = mimetypes.guess_type(original_filename)
        if not mime_type:
            mime_type = 'application/octet-stream'
        file_type = cls._detect_file_type(mime_type)

        if len(file_content) > cls.MAX_FILE_SIZE:
            raise ValueError(f"File exceeds {settings.MAX_FILE_SIZE_MB}MB")
        if mime_type not in cls.ALLOWED_TYPES.get(file_type, []):
            raise ValueError(f"File type {mime_type} not allowed")

        ext = original_filename.rsplit('.', 1)[-1] if '.' in original_filename else 'bin'
        existing = db.query(EvidenceFile).filter(EvidenceFile.session_id == session_id, EvidenceFile.criterion_id == criterion_id, EvidenceFile.is_current == True).all()
        file_index = len(existing) + 1

        system_filename = FilenameService.generate_evidence_filename(
            t.admission_number, a.unit.code if a.unit else "UNKNOWN", file_type.upper(),
            a.assessment_number, a.academic_period.term if a.academic_period else 1,
            a.academic_period.year if a.academic_period else 2026,
            f"{assessor.first_name}_{assessor.last_name}" if assessor else "Unknown",
            item_reference, file_index, ext
        )
        storage_path = f"evidence/{session_id}/{system_filename}"

        try:
            supabase.storage.from_(settings.SUPABASE_STORAGE_BUCKET).upload(path=storage_path, file=file_content, file_options={"content-type": mime_type})
        except Exception as e:
            raise ValueError(f"Upload failed: {str(e)}")

        for ef in existing:
            ef.is_current = False
            ef.version += 1

        evidence = EvidenceFile(
            session_id=session_id, criterion_id=criterion_id, uploaded_by=uploaded_by,
            original_filename=original_filename, system_filename=system_filename, storage_path=storage_path,
            file_type=file_type, mime_type=mime_type, file_size_bytes=len(file_content),
            admission_number=t.admission_number, unit_code=a.unit.code if a.unit else None,
            document_type=file_type.upper(), assessment_number=a.assessment_number,
            term=a.academic_period.term if a.academic_period else None,
            year=a.academic_period.year if a.academic_period else None,
            assessed_by_name=f"{assessor.first_name} {assessor.last_name}" if assessor else None,
            item_reference=item_reference, version=1, is_current=True,
        )
        db.add(evidence)

        if criterion_id:
            r = db.query(CriterionResult).filter(CriterionResult.session_id == session_id, CriterionResult.criterion_id == criterion_id).first()
            if r:
                r.evidence_attached = True

        db.commit()
        db.refresh(evidence)
        return evidence

    @classmethod
    def get_evidence_for_session(cls, db: Session, session_id: uuid.UUID, criterion_id=None):
        q = db.query(EvidenceFile).filter(EvidenceFile.session_id == session_id, EvidenceFile.is_current == True)
        if criterion_id:
            q = q.filter(EvidenceFile.criterion_id == criterion_id)
        return q.order_by(EvidenceFile.created_at).all()

    @classmethod
    def get_signed_url(cls, storage_path: str, expires_in: int = 3600) -> str:
        try:
            response = supabase.storage.from_(settings.SUPABASE_STORAGE_BUCKET).create_signed_url(path=storage_path, expires_in=expires_in)
            return response.get('signedURL', '')
        except Exception as e:
            raise ValueError(f"Failed to generate URL: {str(e)}")
