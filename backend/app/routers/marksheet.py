from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.auth.dependencies import get_current_user, require_hod, require_trainer
from app.models.user import User
from app.services.marksheet_service import MarksheetService

router = APIRouter()


@router.get("/generate")
def generate_marksheet(
    class_id: uuid.UUID = Query(...),
    unit_id: uuid.UUID = Query(...),
    academic_period_id: uuid.UUID = Query(...),
    output_format: str = Query("excel", pattern="^(excel|csv)$"),
    db: Session = Depends(get_db),
    user: User = Depends(require_hod),
):
    try:
        result = MarksheetService(db).generate_marksheet(class_id, unit_id, academic_period_id, output_format)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if output_format == "excel" else "text/csv"
        return FileResponse(path=result["filepath"], filename=result["filename"], media_type=media_type)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/preview")
def preview_marksheet(
    class_id: uuid.UUID = Query(...),
    unit_id: uuid.UUID = Query(...),
    academic_period_id: uuid.UUID = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_trainer),
):
    from app.models.trainee import Trainee
    from app.models.session import AssessmentSession
    from app.models.assessment import Assessment

    trainees = db.query(Trainee).filter(Trainee.class_id == class_id, Trainee.status == 'active').order_by(Trainee.admission_number).all()
    assessments = db.query(Assessment).filter(
        Assessment.class_id == class_id, Assessment.unit_id == unit_id,
        Assessment.academic_period_id == academic_period_id,
        Assessment.status.in_(['published', 'archived']),
    ).all()
    oral = [a for a in assessments if a.assessment_type == 'oral']
    practical = [a for a in assessments if a.assessment_type == 'practical']

    preview = []
    for t in trainees:
        oral_results = []
        for oa in oral:
            s = db.query(AssessmentSession).filter(AssessmentSession.assessment_id == oa.id, AssessmentSession.trainee_id == t.id, AssessmentSession.status.in_(['submitted', 'verified', 'approved'])).first()
            oral_results.append({"assessment": oa.assessment_number, "percentage": s.percentage_score if s else None})
        prac_results = []
        for pa in practical:
            s = db.query(AssessmentSession).filter(AssessmentSession.assessment_id == pa.id, AssessmentSession.trainee_id == t.id, AssessmentSession.status.in_(['submitted', 'verified', 'approved'])).first()
            prac_results.append({"assessment": pa.assessment_number, "percentage": s.percentage_score if s else None})

        oral_vals = [r['percentage'] for r in oral_results if r['percentage'] is not None]
        prac_vals = [r['percentage'] for r in prac_results if r['percentage'] is not None]
        oral_avg = sum(oral_vals) / len(oral_vals) if oral_vals else None
        prac_avg = sum(prac_vals) / len(prac_vals) if prac_vals else None
        overall = (oral_avg + prac_avg) / 2 if oral_avg is not None and prac_avg is not None else (oral_avg or prac_avg)

        preview.append({
            "admission_number": t.admission_number,
            "name": f"{t.first_name} {t.last_name}",
            "oral_results": oral_results,
            "practical_results": prac_results,
            "oral_average": round(oral_avg, 2) if oral_avg else None,
            "practical_average": round(prac_avg, 2) if prac_avg else None,
            "overall_average": round(overall, 2) if overall else None,
        })

    return {
        "oral_assessments": [a.assessment_number for a in oral],
        "practical_assessments": [a.assessment_number for a in practical],
        "trainees": preview,
    }
