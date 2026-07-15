from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    course: str


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str

    class Config:
        from_attributes = True