import logging
import tempfile
from gtts import gTTS # type: ignore
from pydub import AudioSegment # type: ignore
from transformers import pipeline
import moviepy.editor as mp # type: ignore
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from .schema import StudentCreate, Student, TeacherCreate, Teacher, CourseCreate, Course, DocumentCreate, Document, AttendanceCreate, Attendance
from models.db_models import Student as DBStudent, Teacher as DBTeacher, Course as DBCourse, Document as DBDocument, Attendance as DBAttendance
from client import session_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Education Management"])

# Student endpoints
@router.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(session_manager)):
    try:
        with session_manager() as db:
            db_student = DBStudent(**student.dict())
            db.add(db_student)
            db.commit()
            db.refresh(db_student)
            return db_student
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating student: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    #     db_student = DBStudent(**student.dict())
    #     db.add(db_student)
    #     db.commit()
    #     db.refresh(db_student)
    #     return db_student
    # except Exception as e:
    #     db.rollback()
    #     logger.error(f"Error creating student: {e}")
    #     raise HTTPException(status_code=400, detail=str(e))

@router.get("/students/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(session_manager)):
    students = db.query(DBStudent).offset(skip).limit(limit).all()
    return students

@router.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(session_manager)):
    student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Teacher endpoints
@router.post("/teachers/", response_model=Teacher, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(session_manager)):
    try:
        db_teacher = DBTeacher(**teacher.dict())
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
        return db_teacher
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating teacher: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/teachers/", response_model=List[Teacher])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(session_manager)):
    teachers = db.query(DBTeacher).offset(skip).limit(limit).all()
    return teachers

# Course endpoints
@router.post("/courses/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(session_manager)):
    try:
        db_course = DBCourse(**course.dict())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating course: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/courses/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(session_manager)):
    courses = db.query(DBCourse).offset(skip).limit(limit).all()
    return courses

# Document endpoints
@router.post("/documents/", response_model=Document, status_code=status.HTTP_201_CREATED)
def create_document(document: DocumentCreate, db: Session = Depends(session_manager)):
    try:
        db_document = DBDocument(**document.dict())
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating document: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Attendance endpoints
@router.post("/attendance/", response_model=Attendance, status_code=status.HTTP_201_CREATED)
def record_attendance(attendance: AttendanceCreate, db: Session = Depends(session_manager)):
    try: 
        db_attendance = DBAttendance(**attendance.dict())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    except Exception as e :
        db.rollback()
        logger.error(f"Error recording attendance: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    
# Load Hugging Face pipelines
summarizer = pipeline("summarization")
speech_recognizer = pipeline("automatic-speech-recognition")

@router.post("/documents/pdf-to-audio")
async def convert_pdf_to_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(await file.read())
            # Assuming text extraction from PDF is already done, use gTTS to convert to audio
            text = "Extracted text goes here"  # Placeholder for actual text extraction logic
            tts = gTTS(text)
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(audio_file.name)
            return FileResponse(path=audio_file.name, filename="converted_audio.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/pdf-to-summary")
async def convert_pdf_to_summary(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(await file.read())
            text = "Extracted text goes here"  # Placeholder for actual text extraction
            summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
            return {"summary": summary[0]['summary_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/video-to-audio")
async def convert_video_to_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename[-4:]) as tmp:
            tmp.write(await file.read())
            video = mp.VideoFileClip(tmp.name)
            audio = video.audio
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            audio.write_audiofile(audio_file.name)
            return FileResponse(path=audio_file.name, filename="extracted_audio.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/video-to-text")
async def convert_video_to_text(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename[-4:]) as tmp:
            tmp.write(await file.read())
            video = mp.VideoFileClip(tmp.name)
            audio = video.audio
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio.write_audiofile(audio_file.name)
            transcription = speech_recognizer(audio_file.name)
            return {"transcription": transcription['text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/alt-pdf-to-audio")
async def alternative_convert_pdf_to_audio(file: UploadFile = File(...)):
    # Similar implementation to pdf-to-audio, possibly using a different text-to-speech model
    return {"message": "This endpoint would use a different model or method to convert PDF to audio."}