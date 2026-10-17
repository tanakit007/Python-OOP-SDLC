import json
import tempfile
import unittest
from pathlib import Path

from student_card.card import StudentCard
from student_card.models import Student
from student_card.repository import JsonStudentRepository


class StudentTests(unittest.TestCase):
    def test_required_fields_are_trimmed_and_validated(self) -> None:
        student = Student(" S001 ", " Ada Lovelace ", "10", "A")

        self.assertEqual(student.student_id, "S001")
        self.assertEqual(student.full_name, "Ada Lovelace")
        with self.assertRaises(ValueError):
            Student("S002", " ", "10", "A")

    def test_card_contains_student_details(self) -> None:
        card = StudentCard(Student("S001", "Ada Lovelace", "10", "A", "123"))

        self.assertIn("Ada Lovelace", card.render())
        self.assertIn("S001", card.render())
        self.assertIn("Phone      : 123", card.render())


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.file_path = Path(self.temp_dir.name) / "data" / "students.json"
        self.repository = JsonStudentRepository(self.file_path)

    def test_crud_operations_persist_data(self) -> None:
        student = Student("S001", "Ada Lovelace", "10", "A")
        self.repository.add(student)

        self.assertEqual(self.repository.get("s001"), student)
        self.assertEqual(self.repository.find("lovelace"), [student])

        updated = Student("S001", "Ada Byron", "11", "B")
        self.repository.update(updated)
        self.assertEqual(self.repository.list_all(), [updated])

        reopened = JsonStudentRepository(self.file_path)
        self.assertEqual(reopened.list_all(), [updated])
        self.assertTrue(reopened.delete("S001"))
        self.assertEqual(reopened.list_all(), [])
        self.assertFalse(reopened.delete("S001"))

    def test_duplicate_student_ids_are_rejected_case_insensitively(self) -> None:
        self.repository.add(Student("S001", "Ada Lovelace", "10", "A"))

        with self.assertRaises(ValueError):
            self.repository.add(Student("s001", "Another Student", "10", "A"))

    def test_malformed_data_is_reported(self) -> None:
        self.file_path.parent.mkdir(parents=True)
        self.file_path.write_text(json.dumps([{"student_id": "S001"}]), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Invalid student record at index 0"):
            self.repository.list_all()


if __name__ == "__main__":
    unittest.main()
