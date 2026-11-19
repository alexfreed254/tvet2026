from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from app.database import get_db
from app.auth.dependencies import get_current_user, require_trainer, require_hod
from app.models.user import User
from app.models.assessment import Assessment, AssessmentTask
from app.models.criterion import ChecklistCriterion
from app.services.assessment_service import AssessmentService

router = APIRouter()


class AssessmentCreate(BaseModel):
    department_id: uuid.UUID
    course_id: uuid.UUID
    class_id: uuid.UUID
    unit_id: uuid.UUID
    academic_period_id: uuid.UUID
    title: str
    assessment_number: str
    assessment_type: str
    assessment_level: str = None
    instructions: str = None
    duration_minutes: int = None
    passing_percentage: float = 50.0
    required_tools: str = None
    required_equipment: str = None
    required_materials: str = None
    safety_precautions: str = None
    ppe_requirements: str = None
    marking_guidelines: str = None


class TaskCreate(BaseModel):
    task_title: str
    task_description: str = None
    max_marks: int = 0
    task_type: str = "practical"


class CriterionCreate(BaseModel):
    task_id: uuid.UUID = None
    criterion_text: str
    sub_criterion_text: str = None
    max_marks: int = 0
    scoring_type: str = "numerical"
    award_max: int = None
    is_sub_total: bool = False
    is_grand_total: bool = False


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_assessment(data: AssessmentCreate, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    try:
        assessment = AssessmentService.create_assessment(db, data.model_dump(), user.id)
        return {"id": str(assessment.id), "title": assessment.title, "status": assessment.status}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/")
def list_assessments(
    class_id: uuid.UUID = None,
    unit_id: uuid.UUID = None,
    assessment_type: str = None,
    status_filter: str = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Assessment)
    if class_id:
        q = q.filter(Assessment.class_id == class_id)
    if unit_id:
        q = q.filter(Assessment.unit_id == unit_id)
    if assessment_type:
        q = q.filter(Assessment.assessment_type == assessment_type)
    if status_filter:
        q = q.filter(Assessment.status == status_filter)
    if user.role not in ['super_admin', 'management']:
        q = q.filter(Assessment.department_id == user.department_id)
    return [{
        "id": str(a.id),
        "title": a.title,
        "assessment_number": a.assessment_number,
        "assessment_type": a.assessment_type,
        "status": a.status,
        "version": a.version,
        "total_marks": a.total_marks,
        "created_at": a.created_at.isoformat(),
    } for a in q.order_by(Assessment.created_at.desc()).all()]


@router.get("/{assessment_id}")
def get_assessment_detail(assessment_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(404, "Assessment not found")
    tasks = db.query(AssessmentTask).filter(AssessmentTask.assessment_id == assessment_id).order_by(AssessmentTask.display_order).all()
    criteria = db.query(ChecklistCriterion).filter(ChecklistCriterion.assessment_id == assessment_id).order_by(ChecklistCriterion.display_order).all()
    return {
        "assessment": {
            "id": str(a.id),
            "title": a.title,
            "assessment_number": a.assessment_number,
            "assessment_type": a.assessment_type,
            "status": a.status,
            "instructions": a.instructions,
            "passing_percentage": a.passing_percentage,
            "total_marks": a.total_marks,
        },
        "tasks": [{"id": str(t.id), "task_number": t.task_number, "task_title": t.task_title, "task_description": t.task_description, "max_marks": t.max_marks, "task_type": t.task_type} for t in tasks],
        "criteria": [{"id": str(c.id), "task_id": str(c.task_id) if c.task_id else None, "criterion_number": c.criterion_number, "criterion_text": c.criterion_text, "sub_criterion_text": c.sub_criterion_text, "max_marks": c.max_marks, "scoring_type": c.scoring_type, "is_sub_total": c.is_sub_total, "is_grand_total": c.is_grand_total} for c in criteria],
    }


@router.post("/{assessment_id}/tasks", status_code=status.HTTP_201_CREATED)
def add_task(assessment_id: uuid.UUID, data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    try:
        task = AssessmentService.add_task(db, assessment_id, data.model_dump())
        return {"id": str(task.id), "task_number": task.task_number}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/{assessment_id}/criteria", status_code=status.HTTP_201_CREATED)
def add_criterion(assessment_id: uuid.UUID, data: CriterionCreate, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    try:
        criterion = AssessmentService.add_checklist_criterion(db, assessment_id, data.task_id, data.model_dump(exclude={'task_id'}))
        return {"id": str(criterion.id), "criterion_number": criterion.criterion_number}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/{assessment_id}/publish")
def publish_assessment(assessment_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_hod)):
    try:
        a = AssessmentService.publish_assessment(db, assessment_id, user.id)
        return {"message": "Published", "id": str(a.id)}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/{assessment_id}/withdraw")
def withdraw_assessment(assessment_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_hod)):
    try:
        a = AssessmentService.withdraw_assessment(db, assessment_id, user.id)
        return {"message": "Withdrawn", "id": str(a.id)}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/{assessment_id}/new-version")
def create_new_version(assessment_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(require_trainer)):
    try:
        new_a = AssessmentService.create_new_version(db, assessment_id, user.id)
        return {"message": "New version created", "new_assessment_id": str(new_a.id)}
    except ValueError as e:
        raise HTTPException(400, str(e))
