import re
from typing import Optional


class FilenameService:

    @staticmethod
    def _sanitize(text: str) -> str:
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s]+', '_', text.strip())
        return text.upper()

    @classmethod
    def generate_assessment_filename(cls, admission_number: str, unit_name: str, document_type: str, assessment_number: str, term: int, year: int, assessed_by_name: str, item_reference: Optional[str] = None, file_index: Optional[int] = None, extension: str = "pdf") -> str:
        parts = [cls._sanitize(admission_number), cls._sanitize(unit_name), cls._sanitize(document_type), cls._sanitize(assessment_number), f"TERM{term}", str(year), "ASSESSED_BY", cls._sanitize(assessed_by_name)]
        if item_reference:
            parts.append(cls._sanitize(item_reference))
        if file_index is not None:
            parts.append(f"FILE{file_index:02d}")
        return "-".join(parts) + f".{extension}"

    @classmethod
    def generate_evidence_filename(cls, admission_number: str, unit_code: str, document_type: str, assessment_number: str, term: int, year: int, assessed_by_name: str, item_reference: Optional[str] = None, file_index: int = 1, extension: str = "jpg") -> str:
        return cls.generate_assessment_filename(admission_number, unit_code, document_type, assessment_number, term, year, assessed_by_name, item_reference, file_index, extension)

    @classmethod
    def generate_marksheet_filename(cls, unit_code: str, class_name: str, academic_period: str, extension: str = "xlsx") -> str:
        return f"MARKSHEET-{cls._sanitize(unit_code)}-{cls._sanitize(class_name)}-{cls._sanitize(academic_period)}.{extension}"

    @classmethod
    def generate_report_filename(cls, report_type: str, department: str, academic_period: str, extension: str = "pdf") -> str:
        return f"REPORT-{cls._sanitize(report_type)}-{cls._sanitize(department)}-{cls._sanitize(academic_period)}.{extension}"
