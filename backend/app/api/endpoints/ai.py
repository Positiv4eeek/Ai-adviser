from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.utils.auth import get_current_user
from app.models import User, RecommendationLog, Transcript, Curriculum
from app.api.endpoints.transcript import get_current_transcript
from app.utils.openai_client import ask_gpt, get_prompt_content
from pydantic import BaseModel

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

        if not curriculum:
            raise HTTPException(404, "No matching curriculum found")

        template = get_prompt_content(request.prompt_name, db)

        prompt = template.format(
            transcript_courses=transcript_courses,
            curriculum_courses=curriculum["courses"],
            curriculum_electives=curriculum["electives"]
        )

        ai_response = ask_gpt(prompt)

        log = RecommendationLog(
            user_id=user.id,
            prompt_name=request.prompt_name,
            prompt_input=prompt,
            response=ai_response.strip()
        )
        db.add(log)
        db.commit()
        return {"recommendations": ai_response.strip()}

    except Exception as e:
        raise HTTPException(500, detail=str(e))

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
            "prompt_name": log.prompt_name,
            "prompt_input": log.prompt_input,
            "response": log.response,
            "created_at": log.created_at
        }
        for log in logs
    ]