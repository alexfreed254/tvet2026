from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.course import Course
from app.auth.dependencies import get_current_user, require_hod
from app.models.user import User
import uuid

router = APIRouter()


class CourseCreate(BaseModel):
    department_id: uuid.UUID
    name: str
    code: str
    qualification_level: str = None


@router.post("/")
def create_course(data: CourseCreate, db: Session = Depends(get_db), user: User = Depends(require_hod)):
    course = Course(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return {"id": str(course.id), "name": course.name}


@router.get("/")
def list_courses(department_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Course).filter(Course.is_active == True)
    if department_id:
        q = q.filter(Course.department_id == department_id)
    return [{"id": str(c.id), "name": c.name, "code": c.code} for c in q.all()]
