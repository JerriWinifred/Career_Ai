from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.database import engine, SessionLocal
from app.database import models
from app.database.models import Student

from app.models.schemas import StudentCreate, StudentResponse

from app.routes.resume import router as resume_router

# ---------------------------------
# Create Database Tables
# ---------------------------------
models.Base.metadata.create_all(bind=engine)

# ---------------------------------
# FastAPI App
# ---------------------------------
app = FastAPI(
    title="CareerPilot AI API",
    version="1.0.0"
)

# ---------------------------------
# CORS
# ---------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# Include Routers
# ---------------------------------
app.include_router(resume_router)

# ---------------------------------
# Database Dependency
# ---------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------
# Home
# ---------------------------------
@app.get("/")
def home():
    return {
        "message": "CareerPilot AI Backend Running 🚀"
    }

# ---------------------------------
# Health Check
# ---------------------------------
@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }
# ---------------------------------
# Register Student
# ---------------------------------
@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    print("Incoming Email:", student.email)

    existing_student = db.query(Student).filter(
        Student.email == student.email
    ).first()

    print("Existing Student:", existing_student)

    if existing_student:
        print("Existing user found")
        return {
            "message": f"Welcome back, {existing_student.name}!",
            "existing": True,
            "student": {
                "id": existing_student.id,
                "name": existing_student.name,
                "email": existing_student.email,
                "course": existing_student.course
            }
        }

    print("Creating New Student")

    new_student = Student(
        name=student.name,
        email=student.email,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student Registered Successfully",
        "existing": False,
        "student": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "course": new_student.course
        }
    }

# ---------------------------------
# Get Students
# ---------------------------------
@app.get("/students", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):
    return db.query(Student).all()

# ---------------------------------
# Delete Student
# ---------------------------------
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully."
    }