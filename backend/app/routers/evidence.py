from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.database import get_db
from app.auth.dependencies import get_current_user, require_trainer
from app.models.user import User
from app.services.evidence_service import EvidenceService

router = APIRouter()


@router.post("/upload/{session_id}")
def upload_evidence(
    session_id: uuid.UUID,
    criterion_id: uuid.UUID = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_trainer),
):
    try:
        content = file.file.read()
        evidence = EvidenceService.upload_evidence(
            db=db,
            session_id=session_id,
            criterion_id=criterion_id,
            file_content=content,
            original_filename=file.filename,
            uploaded_by=user.id,
        )
        return {
            "id": str(evidence.id),
            "system_filename": evidence.system_filename,
            "file_type": evidence.file_type,
            "file_size_bytes": evidence.file_size_bytes,
        }
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/session/{session_id}")
def list_evidence(session_id: uuid.UUID, criterion_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    files = EvidenceService.get_evidence_for_session(db, session_id, criterion_id)
    return [{
        "id": str(f.id),
        "original_filename": f.original_filename,
        "system_filename": f.system_filename,
        "file_type": f.file_type,
        "mime_type": f.mime_type,
        "file_size_bytes": f.file_size_bytes,
        "version": f.version,
        "created_at": f.created_at.isoformat(),
    } for f in files]


@router.get("/download/{evidence_id}")
def download_evidence(evidence_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    from app.models.evidence import EvidenceFile
    f = db.query(EvidenceFile).filter(EvidenceFile.id == evidence_id).first()
    if not f:
        raise HTTPException(404, "Evidence not found")
    url = EvidenceService.get_signed_url(f.storage_path)
    return {"download_url": url, "filename": f.system_filename}
