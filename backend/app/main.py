from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine, Base
from app.routes import upload, study_plan, lessons
from app.models import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Exam Prep API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(study_plan.router)
app.include_router(lessons.router)

@app.get("/")
async def root():
    return {"message": "Smart Exam Prep API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
