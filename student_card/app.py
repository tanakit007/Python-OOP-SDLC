from pathlib import Path

from student_card.card import StudentCard
from student_card.models import Student
from student_card.repository import JsonStudentRepository


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "students.json"


class StudentCardApp:
    def __init__(self, repository: JsonStudentRepository) -> None:
        self.repository = repository

    def run(self) -> None:
        while True:
            print(
                "\n=== Student Card Management ===\n"
                "1. Add student\n"
                "2. List students\n"
                "3. Search students\n"
                "4. Update student\n"
                "5. Delete student\n"
                "6. Show student card\n"
                "0. Exit"
            )
            choice = input("Choose an option: ").strip()
            actions = {
                "1": self._add_student,
                "2": self._list_students,
                "3": self._search_students,
                "4": self._update_student,
                "5": self._delete_student,
                "6": self._show_card,
            }
            if choice == "0":
                print("Goodbye!")
                return
            action = actions.get(choice)
            if action is None:
                print("Please choose a valid option.")
                continue
            action()

    def _prompt_student(self, student_id: str | None = None) -> Student:
        if student_id is None:
            student_id = self._prompt_required("Student ID: ")
        return Student(
            student_id=student_id,
            full_name=self._prompt_required("Full name: "),
            grade_level=self._prompt_required("Grade level: "),
            classroom=self._prompt_required("Classroom: "),
            phone=input("Phone (optional): ").strip(),
        )

    @staticmethod
    def _prompt_required(message: str) -> str:
        while True:
            value = input(message).strip()
            if value:
                return value
            print("This field is required.")

    def _add_student(self) -> None:
        try:
            self.repository.add(self._prompt_student())
        except ValueError as error:
            print(error)
            return
        print("Student added.")

    def _list_students(self) -> None:
        students = self.repository.list_all()
        if not students:
            print("No students found.")
            return
        for student in students:
            print(
                f"{student.student_id} | {student.full_name} | "
                f"{student.grade_level}/{student.classroom}"
            )

    def _search_students(self) -> None:
        query = input("Search by student ID or name: ").strip()
        matches = self.repository.find(query)
        if not matches:
            print("No matching students found.")
            return
        for student in matches:
            print(
                f"{student.student_id} | {student.full_name} | "
                f"{student.grade_level}/{student.classroom}"
            )

    def _update_student(self) -> None:
        student_id = input("Student ID to update: ").strip()
        if self.repository.get(student_id) is None:
            print(f"Student ID not found: {student_id}")
            return
        try:
            self.repository.update(self._prompt_student(student_id))
        except ValueError as error:
            print(error)
            return
        print("Student updated.")

    def _delete_student(self) -> None:
        student_id = input("Student ID to delete: ").strip()
        if not self.repository.delete(student_id):
            print(f"Student ID not found: {student_id}")
            return
        print("Student deleted.")

    def _show_card(self) -> None:
        student_id = input("Student ID: ").strip()
        student = self.repository.get(student_id)
        if student is None:
            print(f"Student ID not found: {student_id}")
            return
        print(StudentCard(student).render())


def main() -> None:
    StudentCardApp(JsonStudentRepository(DATA_FILE)).run()
