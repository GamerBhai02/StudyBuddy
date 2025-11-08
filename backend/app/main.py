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


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine, Base
from app.routes import upload, study_plan, lessons, test_gemini
from app.models import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Exam Prep API",
    description="AI-powered exam preparation using Gemini 2.5 Pro",
    version="1.0.0"
)

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
app.include_router(test_gemini.router)

@app.get("/")
async def root():
    return {
        "message": "Smart Exam Prep API powered by Gemini 2.5 Pro",
        "version": "1.0.0",
        "ai_model": "gemini-2.5-pro-preview-03-25"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_provider": "Google Gemini 2.5 Pro"
    }
