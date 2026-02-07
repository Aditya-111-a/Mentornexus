SKILL_LEVEL_MAP = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}

def normalize_text(text: str) -> str:
    return text.lower().strip()


def normalize_skills(skills: dict) -> dict:
    return {
        skill.lower(): SKILL_LEVEL_MAP[level.lower()]
        for skill, level in skills.items()
        if level.lower() in SKILL_LEVEL_MAP
    }


def normalize_student(student: dict) -> dict:
    return {
        "student_id": student["student_id"],
        "research_interest": normalize_text(student["research_interest"])
        if student.get("research_interest") else None,
        "skills": normalize_skills(student["skills"]),
        "methodologies": [m.lower() for m in student["methodologies"]],
        "academic_level": student["academic_level"].lower(),
        "availability": student["availability"],
        "goal": student["goal"].lower()
    }


def normalize_faculty(faculty: dict) -> dict:
    return {
        "faculty_id": faculty["faculty_id"],
        "research_areas": normalize_text(faculty["research_areas"]),
        "required_skills": normalize_skills(faculty["required_skills"]),
        "methodologies": [m.lower() for m in faculty["methodologies"]],
        "publications": [normalize_text(p) for p in faculty["publications"]],
        "urgency": faculty["urgency"].lower(),
        "max_students": faculty["max_students"]
    }
