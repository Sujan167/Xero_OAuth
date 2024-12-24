# Description: This file contains the database session configuration for SQLAlchemy. It creates a new session for each request and closes it after the request is completed. The get_db function is used as a dependency in FastAPI route functions to provide access to the database session.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os

# Set up the base for SQLAlchemy models
Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal is the factory that creates session instances for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db: Session = SessionLocal()  # Create a new session for each request
    try:
        yield db
    finally:
        db.close()
