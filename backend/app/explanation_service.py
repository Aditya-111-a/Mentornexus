import os
import google.generativeai as genai

# configure once
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-1.5-flash"

def polish_explanation(raw_explanation: list, context: dict) -> str:
    """
    raw_explanation: list of explanation strings
    context: { student_skills, project_title, faculty_id }
    """

    prompt = f"""
You are explaining why a faculty project is suitable for a student.

Project: {context.get("project_title")}
Student skills: {", ".join(context.get("student_skills", []))}

Technical reasons:
{chr(10).join(raw_explanation)}

Write a short, clear explanation in simple academic language.
Do NOT invent facts.
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        # fallback (VERY IMPORTANT)
        return " ".join(raw_explanation)
