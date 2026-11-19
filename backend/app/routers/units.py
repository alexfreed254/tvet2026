from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.unit import Unit
from app.auth.dependencies import get_current_user, require_hod
from app.models.user import User
import uuid

router = APIRouter()


class UnitCreate(BaseModel):
    course_id: uuid.UUID
    code: str
    name: str
    level: int = None


@router.post("/")
def create_unit(data: UnitCreate, db: Session = Depends(get_db), user: User = Depends(require_hod)):
    unit = Unit(**data.model_dump())
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return {"id": str(unit.id), "name": unit.name}


@router.get("/")
def list_units(course_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Unit).filter(Unit.is_active == True)
    if course_id:
        q = q.filter(Unit.course_id == course_id)
    return [{"id": str(u.id), "code": u.code, "name": u.name} for u in q.all()]
