from student_card.models import Student


class StudentCard:
    def __init__(self, student: Student) -> None:
        self.student = student

    def render(self) -> str:
        student = self.student
        return "\n".join(
            (
                "=" * 38,
                "              STUDENT CARD",
                "=" * 38,
                f"Student ID : {student.student_id}",
                f"Name       : {student.full_name}",
                f"Grade      : {student.grade_level}",
                f"Classroom  : {student.classroom}",
                f"Phone      : {student.phone or '-'}",
                "=" * 38,
            )
        )
