from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db import Base, engine, get_db
from app.models import User, UserRole
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


Base.metadata.create_all(bind=engine)

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.student

@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=User.hash_password(data.password),
        role=data.role
    )
    db.add(user)
    db.commit()
    return {"msg": f"User '{data.email}' registered as {data.role.value}"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.email, user.role)
    return {"access_token": token, "token_type": "bearer"}
