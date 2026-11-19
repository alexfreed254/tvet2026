from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black, white, HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from sqlalchemy.orm import Session
import uuid
import os
import tempfile
from app.models.session import AssessmentSession
from app.models.assessment import Assessment, AssessmentTask
from app.models.criterion import ChecklistCriterion, CriterionResult
from app.models.trainee import Trainee
from app.models.user import User
from app.models.institution import Institution
from app.services.filename_service import FilenameService


class PDFAssessmentGenerator:
    HEADER_BG = HexColor('#2C3E50')
    BORDER_COLOR = HexColor('#333333')
    LIGHT_BG = HexColor('#F5F5F5')

    def __init__(self, db: Session):
        self.db = db

    def generate_completed_assessment_pdf(self, session_id: uuid.UUID, output_dir=None) -> dict:
        s = self.db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
        if not s:
            raise ValueError("Session not found")
        a = self.db.query(Assessment).filter(Assessment.id == s.assessment_id).first()
        t = self.db.query(Trainee).filter(Trainee.id == s.trainee_id).first()
        assessor = self.db.query(User).filter(User.id == s.assessor_id).first()
        institution = self.db.query(Institution).filter(Institution.id == a.institution_id).first() if a.institution_id else None
        criteria = self.db.query(ChecklistCriterion).filter(ChecklistCriterion.assessment_id == a.id).order_by(ChecklistCriterion.display_order).all()
        results_map = {cr.criterion_id: cr for cr in self.db.query(CriterionResult).filter(CriterionResult.session_id == session_id).all()}
        tasks = self.db.query(AssessmentTask).filter(AssessmentTask.assessment_id == a.id).order_by(AssessmentTask.display_order).all()

        if output_dir is None:
            output_dir = tempfile.gettempdir()
        filename = FilenameService.generate_assessment_filename(
            t.admission_number, a.unit.name if a.unit else "Unknown", "COMPLETED_ASSESSMENT",
            a.assessment_number, a.academic_period.term if a.academic_period else 1,
            a.academic_period.year if a.academic_period else 2026,
            f"{assessor.first_name}_{assessor.last_name}" if assessor else "Unknown"
        )
        filepath = os.path.join(output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=15*mm, bottomMargin=15*mm, leftMargin=15*mm, rightMargin=15*mm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=14, alignment=TA_CENTER, fontName='Helvetica-Bold')
        subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER, fontName='Helvetica-Bold')
        normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=9)
        small_style = ParagraphStyle('SmallText', parent=styles['Normal'], fontSize=8)

        elements = []
        elements.append(Paragraph(institution.name if institution else "TVET INSTITUTION", title_style))
        elements.append(Paragraph(a.department.name.upper() if a.department else "DEPARTMENT", subtitle_style))
        elements.append(Spacer(1, 4*mm))
        elements.append(Paragraph(f"<b>ELECTRICAL INSTALLATION LEVEL {a.assessment_level or '4, 5 & 6'}</b>", subtitle_style))
        elements.append(Paragraph(f"Unit Code: <b>{a.unit.code if a.unit else 'N/A'}</b>", normal_style))
        elements.append(Paragraph(f"<b>{a.unit.name if a.unit else 'Unit Name'}</b>", subtitle_style))
        elements.append(Spacer(1, 3*mm))
        elements.append(Paragraph(f"<b>PRACTICAL ASSESSMENT {a.assessment_number}</b>", subtitle_style))
        elements.append(Spacer(1, 4*mm))
        elements.append(Paragraph("<b>OBSERVATION CHECKLIST</b>", subtitle_style))
        elements.append(Spacer(1, 3*mm))

        trainee_data = [
            ["Candidate's Name:", f"{t.first_name} {t.last_name}", "Date:", str(s.assessment_date or "N/A")],
            ["Adm. No.:", t.admission_number, "Venue:", s.assessment_venue or "N/A"],
            ["Assessor:", f"{assessor.first_name} {assessor.last_name}" if assessor else "N/A", "Period:", f"Term {a.academic_period.term}/{a.academic_period.year}" if a.academic_period else "N/A"],
        ]
        trainee_table = Table(trainee_data, colWidths=[45*mm, 65*mm, 40*mm, 40*mm])
        trainee_table.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 8), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('GRID', (0, 0), (-1, -1), 0.5, self.BORDER_COLOR), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
        elements.append(trainee_table)
        elements.append(Spacer(1, 4*mm))

        if a.instructions:
            elements.append(Paragraph("<b>Instructions:</b>", normal_style))
            elements.append(Paragraph(a.instructions, small_style))
            elements.append(Spacer(1, 3*mm))

        table_data = [[Paragraph("<b>Item to be Evaluated</b>", small_style), Paragraph("<b>Marks<br/>Available</b>", small_style), Paragraph("<b>Marks<br/>Obtained</b>", small_style), Paragraph("<b>Comments</b>", small_style)]]

        current_task = None
        for criterion in criteria:
            if criterion.task_id and criterion.task_id != (current_task.id if current_task else None):
                current_task = next((tk for tk in tasks if tk.id == criterion.task_id), None)
                if current_task:
                    table_data.append([Paragraph(f"<b>{current_task.task_number}. {current_task.task_title}</b>", small_style), "", "", ""])
            ct = criterion.criterion_text
            if criterion.sub_criterion_text:
                ct += f"<br/><i>({criterion.sub_criterion_text})</i>"
            r = results_map.get(criterion.id)
            mo = r.marks_obtained if r else 0
            comment = r.assessor_comment if r else ""
            if criterion.is_sub_total:
                table_data.append([Paragraph(f"<b>Sub-Total {criterion.criterion_number}</b>", small_style), Paragraph(f"<b>{criterion.max_marks}</b>", small_style), Paragraph(f"<b>{mo}</b>", small_style), ""])
            elif criterion.is_grand_total:
                table_data.append([Paragraph("<b>GRAND TOTAL</b>", small_style), Paragraph(f"<b>{criterion.max_marks}</b>", small_style), Paragraph(f"<b>{mo}</b>", small_style), ""])
            else:
                table_data.append([Paragraph(ct, small_style), str(criterion.max_marks), str(mo), Paragraph(comment, small_style) if comment else ""])

        pct = (s.total_marks_obtained / s.total_marks_available * 100) if s.total_marks_available > 0 else 0
        table_data.append([Paragraph(f"<b>Percentage: {pct:.1f}%</b>", small_style), "", "", ""])
        table_data.append([Paragraph("<b>ASSESSMENT OUTCOME</b>", small_style), "", "", ""])
        outcome = "☑ Competent    ☐ Not Yet Competent" if s.competency_outcome == 'competent' else "☐ Competent    ☑ Not Yet Competent"
        table_data.append([Paragraph(f"The candidate was found to be:  {outcome}", small_style), "", "", ""])
        table_data.append([Paragraph(f"<i>(Competent if ≥ {a.passing_percentage}%)</i>", small_style), "", "", ""])
        table_data.append([Paragraph("<b>Feedback from Candidate:</b>", small_style), "", "", ""])
        table_data.append(["", "", "", ""])
        table_data.append([Paragraph("<b>Feedback to Candidate:</b>", small_style), "", "", ""])
        table_data.append([Paragraph(s.feedback_to_candidate or "", small_style), "", "", ""])
        table_data.append([Paragraph("<b>Candidate Signature</b>", small_style), "", Paragraph("<b>Date</b>", small_style), ""])
        table_data.append(["_________________________", "", "_________________________", ""])
        table_data.append([Paragraph("<b>Assessor's Signature</b>", small_style), "", Paragraph("<b>Date</b>", small_style), ""])
        table_data.append(["_________________________", "", "_________________________", ""])

        col_widths = [90*mm, 30*mm, 30*mm, 40*mm]
        main_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table_style = [('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 8), ('GRID', (0, 0), (-1, -1), 0.5, self.BORDER_COLOR), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('BACKGROUND', (0, 0), (-1, 0), self.HEADER_BG), ('TEXTCOLOR', (0, 0), (-1, 0), white)]
        for i, row in enumerate(table_data):
            if i > 0:
                first = str(row[0]) if row[0] else ""
                if 'Sub-Total' in first or 'GRAND TOTAL' in first:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), self.LIGHT_BG))
                    table_style.append(('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold'))
                if 'ASSESSMENT OUTCOME' in first:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), HexColor('#E8F4FD')))
        main_table.setStyle(TableStyle(table_style))
        elements.append(main_table)
        doc.build(elements)
        return {"filepath": filepath, "filename": filename, "file_size_bytes": os.path.getsize(filepath), "session_id": str(session_id)}
