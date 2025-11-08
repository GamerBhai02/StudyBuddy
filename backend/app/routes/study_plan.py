from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.schemas import (
    StudyPlanCreate, StudyPlanResponse, TopicUpdateRequest
)
from app.models.models import StudyPlan, Topic, User
from app.services.plan_service import PlanService
from typing import List
from datetime import date

router = APIRouter(prefix="/api/study-plan", tags=["study-plan"])
plan_service = PlanService()

@router.post("/create", response_model=StudyPlanResponse)
async def create_study_plan(
    plan_data: StudyPlanCreate,
    db: Session = Depends(get_db)
):
    """Create a new study plan"""
    # Verify user exists
    user = db.query(User).filter(User.id == plan_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create study plan
    study_plan = StudyPlan(
        user_id=plan_data.user_id,
        subject=plan_data.subject,
        exam_type=plan_data.exam_type,
        exam_date=plan_data.exam_date,
        daily_hours=plan_data.daily_hours,
        target_grade=plan_data.target_grade
    )
    
    db.add(study_plan)
    db.commit()
    db.refresh(study_plan)
    
    return study_plan

@router.post("/{plan_id}/generate-plan")
async def generate_plan(
    plan_id: int,
    topics_data: TopicUpdateRequest,
    db: Session = Depends(get_db)
):
    """Generate study plan from topics"""
    study_plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
    if not study_plan:
        raise HTTPException(status_code=404, detail="Study plan not found")
    
    # Generate plan
    plan = plan_service.generate_study_plan(
        topics=[{"name": t.name, "weight": t.weight} for t in topics_data.topics],
        exam_date=study_plan.exam_date,
        daily_hours=study_plan.daily_hours
    )
    
    # Save topics
    current_date = date.today()
    for topic_data in plan:
        topic = Topic(
            plan_id=plan_id,
            name=topic_data['name'],
            weight=topic_data['weight'],
            allocated_hours=topic_data['allocated_hours'],
            order_index=topic_data['order_index']
        )
        db.add(topic)
        db.flush()
        
        # Create sessions for this topic
        plan_service.create_sessions(
            db=db,
            topic_id=topic.id,
            allocated_hours=topic_data['allocated_hours'],
            start_date=current_date,
            daily_hours=study_plan.daily_hours
        )
        
        current_date = current_date
    
    db.commit()
    
    return {"message": "Study plan generated successfully", "plan_id": plan_id}

@router.get("/{plan_id}", response_model=StudyPlanResponse)
async def get_study_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """Get study plan details"""
    study_plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
    if not study_plan:
        raise HTTPException(status_code=404, detail="Study plan not found")
    
    return study_plan

@router.get("/{plan_id}/dashboard")
async def get_dashboard_data(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """Get dashboard data for a study plan"""
    from sqlalchemy import func
    from app.models.models import Session as StudySession
    
    study_plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
    if not study_plan:
        raise HTTPException(status_code=404, detail="Study plan not found")
    
    # Calculate stats
    total_sessions = db.query(func.count(StudySession.id)).join(Topic).filter(
        Topic.plan_id == plan_id
    ).scalar()
    
    completed_sessions = db.query(func.count(StudySession.id)).join(Topic).filter(
        Topic.plan_id == plan_id,
        StudySession.completed == True
    ).scalar()
    
    progress = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    # Get today's sessions
    today_sessions = db.query(StudySession).join(Topic).filter(
        Topic.plan_id == plan_id,
        StudySession.scheduled_date == date.today()
    ).all()
    
    return {
        "exam_date": study_plan.exam_date,
        "days_remaining": (study_plan.exam_date - date.today()).days,
        "progress": round(progress, 2),
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "today_tasks": [
            {
                "topic": session.topic.name,
                "duration": session.duration,
                "completed": session.completed
            }
            for session in today_sessions
        ]
    }
