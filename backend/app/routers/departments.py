from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.department import Department
from app.auth.dependencies import get_current_user, require_hod
from app.models.user import User
import uuid

router = APIRouter()


class DepartmentCreate(BaseModel):
    institution_id: uuid.UUID
    name: str
    code: str


@router.post("/")
def create_department(data: DepartmentCreate, db: Session = Depends(get_db), user: User = Depends(require_hod)):
    dept = Department(**data.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return {"id": str(dept.id), "name": dept.name}


@router.get("/")
def list_departments(institution_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Department).filter(Department.is_active == True)
    if institution_id:
        q = q.filter(Department.institution_id == institution_id)
    return [{"id": str(d.id), "name": d.name, "code": d.code} for d in q.all()]
