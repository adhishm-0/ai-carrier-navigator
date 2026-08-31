"""
Database setup using SQLAlchemy.
Creates engine, session factory, and declarative base.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

from config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

# Use SQLAlchemy 2.0 style engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

def get_engine():
    return engine

def get_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def create_all_tables():
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
        return False
