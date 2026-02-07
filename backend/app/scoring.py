ACADEMIC_COMPATIBILITY = {
    "ug": ["ug", "pg"],
    "pg": ["ug", "pg", "phd"],
    "phd": ["pg", "phd"]
}

def methodology_score(student_methods: list, faculty_methods: list) -> float:
    if not faculty_methods:
        return 0.0
    overlap = set(student_methods) & set(faculty_methods)
    return len(overlap) / len(faculty_methods)


def academic_level_score(student_level: str, faculty_level: str) -> float:
    return 1.0 if faculty_level in ACADEMIC_COMPATIBILITY.get(student_level, []) else 0.0


def availability_score(student_hours: int, min_required: int = 5) -> float:
    return min(student_hours / min_required, 1.0)


def compatibility_score(student: dict, faculty: dict) -> float:
    return (
        0.4 * methodology_score(student["methodologies"], faculty["methodologies"])
        + 0.3 * academic_level_score(student["academic_level"], faculty["academic_level"])
        + 0.3 * availability_score(student["availability"])
    )


def skill_overlap_score(student_skills: list, project_skills: list) -> float:
    if not project_skills:
        return 0.0
    overlap = set(student_skills) & set(project_skills)
    return len(overlap) / len(project_skills)


def urgency_weight(urgency: str) -> float:
    return {
        "low": 0.8,
        "medium": 1.0,
        "high": 1.2
    }.get(urgency, 1.0)
