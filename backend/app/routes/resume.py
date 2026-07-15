from fastapi import APIRouter, UploadFile, File, Form
import fitz

from app.data.course_skills import COURSE_SKILLS
from app.data.career_roles import CAREER_ROLES
from app.data.learning_paths import LEARNING_PATHS

router = APIRouter()

# -----------------------------
# General Skill Database
# -----------------------------
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Scikit-Learn",
    "Pandas",
    "NumPy",
    "Power BI",
    "Excel",
    "React",
    "FastAPI",
    "Flask",
    "Django",
    "Git",
    "GitHub",
    "Computer Vision",
    "OpenCV",
    "NLP",
    "Docker",
    "AWS",
    "Azure",
    "Kubernetes",
    "HTML",
    "CSS",
    "JavaScript",
    "Node.js",
    "MongoDB",
    "Linux",
    "Networking",
    "Arduino",
    "Raspberry Pi"
]


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    course: str = Form(...)
):

    # -----------------------------
    # Read PDF
    # -----------------------------
    pdf = fitz.open(
        stream=await file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    text_lower = text.lower()

    # -----------------------------
    # Extract Skills
    # -----------------------------
    extracted_skills = sorted(list(set([
        skill
        for skill in SKILLS
        if skill.lower() in text_lower
    ])))

    # -----------------------------
    # Expected Skills
    # -----------------------------
    expected_skills = COURSE_SKILLS.get(course, [])

    matched_skills = [
        skill
        for skill in expected_skills
        if skill in extracted_skills
    ]

    missing_skills = [
        skill
        for skill in expected_skills
        if skill not in extracted_skills
    ]

    # -----------------------------
    # Career Roles
    # -----------------------------
    career_roles = CAREER_ROLES.get(course, [])

    # -----------------------------
    # Learning Path
    # -----------------------------
    learning_path = LEARNING_PATHS.get(course, [])

    # -----------------------------
    # Resume Score
    # -----------------------------
    if expected_skills:
        skill_score = round(
            (len(matched_skills) / len(expected_skills)) * 100
        )
    else:
        skill_score = 0

    bonus = 0

    if "github" in text_lower:
        bonus += 5

    if "linkedin" in text_lower:
        bonus += 5

    if "project" in text_lower:
        bonus += 5

    if "intern" in text_lower or "experience" in text_lower:
        bonus += 5

    resume_score = min(skill_score + bonus, 100)

    # -----------------------------
    # Resume Level
    # -----------------------------
    if resume_score >= 90:
        level = "Industry Ready 🚀"

    elif resume_score >= 75:
        level = "Advanced 🟢"

    elif resume_score >= 60:
        level = "Intermediate 🟡"

    elif resume_score >= 40:
        level = "Beginner 🟠"

    else:
        level = "Needs Improvement 🔴"

    # -----------------------------
    # Suggestions
    # -----------------------------
    if resume_score >= 90:

        suggestion = (
            "Excellent resume! Keep building projects, internships and maintain your GitHub profile."
        )

    elif resume_score >= 75:

        suggestion = (
            "Strong resume. Improve by learning: "
            + ", ".join(missing_skills)
        )

    elif resume_score >= 50:

        suggestion = (
            "Good foundation. Focus on these skills: "
            + ", ".join(missing_skills)
        )

    else:

        suggestion = (
            "Your resume needs improvement. Start by learning: "
            + ", ".join(missing_skills)
        )

    # -----------------------------
    # Return Response
    # -----------------------------
    return {

        "filename": file.filename,

        "course": course,

        "resume_score": resume_score,

        "skill_match_percentage": skill_score,

        "resume_level": level,

        "skills": extracted_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "matched_count": len(matched_skills),

        "missing_count": len(missing_skills),

        "total_required_skills": len(expected_skills),

        "career_roles": career_roles,

        "learning_path": learning_path,

        "suggestion": suggestion
    }