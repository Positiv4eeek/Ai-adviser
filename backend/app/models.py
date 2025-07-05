import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from passlib.context import CryptContext

from app.db import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(str, enum.Enum):
    student = "student"
    admin   = "admin"

class User(Base):
    __tablename__ = "users"

    id               = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name       = Column(String, nullable=False)
    last_name        = Column(String, nullable=False)
    email            = Column(String, unique=True, index=True, nullable=False)
    hashed_password  = Column(String, nullable=False)
    role             = Column(SQLEnum(UserRole), nullable=False, default=UserRole.student)
    created_at       = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def hash_password(cls, pwd: str) -> str:
        return pwd_context.hash(pwd)

    def verify_password(self, pwd: str) -> bool:
        return pwd_context.verify(pwd, self.hashed_password)


class EmailVerification(Base):
    __tablename__ = "email_verifications"

    email       = Column(String, primary_key=True, index=True, nullable=False)
    first_name  = Column(String, nullable=False)
    last_name   = Column(String, nullable=False)
    password    = Column(String, nullable=False)
    role        = Column(SQLEnum(UserRole), nullable=False, default=UserRole.student)
    code        = Column(String, unique=True, index=True, nullable=False)
    expires_at  = Column(DateTime, nullable=False)

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at
