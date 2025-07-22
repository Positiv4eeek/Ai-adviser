from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, conint, confloat
from app.models import AISettings
from app.db import get_db
from app.utils.auth import require_admin

router = APIRouter(prefix="/admin/ai-settings", tags=["admin-ai-settings"])

class AISettingsSchema(BaseModel):
    model: str
    system_prompt: str
    temperature: confloat(ge=0, le=2)
    max_tokens: conint(ge=1)

    class Config:
        from_attributes = True

@router.get("/", response_model=AISettingsSchema, dependencies=[Depends(require_admin)])
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(AISettings).first()
    if not settings:
        raise HTTPException(status_code=404, detail="AI settings not found.")
    return settings

@router.put("/", response_model=AISettingsSchema, dependencies=[Depends(require_admin)])
def update_settings(data: AISettingsSchema, db: Session = Depends(get_db)):
    settings = db.query(AISettings).first()
    if settings:
        for key, value in data.model_dump().items():
            setattr(settings, key, value)
    else:
        settings = AISettings(**data.model_dump())
        db.add(settings)
    db.commit()
    return settings
