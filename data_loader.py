"""Load and validate the pipe-delimited student dataset."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Student:
    erp: str
    name: str
    cgpa: float
    operating_systems: int
    dsa: int
    mathematics: int

    def mark(self, subject: str) -> int:
        return {
            "Operating Systems": self.operating_systems,
            "DSA": self.dsa,
            "Mathematics": self.mathematics,
        }[subject]


DATA_PATH = Path(__file__).resolve().parent / "data" / "student_sample_data.txt"


class DataLoadError(ValueError):
    """An actionable error encountered while reading the student file."""


def normalize_erp(erp: str) -> str:
    return erp.strip().casefold()


def load_students(path: Path = DATA_PATH) -> list[Student]:
    if not path.is_file():
        raise DataLoadError(f"Dataset file not found: {path}. Add student_sample_data.txt to the data folder.")
    students: list[Student] = []
    seen: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        raise DataLoadError(f"Could not read dataset file: {exc}") from exc
    for line_number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.casefold().startswith("erp|"):
            continue
        fields = [part.strip() for part in line.split("|")]
        if len(fields) != 6:
            raise DataLoadError(f"Line {line_number}: expected 6 pipe-separated fields, found {len(fields)}.")
        erp, name, cgpa_text, os_text, dsa_text, math_text = fields
        if not erp or not name:
            raise DataLoadError(f"Line {line_number}: ERP and name cannot be empty.")
        key = normalize_erp(erp)
        if key in seen:
            raise DataLoadError(f"Line {line_number}: duplicate ERP identifier '{erp}'.")
        try:
            cgpa = float(cgpa_text)
            marks = [int(os_text), int(dsa_text), int(math_text)]
        except ValueError as exc:
            raise DataLoadError(f"Line {line_number}: CGPA must be numeric and marks must be integers.") from exc
        if not 0 <= cgpa <= 10:
            raise DataLoadError(f"Line {line_number}: CGPA must be between 0 and 10.")
        if any(not 0 <= mark <= 100 for mark in marks):
            raise DataLoadError(f"Line {line_number}: marks must be between 0 and 100.")
        students.append(Student(erp, name, cgpa, *marks))
        seen.add(key)
    if not students:
        raise DataLoadError("Dataset contains no student records.")
    return students
