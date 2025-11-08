from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService
from app.models.models import UploadedFile
from typing import List

router = APIRouter(prefix="/api/upload", tags=["upload"])
pdf_service = PDFService()
ai_service = AIService()

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    plan_id: int = None,
    file_type: str = "pyq",
    db: Session = Depends(get_db)
):
    """Upload and extract text from PDF"""
    if not pdf_service.validate_pdf(file):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        extracted_text = await pdf_service.extract_text_from_pdf(file)
        
        # Save to database
        uploaded_file = UploadedFile(
            plan_id=plan_id,
            filename=file.filename,
            file_type=file_type,
            extracted_text=extracted_text
        )
        db.add(uploaded_file)
        db.commit()
        db.refresh(uploaded_file)
        
        return {
            "id": uploaded_file.id,
            "filename": file.filename,
            "text_length": len(extracted_text),
            "preview": extracted_text[:200]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-topics")
async def extract_topics(
    text: str,
    subject: str
):
    """Extract topics from text using AI"""
    try:
        topics = await ai_service.extract_topics(text, subject)
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
