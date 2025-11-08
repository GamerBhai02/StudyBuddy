from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    study_plans = relationship("StudyPlan", back_populates="user")

class StudyPlan(Base):
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    exam_type = Column(String)
    exam_date = Column(Date)
    daily_hours = Column(Float)
    target_grade = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="study_plans")
    topics = relationship("Topic", back_populates="study_plan", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"))
    name = Column(String)
    weight = Column(Float)
    allocated_hours = Column(Float)
    order_index = Column(Integer)
    
    study_plan = relationship("StudyPlan", back_populates="topics")
    sessions = relationship("Session", back_populates="topic", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    scheduled_date = Column(Date)
    duration = Column(Float)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    topic = relationship("Topic", back_populates="sessions")

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"))
    filename = Column(String)
    file_type = Column(String)  # pyq, syllabus, notes, mock
    extracted_text = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
