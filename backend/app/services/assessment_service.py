from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.models.assessment import Assessment, AssessmentTask
from app.models.criterion import ChecklistCriterion
from app.models.audit import AuditLog


class AssessmentService:

    @staticmethod
    def create_assessment(db: Session, data: dict, created_by: uuid.UUID) -> Assessment:
        assessment = Assessment(**data, created_by=created_by, status='draft', version=1)
        db.add(assessment)
        db.flush()
        db.add(AuditLog(user_id=created_by, action="assessment_created", entity_type="assessment", entity_id=assessment.id, new_values={"title": data.get("title")}))
        db.commit()
        db.refresh(assessment)
        return assessment

    @staticmethod
    def add_task(db: Session, assessment_id: uuid.UUID, task_data: dict) -> AssessmentTask:
        count = db.query(AssessmentTask).filter(AssessmentTask.assessment_id == assessment_id).count()
        task = AssessmentTask(assessment_id=assessment_id, task_number=count + 1, **task_data)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def add_checklist_criterion(db: Session, assessment_id: uuid.UUID, task_id, criterion_data: dict) -> ChecklistCriterion:
        count = db.query(ChecklistCriterion).filter(ChecklistCriterion.assessment_id == assessment_id).count()
        criterion = ChecklistCriterion(assessment_id=assessment_id, task_id=task_id, criterion_number=str(count + 1), **criterion_data)
        db.add(criterion)
        db.commit()
        db.refresh(criterion)
        return criterion

    @staticmethod
    def publish_assessment(db: Session, assessment_id: uuid.UUID, user_id: uuid.UUID) -> Assessment:
        a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not a:
            raise ValueError("Assessment not found")
        if a.status != 'draft':
            raise ValueError("Only draft assessments can be published")
        from sqlalchemy import func
        total = db.query(func.coalesce(func.sum(ChecklistCriterion.max_marks), 0)).filter(ChecklistCriterion.assessment_id == assessment_id).scalar()
        a.status = 'published'
        a.published_at = datetime.utcnow()
        a.total_marks = total
        db.commit()
        db.refresh(a)
        return a

    @staticmethod
    def withdraw_assessment(db: Session, assessment_id: uuid.UUID, user_id: uuid.UUID) -> Assessment:
        a = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not a:
            raise ValueError("Assessment not found")
        from app.models.session import AssessmentSession
        active = db.query(AssessmentSession).filter(AssessmentSession.assessment_id == assessment_id, AssessmentSession.status.in_(['in_progress', 'submitted'])).count()
        if active > 0:
            raise ValueError(f"Cannot withdraw: {active} active session(s)")
        a.status = 'withdrawn'
        db.commit()
        db.refresh(a)
        return a

    @staticmethod
    def create_new_version(db: Session, assessment_id: uuid.UUID, user_id: uuid.UUID) -> Assessment:
        original = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not original:
            raise ValueError("Assessment not found")
        original.status = 'archived'
        new_a = Assessment(
            institution_id=original.institution_id, department_id=original.department_id,
            course_id=original.course_id, class_id=original.class_id, unit_id=original.unit_id,
            academic_period_id=original.academic_period_id, title=original.title,
            assessment_number=original.assessment_number, assessment_type=original.assessment_type,
            assessment_level=original.assessment_level, instructions=original.instructions,
            duration_minutes=original.duration_minutes, passing_percentage=original.passing_percentage,
            required_tools=original.required_tools, required_equipment=original.required_equipment,
            required_materials=original.required_materials, safety_precautions=original.safety_precautions,
            ppe_requirements=original.ppe_requirements, marking_guidelines=original.marking_guidelines,
            status='draft', version=original.version + 1, created_by=user_id,
        )
        db.add(new_a)
        db.flush()
        for t in db.query(AssessmentTask).filter(AssessmentTask.assessment_id == assessment_id).all():
            db.add(AssessmentTask(assessment_id=new_a.id, task_number=t.task_number, task_title=t.task_title, task_description=t.task_description, max_marks=t.max_marks, task_type=t.task_type, display_order=t.display_order))
        for c in db.query(ChecklistCriterion).filter(ChecklistCriterion.assessment_id == assessment_id).all():
            db.add(ChecklistCriterion(assessment_id=new_a.id, criterion_number=c.criterion_number, criterion_text=c.criterion_text, sub_criterion_text=c.sub_criterion_text, max_marks=c.max_marks, scoring_type=c.scoring_type, award_max=c.award_max, display_order=c.display_order, is_sub_total=c.is_sub_total, is_grand_total=c.is_grand_total))
        db.commit()
        db.refresh(new_a)
        return new_a
