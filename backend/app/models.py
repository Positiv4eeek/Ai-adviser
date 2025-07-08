import enum
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, DateTime, Enum as SQLEnum,
    Integer, Float, ForeignKey
)
from sqlalchemy.orm import relationship
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


class Curriculum(Base):
    __tablename__ = "curricula"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    program_code   = Column(String, nullable=False)
    program_name   = Column(String, nullable=False)
    intake_year    = Column(Integer, nullable=False)
    language       = Column(String, nullable=True)
    total_credits  = Column(Float, nullable=False)

    courses        = relationship("Course", back_populates="curriculum", cascade="all, delete-orphan")
    electives      = relationship("Elective", back_populates="curriculum", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    curriculum_id    = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    year             = Column(Integer, nullable=False)
    semester         = Column(String, nullable=False)
    block            = Column(String, nullable=False)
    discipline_code  = Column(String, nullable=False)
    discipline_name  = Column(String, nullable=False)
    discipline_type  = Column(String, nullable=False)
    credits          = Column(Float, nullable=False)
    contact_hours    = Column(Float, nullable=True)
    exam_type        = Column(String, nullable=True)
    prerequisite     = Column(String, nullable=True)
    module           = Column(String, nullable=False)

    curriculum       = relationship("Curriculum", back_populates="courses")

class Elective(Base):
    __tablename__ = "electives"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    curriculum_id    = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    group_name       = Column(String, nullable=False)
    block            = Column(String, nullable=False)
    discipline_code  = Column(String, nullable=False)
    discipline_name  = Column(String, nullable=False)
    discipline_type  = Column(String, nullable=False)
    credits          = Column(Float, nullable=False)
    contact_hours    = Column(Float, nullable=True)
    exam_type        = Column(String, nullable=True)
    prerequisite     = Column(String, nullable=True)
    module           = Column(String, nullable=False)

    curriculum       = relationship("Curriculum", back_populates="electives")
