import json
from pathlib import Path

from student_card.models import Student


class JsonStudentRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def list_all(self) -> list[Student]:
        return self._load()

    def get(self, student_id: str) -> Student | None:
        normalized_id = student_id.strip().casefold()
        return next(
            (
                student
                for student in self._load()
                if student.student_id.casefold() == normalized_id
            ),
            None,
        )

    def find(self, query: str) -> list[Student]:
        normalized_query = query.strip().casefold()
        if not normalized_query:
            return []
        return [
            student
            for student in self._load()
            if normalized_query in student.student_id.casefold()
            or normalized_query in student.full_name.casefold()
        ]

    def add(self, student: Student) -> None:
        students = self._load()
        if any(
            current.student_id.casefold() == student.student_id.casefold()
            for current in students
        ):
            raise ValueError(f"Student ID already exists: {student.student_id}")
        students.append(student)
        self._save(students)

    def update(self, student: Student) -> None:
        students = self._load()
        for index, current in enumerate(students):
            if current.student_id.casefold() == student.student_id.casefold():
                students[index] = student
                self._save(students)
                return
        raise KeyError(f"Student ID not found: {student.student_id}")

    def delete(self, student_id: str) -> bool:
        students = self._load()
        remaining = [
            student
            for student in students
            if student.student_id.casefold() != student_id.strip().casefold()
        ]
        if len(remaining) == len(students):
            return False
        self._save(remaining)
        return True

    def _load(self) -> list[Student]:
        if not self.file_path.exists():
            return []

        records = json.loads(self.file_path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError(f"Student data must be a JSON list: {self.file_path}")

        students = []
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                raise ValueError(f"Invalid student record at index {index}")
            try:
                students.append(Student(**record))
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid student record at index {index}: {error}"
                ) from error
        return students

    def _save(self, students: list[Student]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.file_path.with_name(self.file_path.name + ".tmp")
        data = json.dumps(
            [student.to_dict() for student in students],
            ensure_ascii=False,
            indent=2,
        )
        temporary_path.write_text(data + "\n", encoding="utf-8")
        temporary_path.replace(self.file_path)
