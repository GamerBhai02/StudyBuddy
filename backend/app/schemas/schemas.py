from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    
    class Config:
        from_attributes = True

class StudyPlanCreate(BaseModel):
    user_id: int
    subject: str
    exam_type: str
    exam_date: date
    daily_hours: float
    target_grade: str

class TopicResponse(BaseModel):
    id: int
    name: str
    weight: float
    allocated_hours: float
    order_index: int
    
    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    id: int
    topic_id: int
    scheduled_date: date
    duration: float
    completed: bool
    
    class Config:
        from_attributes = True

class StudyPlanResponse(BaseModel):
    id: int
    subject: str
    exam_type: str
    exam_date: date
    daily_hours: float
    target_grade: str
    status: str
    topics: List[TopicResponse]
    
    class Config:
        from_attributes = True

class TopicInput(BaseModel):
    name: str
    weight: float

class TopicUpdateRequest(BaseModel):
    topics: List[TopicInput]

class LessonContentResponse(BaseModel):
    topic_name: str
    content: dict
