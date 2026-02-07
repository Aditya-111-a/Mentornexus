from backend.app.explanation_service import polish_explanation


def search_faculty(faculty_records, query: str):
    q = query.lower()
    results = []

    for f in faculty_records:
        if not f.get("is_visible", True):
            continue

        faculty_text = (
            f.get("research_areas", "") + " " + f.get("publications", "")
        ).lower()

        matched_projects = []

        for project in f.get("projects", []):
            project_text = (
                project.get("title", "") + " " + project.get("description", "")
            ).lower()

            if q in project_text:
                # raw, deterministic explanation
                raw_explanation = [
                    f"Project title matches the search query '{query}'.",
                    f"Project status is '{project['status']}'.",
                    f"Current team size is {project['current_students']} "
                    f"out of {project['max_students']} students."
                ]

                # Gemini-polished explanation (safe fallback)
                explanation = polish_explanation(
                    raw_explanation,
                    {
                        "project_title": project.get("title", ""),
                        "student_skills": [],   # search has no student context
                        "faculty_id": f["faculty_id"]
                    }
                )

                matched_projects.append({
                    "project_id": project["project_id"],
                    "title": project["title"],
                    "status": project["status"],
                    "current_students": project["current_students"],
                    "max_students": project["max_students"],
                    "explanation": explanation
                })

        # include faculty if query matches faculty OR any project
        if q in faculty_text or matched_projects:
            results.append({
                "faculty_id": f["faculty_id"],
                "name": f.get("name", ""),
                "research_areas": f.get("research_areas", ""),
                "projects": matched_projects  # may be empty
            })

    return results
