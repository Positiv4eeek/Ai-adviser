from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
from app.db import get_db
from app.models import User, UserRole
from app.utils.auth import get_current_user, require_admin


router = APIRouter(prefix="/admin/users", tags=["Admin: Users"], dependencies=[Depends(require_admin)])

class UserSummary(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdateRole(BaseModel):
    role: UserRole


@router.get("/", response_model=List[UserSummary])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    return db.query(User).order_by(User.created_at.desc()).all()


@router.patch("/{user_id}", response_model=UserSummary)
def update_user_role(
    user_id: str,
    update: UserUpdateRole,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = update.role
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Нельзя удалить себя")

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "Пользователь удалён"}
