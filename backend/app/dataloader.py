import pandas as pd
import json


def load_faculty_dataset(path: str):
    df = pd.read_csv(path)

    faculty_records = []
    faculty_texts = []

    for _, row in df.iterrows():
        record = {
            "faculty_id": row["faculty_id"],
            "name": row["name"],
            "email": row["email"],
            "research_areas": row["research_areas"],
            "required_skills": json.loads(row["required_skills"]),
            "methodologies": row["methodologies"].split(","),
            "publications": row["publications"],
            "urgency": row["urgency"],
            "max_students": row["max_students"],
            "current_students": row["current_students"],
            "academic_level": row["academic_level"],
            "availability": row["availability"],
            "projects": json.loads(row["projects"]) if "projects" in row and pd.notna(row["projects"]) else []
        }

        faculty_records.append(record)

        combined_text = (
            row["research_areas"] + " " + row["publications"]
        )
        faculty_texts.append(combined_text)

    return faculty_records, faculty_texts
