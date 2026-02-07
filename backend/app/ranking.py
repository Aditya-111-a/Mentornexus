def compute_final_score(student, faculty, project, research_score):
    """
    Computes final score for a SINGLE (faculty, project) pair
    """

    mode = decide_mode(research_score)
    w = WEIGHTS[mode]

    # ✅ skill presence overlap (student ↔ project)
    skill_score = skill_overlap_score(
        student["skills"],
        project["required_skills"]
    )

    # faculty-level compatibility
    compat_score = compatibility_score(student, faculty)

    # urgency as multiplier
    urgency_factor = urgency_weight(faculty["urgency"])

    avail_score = availability_score(student["availability"])

    base_score = (
        w["research"] * research_score +
        w["skill"] * skill_score +
        w["compatibility"] * compat_score +
        w["availability"] * avail_score
    )

    final_score = base_score * urgency_factor

    explanation = [
        f"Matching mode: {mode.replace('_', ' ')}",
        f"Research similarity: {round(research_score, 3)}",
        f"Project skill overlap: {round(skill_score, 3)}",
        f"Faculty compatibility: {round(compat_score, 3)}",
        f"Faculty urgency: {faculty['urgency']}"
    ]

    return round(final_score, 4), mode, explanation
