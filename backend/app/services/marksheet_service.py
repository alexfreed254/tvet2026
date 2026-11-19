from sqlalchemy.orm import Session
import uuid
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
import csv
import io
import tempfile
import os
from app.models.session import AssessmentSession
from app.models.assessment import Assessment
from app.models.trainee import Trainee
from app.models.class_model import Class
from app.models.unit import Unit
from app.services.filename_service import FilenameService


class MarksheetService:
    def __init__(self, db: Session):
        self.db = db

    def generate_marksheet(self, class_id: uuid.UUID, unit_id: uuid.UUID, academic_period_id: uuid.UUID, output_format: str = 'excel') -> dict:
        class_obj = self.db.query(Class).filter(Class.id == class_id).first()
        unit = self.db.query(Unit).filter(Unit.id == unit_id).first()
        trainees = self.db.query(Trainee).filter(Trainee.class_id == class_id, Trainee.status == 'active').order_by(Trainee.admission_number).all()
        assessments = self.db.query(Assessment).filter(Assessment.class_id == class_id, Assessment.unit_id == unit_id, Assessment.academic_period_id == academic_period_id, Assessment.status.in_(['published', 'archived'])).order_by(Assessment.assessment_type, Assessment.assessment_number).all()
        oral = [a for a in assessments if a.assessment_type == 'oral']
        practical = [a for a in assessments if a.assessment_type == 'practical']

        data = []
        for t in trainees:
            row = {"admission_number": t.admission_number, "trainee_name": f"{t.first_name} {t.last_name}", "oral_marks": {}, "practical_marks": {}}
            oral_total, oral_count = 0, 0
            for oa in oral:
                s = self.db.query(AssessmentSession).filter(AssessmentSession.assessment_id == oa.id, AssessmentSession.trainee_id == t.id, AssessmentSession.status.in_(['submitted', 'verified', 'approved'])).first()
                if s:
                    row["oral_marks"][oa.assessment_number] = {"marks_obtained": s.total_marks_obtained, "marks_available": s.total_marks_available, "percentage": s.percentage_score, "competency": s.competency_outcome}
                    oral_total += s.percentage_score
                    oral_count += 1
                else:
                    row["oral_marks"][oa.assessment_number] = None
            row["oral_average"] = (oral_total / oral_count) if oral_count > 0 else None

            prac_total, prac_count = 0, 0
            for pa in practical:
                s = self.db.query(AssessmentSession).filter(AssessmentSession.assessment_id == pa.id, AssessmentSession.trainee_id == t.id, AssessmentSession.status.in_(['submitted', 'verified', 'approved'])).first()
                if s:
                    row["practical_marks"][pa.assessment_number] = {"marks_obtained": s.total_marks_obtained, "marks_available": s.total_marks_available, "percentage": s.percentage_score, "competency": s.competency_outcome}
                    prac_total += s.percentage_score
                    prac_count += 1
                else:
                    row["practical_marks"][pa.assessment_number] = None
            row["practical_average"] = (prac_total / prac_count) if prac_count > 0 else None

            if row["oral_average"] is not None and row["practical_average"] is not None:
                row["overall_average"] = (row["oral_average"] + row["practical_average"]) / 2
            else:
                row["overall_average"] = row["oral_average"] or row["practical_average"]
            data.append(row)

        if output_format == 'excel':
            return self._generate_excel(data, oral, practical, class_obj, unit)
        return self._generate_csv(data, oral, practical, class_obj, unit)

    def _generate_excel(self, data, oral, practical, class_obj, unit) -> dict:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Marksheet"
        header_font = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
        header_fill = PatternFill(start_color='2C3E50', end_color='2C3E50', fill_type='solid')
        avg_fill = PatternFill(start_color='27AE60', end_color='27AE60', fill_type='solid')
        avg_font = Font(name='Calibri', bold=True, size=10, color='FFFFFF')
        border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
        center = Alignment(horizontal='center', vertical='center', wrap_text=True)

        ws.merge_cells('A1:Z1')
        ws['A1'] = "TVET e-ASSESS — CONSOLIDATED MARKSHEET"
        ws['A1'].font = Font(name='Calibri', bold=True, size=14)
        ws['A1'].alignment = Alignment(horizontal='center')

        row = 5
        col = 1
        for h in ['ADM NO.', 'TRAINEE NAME']:
            c = ws.cell(row=row, column=col, value=h)
            c.font = header_font; c.fill = header_fill; c.alignment = center; c.border = border
            col += 1
        for oa in oral:
            c = ws.cell(row=row, column=col, value=f"ORAL {oa.assessment_number}")
            c.font = header_font; c.fill = PatternFill(start_color='E67E22', end_color='E67E22', fill_type='solid'); c.alignment = center; c.border = border
            col += 1
        c = ws.cell(row=row, column=col, value="ORAL AVG."); c.font = avg_font; c.fill = avg_fill; c.alignment = center; c.border = border; col += 1
        for pa in practical:
            c = ws.cell(row=row, column=col, value=f"PRAC. {pa.assessment_number}")
            c.font = header_font; c.fill = PatternFill(start_color='2980B9', end_color='2980B9', fill_type='solid'); c.alignment = center; c.border = border
            col += 1
        c = ws.cell(row=row, column=col, value="PRAC. AVG."); c.font = avg_font; c.fill = avg_fill; c.alignment = center; c.border = border; col += 1
        c = ws.cell(row=row, column=col, value="OVERALL AVG."); c.font = avg_font; c.fill = PatternFill(start_color='8E44AD', end_color='8E44AD', fill_type='solid'); c.alignment = center; c.border = border; col += 1
        c = ws.cell(row=row, column=col, value="COMPETENCY"); c.font = header_font; c.fill = header_fill; c.alignment = center; c.border = border

        for i, td in enumerate(data):
            row = 6 + i; col = 1
            for val in [td['admission_number'], td['trainee_name']]:
                c = ws.cell(row=row, column=col, value=val); c.font = Font(name='Calibri', size=10); c.alignment = center if col == 1 else Alignment(horizontal='left'); c.border = border; col += 1
            for oa in oral:
                r = td['oral_marks'].get(oa.assessment_number)
                c = ws.cell(row=row, column=col, value=r['percentage'] if r else "-"); c.font = Font(name='Calibri', size=10); c.alignment = center; c.border = border; col += 1
            c = ws.cell(row=row, column=col, value=td['oral_average'] if td['oral_average'] is not None else "-"); c.font = Font(name='Calibri', bold=True, size=10); c.alignment = center; c.border = border; col += 1
            for pa in practical:
                r = td['practical_marks'].get(pa.assessment_number)
                c = ws.cell(row=row, column=col, value=r['percentage'] if r else "-"); c.font = Font(name='Calibri', size=10); c.alignment = center; c.border = border; col += 1
            c = ws.cell(row=row, column=col, value=td['practical_average'] if td['practical_average'] is not None else "-"); c.font = Font(name='Calibri', bold=True, size=10); c.alignment = center; c.border = border; col += 1
            c = ws.cell(row=row, column=col, value=td['overall_average'] if td['overall_average'] is not None else "-"); c.font = Font(name='Calibri', bold=True, size=10); c.alignment = center; c.border = border; col += 1
            overall = td['overall_average']
            comp = "Competent" if overall is not None and overall >= 50 else ("Not Yet Competent" if overall is not None else "Pending")
            c = ws.cell(row=row, column=col, value=comp); c.font = Font(name='Calibri', bold=True, size=10); c.alignment = center; c.border = border
            if comp == "Competent":
                c.fill = PatternFill(start_color='D5F5E3', end_color='D5F5E3', fill_type='solid')
            elif comp == "Not Yet Competent":
                c.fill = PatternFill(start_color='FADBD8', end_color='FADBD8', fill_type='solid')

        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 30
        for cl in [get_column_letter(i) for i in range(3, col + 1)]:
            ws.column_dimensions[cl].width = 14

        output_dir = tempfile.gettempdir()
        filename = FilenameService.generate_marksheet_filename(unit.code if unit else "UNKNOWN", class_obj.name if class_obj else "UNKNOWN", "TERM1-2026")
        filepath = os.path.join(output_dir, filename)
        wb.save(filepath)
        return {"filepath": filepath, "filename": filename, "file_size_bytes": os.path.getsize(filepath), "trainee_count": len(data)}

    def _generate_csv(self, data, oral, practical, class_obj, unit) -> dict:
        output = io.StringIO()
        writer = csv.writer(output)
        header = ['ADM NO.', 'TRAINEE NAME']
        for oa in oral: header.append(f'ORAL {oa.assessment_number}')
        header.append('ORAL AVG.')
        for pa in practical: header.append(f'PRAC. {pa.assessment_number}')
        header.append('PRAC. AVG.'); header.append('OVERALL AVG.'); header.append('COMPETENCY')
        writer.writerow(header)
        for td in data:
            row = [td['admission_number'], td['trainee_name']]
            for oa in oral:
                r = td['oral_marks'].get(oa.assessment_number)
                row.append(f"{r['percentage']:.2f}" if r else "-")
            row.append(f"{td['oral_average']:.2f}" if td['oral_average'] is not None else "-")
            for pa in practical:
                r = td['practical_marks'].get(pa.assessment_number)
                row.append(f"{r['percentage']:.2f}" if r else "-")
            row.append(f"{td['practical_average']:.2f}" if td['practical_average'] is not None else "-")
            row.append(f"{td['overall_average']:.2f}" if td['overall_average'] is not None else "-")
            overall = td['overall_average']
            comp = "Competent" if overall is not None and overall >= 50 else ("Not Yet Competent" if overall is not None else "Pending")
            row.append(comp)
            writer.writerow(row)
        output_dir = tempfile.gettempdir()
        filename = f"marksheet_{unit.code if unit else 'unknown'}_{class_obj.name if class_obj else 'unknown'}.csv"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', newline='') as f:
            f.write(output.getvalue())
        return {"filepath": filepath, "filename": filename, "file_size_bytes": os.path.getsize(filepath)}
