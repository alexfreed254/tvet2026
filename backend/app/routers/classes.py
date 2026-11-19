from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.class_model import Class
from app.auth.dependencies import get_current_user, require_hod
from app.models.user import User
import uuid

router = APIRouter()


class ClassCreate(BaseModel):
    course_id: uuid.UUID
    name: str
    intake_year: int = None
    cycle: int = None
    level: int = None


@router.post("/")
def create_class(data: ClassCreate, db: Session = Depends(get_db), user: User = Depends(require_hod)):
    cls = Class(**data.model_dump())
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return {"id": str(cls.id), "name": cls.name}


@router.get("/")
def list_classes(course_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Class).filter(Class.is_active == True)
    if course_id:
        q = q.filter(Class.course_id == course_id)
    return [{"id": str(c.id), "name": c.name, "level": c.level} for c in q.all()]
