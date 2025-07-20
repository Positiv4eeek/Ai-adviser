from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import AIPrompt
from typing import List
from pydantic import BaseModel
from app.utils.auth import require_admin
from fastapi import Path
from app.utils.auth import User

router = APIRouter(prefix="/admin/prompts", tags=["admin-prompts"])

class PromptBase(BaseModel):
    name: str
    description: str | None = None
    content: str

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    name: str | None = None
    content: str | None = None

class PromptOut(PromptBase):
    id: int

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PromptOut], dependencies=[Depends(require_admin)])
def get_prompts(db: Session = Depends(get_db)):
    return db.query(AIPrompt).all()

@router.post("/", response_model=PromptOut, dependencies=[Depends(require_admin)])
def create_prompt(data: PromptCreate, db: Session = Depends(get_db)):
    if db.query(AIPrompt).filter_by(name=data.name).first():
        raise HTTPException(400, detail="Prompt with this name already exists")
    prompt = AIPrompt(**data.model_dump())
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt

@router.patch("/{prompt_id}", response_model=PromptOut, dependencies=[Depends(require_admin)])
def update_prompt(prompt_id: int, data: PromptUpdate, db: Session = Depends(get_db)):
    prompt = db.query(AIPrompt).filter_by(id=prompt_id).first()
    if not prompt:
        raise HTTPException(404, detail="Prompt not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(prompt, field, value)

    db.commit()
    db.refresh(prompt)
    return prompt

@router.delete("/{prompt_id}", status_code=204)
def delete_prompt(
    prompt_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user: User = Depends(require_admin)
):
    prompt = db.query(AIPrompt).filter(AIPrompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    db.delete(prompt)
    db.commit()