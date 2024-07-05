from datetime import date, datetime
from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class TeacherBase(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    cnic: str
    gender: str
    date_of_birth: date

class TeacherCreate(TeacherBase):
    password: str
    confirm_password: str
    subjects: List[str]

class TeacherUpdate(TeacherBase):
    subjects: Optional[List[str]] = None

class TeacherInDBBase(TeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Teacher(TeacherInDBBase):
    pass

class TeacherWithCourses(TeacherInDBBase):
    courses: List['Course']

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    gender: str
    dob: date
    address: str
    class_: str
    section: str
    roll_no: int

class StudentCreate(StudentBase):
    password: str
    confirm_password: str

class StudentUpdate(StudentBase):
    pass

class StudentInDBBase(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Student(StudentInDBBase):
    pass

class CourseBase(BaseModel):
    title: str
    description: str
    course_code: str
    assigned_class: str

class CourseCreate(CourseBase):
    assigned_teacher_id: int

class CourseUpdate(CourseBase):
    pass

class CourseInDBBase(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Course(CourseInDBBase):
    pass

class CourseWithDocuments(CourseInDBBase):
    documents: List['Document']

class SubjectBase(BaseModel):
    name: str
    class_to_teach: str

class SubjectCreate(SubjectBase):
    teacher_id: int

class SubjectUpdate(SubjectBase):
    pass

class SubjectInDBBase(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Subject(SubjectInDBBase):
    pass

class DocumentBase(BaseModel):
    title: str
    file_path: str

class DocumentCreate(DocumentBase):
    course_id: int

class DocumentUpdate(DocumentBase):
    pass

class DocumentInDBBase(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Document(DocumentInDBBase):
    pass

class AttendanceBase(BaseModel):
    date: date
    status: bool

class AttendanceCreate(AttendanceBase):
    student_id: int
    course_id: int

class AttendanceInDBBase(AttendanceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Attendance(AttendanceInDBBase):
    pass

# Necessary to resolve forward references in the schema models that reference each other
TeacherWithCourses.update_forward_refs()
CourseWithDocuments.update_forward_refs()