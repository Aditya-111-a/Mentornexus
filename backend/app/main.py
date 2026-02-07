from fastapi import FastAPI, HTTPException
from backend.app.schemas import StudentInput, FacultyUpsert
from backend.app.normalize import normalize_student
from backend.app.dataloader import load_faculty_dataset
from backend.app.nlp import ResearchSimilarityEngine
from backend.app.faculty_service import upsert_faculty, list_faculty
from backend.app.ranking import compute_final_score
from backend.app.schemas import StudentUpsert
from backend.app.student_service import upsert_student
from backend.app.search import search_faculty
from backend.app.blockchain_service import commit_match
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MentorNexus")

FACULTY_DATA_PATH = "backend/data/faculty_dataset.csv"

faculty_records, faculty_texts = load_faculty_dataset(FACULTY_DATA_PATH)

nlp_engine = ResearchSimilarityEngine()
if faculty_texts:
    nlp_engine.fit(faculty_texts)


@app.get("/")
def root():
    return {"status": "MentorNexus backend running"}


# ---------- FACULTY MANAGEMENT ----------
@app.post("/faculty/upsert")
def add_or_update_faculty(faculty: FacultyUpsert):
    upsert_faculty(faculty.dict())
    return {"status": "faculty added/updated"}


@app.get("/faculty")
def get_all_faculty():
    return list_faculty()


# ---------- RESEARCH MATCH ----------
@app.post("/match/research")
def research_match(student: StudentInput):
    student_n = normalize_student(student.dict())

    if not student_n.get("research_interest"):
        raise HTTPException(status_code=400, detail="Research interest required")

    scores = nlp_engine.compute(student_n["research_interest"])

    ranked = sorted(
        zip(faculty_records, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "faculty_id": f["faculty_id"],
            "name": f["name"],
            "research_similarity": round(score, 4)
        }
        for f, score in ranked
    ]

@app.post("/match/full")
def full_match(student: StudentInput):
    student_n = normalize_student(student.dict())

    if not faculty_records:
        raise HTTPException(status_code=500, detail="Faculty dataset unavailable")

    research_scores = (
        nlp_engine.compute(student_n["research_interest"])
        if student_n.get("research_interest")
        else [0.0] * len(faculty_records)
    )

    results = []

    for faculty, research_score in zip(faculty_records, research_scores):

        if not faculty.get("is_visible", True):
            continue

        for project in faculty.get("projects", []):

            # 🚫 Project capacity check
            if project["status"] == "full":
                continue

            final_score, mode, explanation = compute_final_score(
                student_n,
                faculty,
                project,
                research_score
            )

            match_id = commit_match(
                student_id=student_n["student_id"],
                faculty_id=faculty["faculty_id"],
                project_id=project["project_id"],
                final_score=final_score,
                match_mode=mode,
                explanation=explanation
            )

            results.append({
                "faculty_id": faculty["faculty_id"],
                "project_id": project["project_id"],
                "project_title": project["title"],
                "name": faculty.get("name", ""),
                "final_score": round(final_score, 4),
                "match_mode": mode,
                "explanation": explanation,
                "match_id": match_id
            })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)

# ---------- STUDENT MANAGEMENT ----------
@app.post("/student/upsert")
def add_or_update_student(student: StudentUpsert):
    upsert_student(student.dict())
    return {"status": "student added/updated"}


# ---------- FACULTY SEARCH ----------
@app.get("/search/faculty")
def faculty_search(q: str):
    return search_faculty(faculty_records, q)
