from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.utils.auth import get_current_user
from app.models import User, RecommendationLog, Transcript, Curriculum, AIPrompt
from app.api.endpoints.transcript import get_current_transcript
from app.utils.openai_client import ask_gpt, get_prompt_content
from pydantic import BaseModel
from datetime import datetime
import json
import traceback

router = APIRouter(prefix="/ai", tags=["ai"])

class PromptNameRequest(BaseModel):
    prompt_name: str

@router.post("/recommendations")
def recommend_courses(
    request: PromptNameRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        data = get_current_transcript(user=user, db=db)
        transcript_courses = data["courses"]
        curriculum = data.get("curriculum")
        student_info = data["student_info"]

        name = student_info.get("name")
        specialty = student_info.get("program_name")
        entry_year = student_info.get("entry_year")
        gpa = student_info.get("gpa")
        program_name = student_info.get("program_name")
        
        current_semester = student_info.get("current_semester")
        if not current_semester:
            try:
                entry_year_int = int(entry_year)
            except Exception:
                raise HTTPException(400, detail="Некорректный формат entry_year в student_info")

            now = datetime.now()
            current_semester = (now.year - entry_year) * 2 + (1 if now.month >= 9 else 0)
            next_semester = current_semester + 1
            next_semester_season = "fall" if next_semester % 2 == 1 else "spring"
            next_study_year = (next_semester + 1) // 2

        if not curriculum:
            raise HTTPException(404, "No matching curriculum found")

        template = get_prompt_content(request.prompt_name, db)

        prompt = template.format(
            student_name=name,
            program_name=specialty,
            entry_year=entry_year,
            gpa=gpa,
            specialty=program_name,
            current_semester=current_semester,
            next_semester=next_semester,
            next_semester_season=next_semester_season,
            next_study_year=next_study_year,
            student_info=json.dumps(student_info, ensure_ascii=False, indent=2),
            transcript_courses=json.dumps(transcript_courses, ensure_ascii=False, indent=2),
            curriculum_courses=json.dumps(curriculum["courses"], ensure_ascii=False, indent=2),
            curriculum_electives=json.dumps(curriculum["electives"], ensure_ascii=False, indent=2)
        )

        ai_response = ask_gpt(prompt, db).strip()

        try:
            parsed = json.loads(ai_response)
        except json.JSONDecodeError:
            raise HTTPException(500, f"AI вернул невалидный JSON:\n{ai_response}")
        
        log = RecommendationLog(
            user_id=user.id,
            student_name=name,
            entry_year=entry_year,
            gpa=gpa,
            specialty=program_name,
            prompt_name=request.prompt_name,
            prompt_input=prompt,
            response=ai_response
        )
        db.add(log)
        db.commit()

        return {"recommendations": ai_response}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/history")
def get_recommendation_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    logs = db.query(RecommendationLog)\
             .filter(RecommendationLog.user_id == user.id)\
             .order_by(RecommendationLog.created_at.desc())\
             .all()

    return [
        {
            "id": log.id,
            "student_name": log.student_name,
            "entry_year": log.entry_year,
            "gpa": log.gpa,
            "specialty": log.specialty,
            "prompt_name": log.prompt_name,
            "prompt_input": log.prompt_input,
            "response": log.response,
            "created_at": log.created_at
        }
        for log in logs
    ]

@router.get("/prompts")
def get_prompts(db: Session = Depends(get_db)):
    return db.query(AIPrompt).all()