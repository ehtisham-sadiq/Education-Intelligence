from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
database_schema = "public"

class Admin(Base):
    __tablename__ = 'admin'
    __table_args__ = {'schema': database_schema}
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class Teacher(Base):
    __tablename__ = 'teachers'
    __table_args__ = {'schema': database_schema}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=False)
    cnic = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    confirm_password = Column(String(255), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    subjects = Column(Text)  # Postgres-specific ARRAY type can also be used if appropriate
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = {'schema': database_schema}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    confirm_password = Column(String(255), nullable=False)
    gender = Column(String(10), nullable=False)
    dob = Column(Date, nullable=False)
    address = Column(Text, nullable=False)
    class_ = Column(String(50), nullable=False)
    section = Column(String(50), nullable=False)
    roll_no = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class Course(Base):
    __tablename__ = 'courses'
    __table_args__ = {'schema': database_schema}
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    course_code = Column(String(50), unique=True, nullable=False)
    assigned_teacher_id = Column(Integer, ForeignKey('{}.teachers.id'.format(database_schema)))
    assigned_class = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    teacher = relationship("Teacher", back_populates="courses")

Teacher.courses = relationship("Course", order_by=Course.id, back_populates="teacher")

class Subject(Base):
    __tablename__ = 'subjects'
    __table_args__ = {'schema': database_schema}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    teacher_id = Column(Integer, ForeignKey('{}.teachers.id'.format(database_schema)))
    class_to_teach = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    teacher = relationship("Teacher", back_populates="subjects")

Teacher.subjects = relationship("Subject", order_by=Subject.id, back_populates="teacher")

class Document(Base):
    __tablename__ = 'documents'
    __table_args__ = {'schema': database_schema}
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    course_id = Column(Integer, ForeignKey('{}.courses.id'.format(database_schema)))
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    course = relationship("Course", back_populates="documents")

Course.documents = relationship("Document", order_by=Document.id, back_populates="course")

class Attendance(Base):
    __tablename__ = 'attendance'
    __table_args__ = {'schema': database_schema}
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('{}.students.id'.format(database_schema)))
    course_id = Column(Integer, ForeignKey('{}.courses.id'.format(database_schema)))
    date = Column(Date, nullable=False)
    status = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())