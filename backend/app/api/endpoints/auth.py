import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db import get_db, settings
from app.models import User, UserRole, EmailVerification
from app.utils.auth import create_access_token, get_current_user
from app.utils.email import fm, MessageSchema

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.student

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    role: str

class UpdateProfileRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    old_password: str | None = None
    password: str | None = None

@router.post("/register", status_code=201)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):

    if not data.email.lower().endswith("@narxoz.kz"):
        raise HTTPException(
            status_code=400,
            detail="register.invalid_domain"
        )

    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")

    db.query(EmailVerification).filter(
        EmailVerification.email == data.email
    ).delete()

    code = f"{secrets.randbelow(10**6):06d}"
    ev = EmailVerification(
        email      = data.email,
        first_name = data.first_name,
        last_name  = data.last_name,
        password   = User.hash_password(data.password),
        role       = data.role,
        code       = code,
        expires_at = datetime.utcnow() + timedelta(hours=1),
    )
    db.add(ev)
    db.commit()

    body = f"Ваш код подтверждения: {code}"
    msg = MessageSchema(
        subject="Подтвердите вашу почту",
        recipients=[data.email],
        body=body,
        subtype="plain"
    )
    await fm.send_message(msg)

    return {"msg": "Код подтверждения отправлен на вашу почту"}


@router.post("/verify", status_code=200)
def verify(req: VerifyRequest, db: Session = Depends(get_db)):

    ev = db.query(EmailVerification).filter(
        EmailVerification.email == req.email,
        EmailVerification.code  == req.code
    ).first()

    if not ev or ev.is_expired():
        raise HTTPException(400, "Неверный код или он истёк")

    user = User(
        first_name      = ev.first_name,
        last_name       = ev.last_name,
        email           = ev.email,
        hashed_password = ev.password,
        role            = ev.role,
    )
    db.add(user)
    db.delete(ev)
    db.commit()

    return {"msg": "Email подтверждён, аккаунт создан"}


@router.post("/token", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserOut)
def read_current_user(user: User = Depends(get_current_user)):
    return user

@router.patch("/me", response_model=UserOut)
def update_profile(
    data: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = False

    if data.first_name:
        user.first_name = data.first_name
        updated = True

    if data.last_name:
        user.last_name = data.last_name
        updated = True

    if data.password or data.old_password:
        if not data.password or not data.old_password:
            raise HTTPException(status_code=400, detail="Both old and new password must be provided")
        if not user.verify_password(data.old_password):
            raise HTTPException(status_code=400, detail="Incorrect old password")
        user.hashed_password = User.hash_password(data.password)
        updated = True

    if updated:
        db.commit()
        db.refresh(user)

    return user