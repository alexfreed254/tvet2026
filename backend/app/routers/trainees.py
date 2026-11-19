from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.trainee import Trainee
from app.auth.dependencies import get_current_user, require_trainer
from app.models.user import User
import uuid

router = APIRouter()


class TraineeCreate(BaseModel):
    class_id: uuid.UUID
    admission_number: str
    first_name: str
    last_name: str
    national_id: str = None
    phone: str = None
    email: str = None


@router.post("/")
def create_trainee(data: TraineeCreate, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    trainee = Trainee(**data.model_dump())
    db.add(trainee)
    db.commit()
    db.refresh(trainee)
    return {"id": str(trainee.id), "admission_number": trainee.admission_number}


@router.get("/")
def list_trainees(class_id: uuid.UUID = None, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    q = db.query(Trainee).filter(Trainee.status == 'active')
    if class_id:
        q = q.filter(Trainee.class_id == class_id)
    return [{
        "id": str(t.id),
        "admission_number": t.admission_number,
        "first_name": t.first_name,
        "last_name": t.last_name,
        "class_id": str(t.class_id),
    } for t in q.order_by(Trainee.admission_number).all()]


@router.get("/{trainee_id}")
def get_trainee(trainee_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    t = db.query(Trainee).filter(Trainee.id == trainee_id).first()
    if not t:
        raise HTTPException(404, "Trainee not found")
    return {
        "id": str(t.id),
        "admission_number": t.admission_number,
        "first_name": t.first_name,
        "last_name": t.last_name,
        "national_id": t.national_id,
        "phone": t.phone,
        "email": t.email,
        "status": t.status,
    }
