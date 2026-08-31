"""
Example ORM models for AI Career Navigator.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resumes = relationship("Resume", back_populates="owner", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(512), nullable=True)
    content = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="resumes")
