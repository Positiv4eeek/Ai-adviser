from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
import tempfile, os, json
from datetime import datetime
from typing import List

from app.db import get_db
from app.models import User, Transcript, TranscriptCourse, Curriculum
from app.utils.parse_transcript import parse_transcript
from app.utils.auth import get_current_user, require_admin
from pydantic import BaseModel
from app.utils.auth import UserRole

router = APIRouter(prefix="/transcript", tags=["transcript"])

class CourseOut(BaseModel):
    code: int
    course_name: str
    credits: int
    percent: float | None
    grade_letter: str | None
    grade_point: float | None
    grade_traditional: str | None
    is_retake: bool


class TranscriptOut(BaseModel):
    id: int
    student_id: str
    parsed_at: datetime
    student_info: dict
    courses: List[CourseOut]


class TranscriptSummary(BaseModel):
    id: int
    student_id: str
    parsed_at: datetime
    student_info: dict


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)]
)
async def upload_transcript(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old = db.query(Transcript).filter_by(user_id=current_user.id).all()
    for tr in old:
        db.query(TranscriptCourse).filter_by(transcript_id=tr.id).delete()
        db.delete(tr)
    db.commit()

    suffix = os.path.splitext(file.filename)[1] or ".pdf"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(await file.read())
        tmp.close()

        data = parse_transcript(tmp.name)

        tr = Transcript(
            user_id      = current_user.id,
            student_id   = data["student_id"],
            parsed_at    = datetime.fromisoformat(data["parsed_at"]),
            student_info = json.dumps(data["student_info"], ensure_ascii=False),
        )
        db.add(tr)
        db.flush()

        for c in data["courses"]:
            db.add(TranscriptCourse(
                transcript_id     = tr.id,
                code              = c["code"],
                course_name       = c["course_name"],
                credits           = c["credits"],
                percent           = c.get("percent"),
                grade_letter      = c.get("grade_letter"),
                grade_point       = c.get("grade_point"),
                grade_traditional = c.get("grade_traditional"),
                is_retake         = c.get("is_retake", False),
            ))

        db.commit()
        return {"id": tr.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass


@router.get(
    "/",
    response_model=List[TranscriptSummary]
)
def list_transcripts(
    user_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    query = db.query(Transcript)
    if user_id:
        query = query.filter_by(user_id=user_id)

    items = query.order_by(Transcript.parsed_at.desc()).all()

    return [
        {
            "id": t.id,
            "student_id": t.user_id,
            "parsed_at": t.parsed_at,
            "student_info": json.loads(t.student_info) if t.student_info else {}
        }
        for t in items
    ]

@router.get("/current")
def get_current_transcript(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transcript = (
        db.query(Transcript)
        .filter(Transcript.user_id == user.id)
        .order_by(Transcript.parsed_at.desc())
        .first()
    )

    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    try:
        student_info = json.loads(transcript.student_info)
    except (json.JSONDecodeError, TypeError):
        student_info = {}

    program_name = student_info.get("program_name")
    intake_year = student_info.get("entry_year")
    curriculum = None

    if program_name and intake_year:
        curriculum = (
            db.query(Curriculum)
            .filter(
                Curriculum.program_name == program_name,
                Curriculum.intake_year == intake_year
            )
            .first()
        )

    return {
        "id": transcript.id,
        "student_id": transcript.student_id,
        "parsed_at": transcript.parsed_at,
        "student_info": student_info,
        "curriculum": {
            "id": curriculum.id,
            "program_code": curriculum.program_code,
            "program_name": curriculum.program_name,
            "intake_year": curriculum.intake_year,
            "language": curriculum.language,
            "total_credits": curriculum.total_credits,
            "courses": [
                {
                    "id": course.id,
                    "year": course.year,
                    "semester": course.semester,
                    "block": course.block,
                    "discipline_code": course.discipline_code,
                    "discipline_name": course.discipline_name,
                    "discipline_type": course.discipline_type,
                    "credits": course.credits,
                    "contact_hours": course.contact_hours,
                    "exam_type": course.exam_type,
                    "prerequisite": course.prerequisite,
                    "module": course.module,
                }
                for course in curriculum.courses
            ],
            "electives": [
                {
                    "id": elective.id,
                    "group_name": elective.group_name,
                    "block": elective.block,
                    "discipline_code": elective.discipline_code,
                    "discipline_name": elective.discipline_name,
                    "discipline_type": elective.discipline_type,
                    "credits": elective.credits,
                    "contact_hours": elective.contact_hours,
                    "exam_type": elective.exam_type,
                    "prerequisite": elective.prerequisite,
                    "module": elective.module,
                }
                for elective in curriculum.electives
            ]
        } if curriculum else None,
        "courses": [
            {
                "code": course.code,
                "course_name": course.course_name,
                "credits": course.credits,
                "percent": course.percent,
                "grade_letter": course.grade_letter,
                "grade_point": course.grade_point,
                "grade_traditional": course.grade_traditional,
                "is_retake": course.is_retake,
            }
            for course in transcript.courses
        ]
    }


@router.get(
    "/{transcript_id}",
    response_model=TranscriptOut
)
def get_transcript(
    transcript_id: int,
    db: Session = Depends(get_db),
):
    try:
        print("Looking for transcript with id:", transcript_id)
        tr = db.query(Transcript).filter(Transcript.id == transcript_id).first()
        if not tr:
            print("Transcript not found")
            raise HTTPException(status_code=404, detail="Transcript not found")

        student_info = json.loads(tr.student_info)
        courses = db.query(TranscriptCourse).filter_by(transcript_id=tr.id).all()

        return {
            "id": tr.id,
            "student_id": tr.student_id,
            "parsed_at": tr.parsed_at,
            "student_info": student_info,
            "courses": [
                {
                    "code":              c.code,
                    "course_name":       c.course_name,
                    "credits":           c.credits,
                    "percent":           c.percent,
                    "grade_letter":      c.grade_letter,
                    "grade_point":       c.grade_point,
                    "grade_traditional": c.grade_traditional,
                    "is_retake":         c.is_retake,
                }
                for c in courses
            ],
        }
    except Exception as e:
        print("Exception occurred:", str(e))
        raise HTTPException(status_code=500, detail="Server error")
    
@router.delete("/{transcript_id}", status_code=204)
def delete_transcript(
    transcript_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    transcript = db.query(Transcript).filter_by(id=transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    db.query(TranscriptCourse).filter_by(transcript_id=transcript_id).delete()
    db.delete(transcript)
    db.commit()