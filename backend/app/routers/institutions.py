from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.institution import Institution
from app.auth.dependencies import get_current_user, require_admin
from app.models.user import User

router = APIRouter()


class InstitutionCreate(BaseModel):
    name: str
    code: str
    address: str = None
    phone: str = None
    email: str = None


@router.post("/", response_model=dict)
def create_institution(data: InstitutionCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    inst = Institution(**data.model_dump())
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return {"id": str(inst.id), "name": inst.name}


@router.get("/", response_model=List[dict])
def list_institutions(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return [{"id": str(i.id), "name": i.name, "code": i.code} for i in db.query(Institution).filter(Institution.is_active == True).all()]
