from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class Student:
    student_id: str
    full_name: str
    grade_level: str
    classroom: str
    phone: str = ""

    def __post_init__(self) -> None:
        for field_name in ("student_id", "full_name", "grade_level", "classroom"):
            value = getattr(self, field_name).strip()
            if not value:
                raise ValueError(f"{field_name.replace('_', ' ')} cannot be empty")
            object.__setattr__(self, field_name, value)

        object.__setattr__(self, "phone", self.phone.strip())

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
