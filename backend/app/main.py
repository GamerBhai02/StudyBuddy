from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config.database import engine, Base
from app.routes import upload, study_plan, lessons, test_gemini
from app.models import models
import traceback
import sys

# Create database tables
print("Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")
except Exception as e:
    print(f"❌ Error creating database tables: {e}")
    sys.exit(1)

app = FastAPI(
    title="Smart Exam Prep API",
    description="AI-powered exam preparation using Gemini 2.5 Pro",
    version="1.0.0"
)

# Enhanced exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_trace = traceback.format_exc()
    print(f"\n{'='*60}")
    print(f"❌ UNHANDLED EXCEPTION")
    print(f"Path: {request.method} {request.url.path}")
    print(f"Error Type: {type(exc).__name__}")
    print(f"Error: {str(exc)}")
    print(f"Traceback:")
    print(error_trace)
    print(f"{'='*60}\n")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "error_type": type(exc).__name__,
            "path": str(request.url.path)
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# CORS middleware - MUST be added BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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
        "ai_model": "gemini-2.5-pro-preview-03-25",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_provider": "Google Gemini 2.5 Pro",
        "database": "connected"
    }

@app.get("/debug/db-status")
async def check_database():
    """Check database connection and tables"""
    from app.config.database import SessionLocal
    from sqlalchemy import inspect
    
    try:
        db = SessionLocal()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Count users
        user_count = db.query(models.User).count()
        plan_count = db.query(models.StudyPlan).count()
        
        db.close()
        
        return {
            "status": "connected",
            "tables": tables,
            "user_count": user_count,
            "plan_count": plan_count
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
